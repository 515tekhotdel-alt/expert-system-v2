"""
Экспертная система ИЛ - версия 2.0
Точка входа в приложение Streamlit.
"""

import streamlit as st
from st_keyup import st_keyup
from typing import List, Set

from models import Laboratory
from data_loader import load_laboratories
from ui.sidebar import render_sidebar
from ui.tables import render_product_table, render_tnved_table, render_standard_table
from ui.results import render_intersection_result, render_indicators_result
from ui.styles import apply_styles
from datetime import datetime

# ============================================================
# КОНФИГУРАЦИЯ СТРАНИЦЫ
# ============================================================
st.set_page_config(
    page_title="Экспертная система ИЛ v2",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_styles()

# ============================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================
def parse_input_text(text: str) -> list:
    """Парсит ввод пользователя в список."""
    if not text:
        return []
    for sep in [';', '\n', '\r', '\t']:
        text = text.replace(sep, ',')
    return [item.strip() for item in text.split(',') if item.strip()]


def clear_form():
    """Очищает поля формы и таблицы."""
    st.session_state.tnved_value = ""
    st.session_state.standard_value = ""
    st.session_state.product_table = None
    st.session_state.tnved_table = None
    st.session_state.standard_table = None
    st.session_state.tables_built = False
    st.session_state.intersection_result = None
    st.session_state.intersection_ready = False
    st.session_state.indicators_result = None
    # Очищаем чекбоксы
    for key in list(st.session_state.keys()):
        if key.startswith(('prod_cb_', 'tnved_cb_', 'std_cb_')):
            del st.session_state[key]
    st.session_state.product_checkboxes = {}
    st.session_state.tnved_checkboxes = {}
    st.session_state.standard_checkboxes = {}


def set_test_data():
    """Заполняет форму тестовыми данными (кроме продукции)."""
    st.session_state.tnved_value = "6115, 6116, 6117"
    st.session_state.standard_value = "МР 2915-82, МУ 4395-87"


# ============================================================
# ИНИЦИАЛИЗАЦИЯ СЕССИИ
# ============================================================
def init_session_state():
    """Инициализация session_state при первом запуске."""
    if 'labs_data' not in st.session_state:
        with st.spinner('Загрузка данных лабораторий...'):
            st.session_state.labs_data = load_laboratories()
        
        if st.session_state.labs_data:
            st.session_state.current_lab = list(st.session_state.labs_data.keys())[0]
            st.session_state.lab = st.session_state.labs_data[st.session_state.current_lab]
        else:
            st.error("Не удалось загрузить данные. Проверьте подключение к интернету.")
            st.stop()
    
    # Значения полей
    if 'product_value' not in st.session_state:
        st.session_state.product_value = ''
    if 'tnved_value' not in st.session_state:
        st.session_state.tnved_value = ''
    if 'standard_value' not in st.session_state:
        st.session_state.standard_value = ''
    
    # Таблицы
    if 'product_table' not in st.session_state:
        st.session_state.product_table = None
    if 'tnved_table' not in st.session_state:
        st.session_state.tnved_table = None
    if 'standard_table' not in st.session_state:
        st.session_state.standard_table = None
    
    # Выбранные чекбоксы
    if 'selected_products' not in st.session_state:
        st.session_state.selected_products = set()
    if 'selected_tnved' not in st.session_state:
        st.session_state.selected_tnved = set()
    if 'selected_standards' not in st.session_state:
        st.session_state.selected_standards = set()
    
    # Результаты
    if 'intersection_result' not in st.session_state:
        st.session_state.intersection_result = None
    if 'indicators_result' not in st.session_state:
        st.session_state.indicators_result = None
    
    # Состояние UI
    if 'tables_built' not in st.session_state:
        st.session_state.tables_built = False
    if 'intersection_ready' not in st.session_state:
        st.session_state.intersection_ready = False
    
    # Чекбоксы таблиц
    if 'product_checkboxes' not in st.session_state:
        st.session_state.product_checkboxes = {}
    if 'tnved_checkboxes' not in st.session_state:
        st.session_state.tnved_checkboxes = {}
    if 'standard_checkboxes' not in st.session_state:
        st.session_state.standard_checkboxes = {}


init_session_state()

# ============================================================
# ЗАГОЛОВОК
# ============================================================
st.title(f"🔬 Экспертная система ИЛ v2.0 — {st.session_state.current_lab}")

# ============================================================
# САЙДБАР
# ============================================================
render_sidebar(st.session_state.labs_data, st.session_state.current_lab)

# ============================================================
# ПОЛЕ ПРОДУКЦИИ (вне формы, с живыми подсказками)
# ============================================================
st.markdown("### 📦 Продукция")
product_input = st_keyup(
    "Введите название продукции",
    value=st.session_state.product_value,
    placeholder="например: белье, замша, стекло",
    key="product_keyup",
    label_visibility="collapsed"
)
st.session_state.product_value = product_input


# Живые подсказки (только если поле в фокусе)
if product_input and len(product_input) >= 2:
    lab = st.session_state.lab
    all_products = lab.get_all_products()
    suggestions = [p for p in all_products if product_input.lower() in p.lower()]
    if suggestions:
        with st.container():
            st.markdown(f"**📋 Найдено в области ({len(suggestions)}):**")
            suggestions_text = ""
            for s in suggestions[:15]:
                suggestions_text += f"• {s}\n"
            if len(suggestions) > 15:
                suggestions_text += f"... и еще {len(suggestions)-15}"
            st.text(suggestions_text)

# ============================================================
# ФОРМА (ТН ВЭД, Стандарты, кнопки)
# ============================================================
with st.form(key="input_form"):
    col1, col2 = st.columns(2)
    with col1:
        tnved_input = st.text_area(
            "📟 Коды ТН ВЭД",
            value=st.session_state.tnved_value,
            placeholder="6115, 6116, 6117",
            height=80
        )
    with col2:
        standard_input = st.text_area(
            "📄 Стандарты",
            value=st.session_state.standard_value,
            placeholder="ГОСТ 1234-2020, МР 2915-82",
            height=80
        )
    
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        build_btn = st.form_submit_button("📊 Построить таблицы", type="primary", use_container_width=True)
    with col_btn2:
        clear_btn = st.form_submit_button("🗑️ Очистить", on_click=clear_form, use_container_width=True)
    with col_btn3:
        test_btn = st.form_submit_button("⚡ Тест", on_click=set_test_data, use_container_width=True)

# После отправки формы сохраняем значения ТН ВЭД и Стандартов
if build_btn or clear_btn or test_btn:
    st.session_state.tnved_value = tnved_input
    st.session_state.standard_value = standard_input

# ============================================================
# ОБРАБОТКА НАЖАТИЯ "ПОСТРОИТЬ ТАБЛИЦЫ"
# ============================================================
if build_btn and st.session_state.product_value:
    from logic import search_products, filter_by_tnved, filter_by_standard_and_tnved, group_sections_for_display
    
    lab = st.session_state.lab
    product_query = st.session_state.product_value
    
    # 1. Таблица продукции
    products = search_products(lab, product_query)
    if products:
        rows = []
        for product_name, sections in products.items():
            rows.append({
                'Формулировка продукции': product_name,
                'Разделы': group_sections_for_display(sections),
                '_sections': sections
            })
        st.session_state.product_table = rows
    else:
        st.warning("❌ Продукция не найдена")
        st.session_state.product_table = None
    
    # 2. Таблица ТН ВЭД
    tnved_list = parse_input_text(st.session_state.tnved_value)
    if tnved_list and st.session_state.product_table:
        rows = []
        all_product_sections = set().union(*[row['_sections'] for row in st.session_state.product_table])
        for code in tnved_list:
            sections = filter_by_tnved(lab, code, all_product_sections)
            rows.append({
                'ТН ВЭД': code,
                'Разделы': group_sections_for_display(sections) if sections else '❌ Не найден',
                '_sections': sections
            })
        st.session_state.tnved_table = rows
    else:
        st.session_state.tnved_table = None
    
    # 3. Таблица Стандартов
    standard_list = parse_input_text(st.session_state.standard_value)
    if standard_list and tnved_list and st.session_state.product_table:
        rows = []
        all_product_sections = set().union(*[row['_sections'] for row in st.session_state.product_table])
        for std in standard_list:
            for code in tnved_list:
                sections = filter_by_standard_and_tnved(lab, std, code, all_product_sections)
                for sec in sections:
                    full_std_name = std
                    for section in lab.sections:
                        if section.full_id == sec:
                            for s in section.standards:
                                if std.lower() in s.lower():
                                    full_std_name = s
                                    break
                            break
                    rows.append({
                        'Стандарт': full_std_name,
                        'ТН ВЭД': code,
                        'Разделы': group_sections_for_display({sec}),
                        '_sections': {sec}
                    })
        st.session_state.standard_table = rows if rows else None
    else:
        st.session_state.standard_table = None
    
    st.session_state.tables_built = True
    
    # Очищаем старые результаты
    st.session_state.intersection_result = None
    st.session_state.intersection_ready = False
    st.session_state.indicators_result = None
    
    # Сбрасываем чекбоксы
    for key in list(st.session_state.keys()):
        if key.startswith(('prod_cb_', 'tnved_cb_', 'std_cb_')):
            del st.session_state[key]
    st.session_state.product_checkboxes = {}
    st.session_state.tnved_checkboxes = {}
    st.session_state.standard_checkboxes = {}
    
    st.rerun()

# ============================================================
# ПАНЕЛЬ КНОПОК УПРАВЛЕНИЯ (всегда видна)
# ============================================================
tables_built = st.session_state.get('tables_built', False)
intersection_ready = st.session_state.get('intersection_ready', False)
indicators_ready = st.session_state.get('indicators_result') is not None

st.markdown("---")

# Первая строка кнопок
col1, col2, col3, col4 = st.columns(4)

with col1:
    if 'select_all_state' not in st.session_state:
        st.session_state.select_all_state = False
    
    button_label = "🌍 Убрать все" if st.session_state.select_all_state else "🌍 Выбрать все"
    button_type = "secondary" if st.session_state.select_all_state else "primary"
    
    if st.button(button_label, type=button_type, disabled=not tables_built, use_container_width=True, key="btn_select_all"):
        new_value = not st.session_state.select_all_state
        if st.session_state.get('product_table'):
            for i in range(len(st.session_state.product_table)):
                st.session_state[f"prod_cb_{i}"] = new_value
                st.session_state.product_checkboxes[i] = new_value
        if st.session_state.get('tnved_table'):
            for i in range(len(st.session_state.tnved_table)):
                st.session_state[f"tnved_cb_{i}"] = new_value
                st.session_state.tnved_checkboxes[i] = new_value
        if st.session_state.get('standard_table'):
            for i in range(len(st.session_state.standard_table)):
                st.session_state[f"std_cb_{i}"] = new_value
                st.session_state.standard_checkboxes[i] = new_value
        st.session_state.select_all_state = new_value
        st.rerun()

with col2:
    if st.button("🔍 Пересечение", type="primary", disabled=not tables_built, use_container_width=True, key="btn_intersect"):
        selected_product_sections = set()
        selected_tnved_sections = set()
        selected_standard_sections = set()
        
        if st.session_state.get('product_table'):
            for idx, row in enumerate(st.session_state.product_table):
                if st.session_state.get(f"prod_cb_{idx}", False):
                    selected_product_sections.update(row['_sections'])
        
        if st.session_state.get('tnved_table'):
            for idx, row in enumerate(st.session_state.tnved_table):
                if st.session_state.get(f"tnved_cb_{idx}", False):
                    selected_tnved_sections.update(row['_sections'])
        
        if st.session_state.get('standard_table'):
            for idx, row in enumerate(st.session_state.standard_table):
                if st.session_state.get(f"std_cb_{idx}", False):
                    selected_standard_sections.update(row['_sections'])
        
        if selected_tnved_sections:
            common = selected_product_sections & selected_tnved_sections
            if selected_standard_sections:
                common = common & selected_standard_sections
        else:
            common = selected_product_sections
        
        st.session_state.intersection_result = common
        st.session_state.intersection_ready = bool(common)
        st.rerun()

with col3:
    if st.button("📋 Показатели", disabled=not intersection_ready, use_container_width=True, key="btn_indicators"):
        from logic import extract_indicators
        
        lab = st.session_state.lab
        common_sections = st.session_state.intersection_result
        
        selected_std_names = []
        if st.session_state.get('standard_table'):
            for idx, row in enumerate(st.session_state.standard_table):
                if st.session_state.get(f"std_cb_{idx}", False):
                    selected_std_names.append(row['Стандарт'])
        
        indicators = extract_indicators(lab, common_sections, selected_std_names)
        st.session_state.indicators_result = indicators
        st.rerun()

with col4:
    pass  # пустая колонка

# Вторая строка кнопок (Экспорт)
col_exp1, col_exp2, col_exp3, col_exp4 = st.columns([1, 1, 1, 1])

with col_exp2:
    if st.button("📄 Подготовить отчёт", 
                 disabled=not indicators_ready,
                 use_container_width=True,
                 key="btn_prepare_export"):
        if st.session_state.indicators_result:
            import pandas as pd
            import io
            
            output = io.BytesIO()
            all_rows = []
            
            # Параметры поиска
            all_rows.append({'Раздел': 'ПАРАМЕТРЫ ПОИСКА', 'Параметр': '', 'Значение': ''})
            all_rows.append({'Раздел': '', 'Параметр': 'Лаборатория', 'Значение': st.session_state.current_lab})
            all_rows.append({'Раздел': '', 'Параметр': 'Продукция', 'Значение': st.session_state.product_value})
            all_rows.append({'Раздел': '', 'Параметр': 'Коды ТН ВЭД', 'Значение': st.session_state.tnved_value})
            all_rows.append({'Раздел': '', 'Параметр': 'Стандарты', 'Значение': st.session_state.standard_value})
            all_rows.append({'Раздел': '', 'Параметр': '', 'Значение': ''})
            
            # Таблица 1
            if st.session_state.get('product_table'):
                all_rows.append({'Раздел': 'ТАБЛИЦА 1. ПРОДУКЦИЯ', 'Параметр': '', 'Значение': ''})
                for row in st.session_state.product_table:
                    all_rows.append({'Раздел': '', 'Параметр': row['Формулировка продукции'], 'Значение': row['Разделы']})
                all_rows.append({'Раздел': '', 'Параметр': '', 'Значение': ''})
            
            # Таблица 2
            if st.session_state.get('tnved_table'):
                all_rows.append({'Раздел': 'ТАБЛИЦА 2. ТН ВЭД', 'Параметр': '', 'Значение': ''})
                for row in st.session_state.tnved_table:
                    all_rows.append({'Раздел': '', 'Параметр': row['ТН ВЭД'], 'Значение': row['Разделы']})
                all_rows.append({'Раздел': '', 'Параметр': '', 'Значение': ''})
            
            # Таблица 3
            if st.session_state.get('standard_table'):
                all_rows.append({'Раздел': 'ТАБЛИЦА 3. СТАНДАРТЫ', 'Параметр': '', 'Значение': ''})
                for row in st.session_state.standard_table:
                    all_rows.append({
                        'Раздел': '', 
                        'Параметр': f"{row['Стандарт']} ({row['ТН ВЭД']})", 
                        'Значение': row['Разделы']
                    })
                all_rows.append({'Раздел': '', 'Параметр': '', 'Значение': ''})
            
            # Пересечение
            if st.session_state.get('intersection_result'):
                from logic import group_sections_for_display
                all_rows.append({'Раздел': 'РЕЗУЛЬТАТ ПЕРЕСЕЧЕНИЯ', 'Параметр': '', 'Значение': ''})
                all_rows.append({'Раздел': '', 'Параметр': 'Общие разделы', 'Значение': group_sections_for_display(st.session_state.intersection_result)})
                all_rows.append({'Раздел': '', 'Параметр': '', 'Значение': ''})
            
            # Показатели — ОТДЕЛЬНЫЙ БЛОК С 4 КОЛОНКАМИ
            if st.session_state.indicators_result:
                # Создаём отдельный DataFrame для показателей
                indicators_data = []
                for ind in st.session_state.indicators_result:
                    std = ind.get('standard', '—')
                    sec = ind.get('section', '—')
                    name = ind.get('name', '')
                    range_val = ind.get('range', '')
                    
                    # Форматируем раздел
                    if '_' in sec:
                        src, num = sec.split('_', 1)
                        display_sec = f"{src}:{num}"
                    else:
                        display_sec = sec
                    
                    # Стандарт с разделом в скобках
                    std_with_sec = f"{std} ({display_sec})"
                    
                    # Заменяем <br> и \n на перенос строки для Excel
                    range_val_excel = range_val.replace('<br>', '\n').replace('\r\n', '\n').replace('\r', '\n')
                    
                    indicators_data.append({
                        'Стандарт': std_with_sec,
                        'Показатель': name,
                        'Значение': range_val_excel
                    })
                
                df_indicators = pd.DataFrame(indicators_data)
                
                # Сохраняем в Excel
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    # Сначала пишем основные данные на лист "Отчёт"
                    df_main = pd.DataFrame(all_rows)
                    df_main.to_excel(writer, sheet_name='Отчёт', index=False)
                    
                    # Затем показатели на отдельный лист
                    df_indicators.to_excel(writer, sheet_name='Показатели', index=False)
                    
                    # Настраиваем ширину столбцов для листа "Отчёт"
                    worksheet_main = writer.sheets['Отчёт']
                    worksheet_main.column_dimensions['A'].width = 30
                    worksheet_main.column_dimensions['B'].width = 45
                    worksheet_main.column_dimensions['C'].width = 50
                    
                    # Настраиваем ширину и перенос текста для листа "Показатели"
                    worksheet_ind = writer.sheets['Показатели']
                    worksheet_ind.column_dimensions['A'].width = 40
                    worksheet_ind.column_dimensions['B'].width = 35
                    worksheet_ind.column_dimensions['C'].width = 50
                    
                    # Включаем перенос текста для всех ячеек листа "Показатели"
                    from openpyxl.styles import Alignment
                    for row in worksheet_ind.iter_rows():
                        for cell in row:
                            cell.alignment = Alignment(wrap_text=True)
            
            else:
                # Если показателей нет, просто сохраняем основные данные
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_main = pd.DataFrame(all_rows)
                    df_main.to_excel(writer, sheet_name='Отчёт', index=False)
                    worksheet_main = writer.sheets['Отчёт']
                    worksheet_main.column_dimensions['A'].width = 30
                    worksheet_main.column_dimensions['B'].width = 45
                    worksheet_main.column_dimensions['C'].width = 50
            
            output.seek(0)
            st.session_state.export_data = output.getvalue()
            st.session_state.export_ready = True
            st.rerun()

with col_exp3:
    if st.session_state.get('export_ready', False):
        st.download_button(
            label="📥 Скачать",
            data=st.session_state.export_data,
            file_name=f"Экспертная_оценка_{st.session_state.current_lab}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_export_file",
            use_container_width=True
        )
    else:
        st.button("📥 Скачать", disabled=True, use_container_width=True, key="btn_download_disabled")

# ============================================================
# ОТОБРАЖЕНИЕ РЕЗУЛЬТАТОВ
# ============================================================
if st.session_state.intersection_result is not None:
    render_intersection_result(st.session_state.intersection_result)

if st.session_state.indicators_result is not None:
    render_indicators_result(st.session_state.indicators_result)

# ============================================================
# ОТОБРАЖЕНИЕ ТАБЛИЦ
# ============================================================
if st.session_state.tables_built:
    st.markdown("---")
    
    if st.session_state.product_table:
        selected = render_product_table(
            st.session_state.product_table,
            st.session_state.selected_products
        )
        st.session_state.selected_products = selected
    
    if st.session_state.tnved_table:
        selected = render_tnved_table(
            st.session_state.tnved_table,
            st.session_state.selected_tnved
        )
        st.session_state.selected_tnved = selected
    
    if st.session_state.standard_table:
        selected = render_standard_table(
            st.session_state.standard_table,
            st.session_state.selected_standards
        )
        st.session_state.selected_standards = selected