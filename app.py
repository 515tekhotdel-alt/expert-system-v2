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

# Живые подсказки
if product_input and len(product_input) >= 2:
    lab = st.session_state.lab
    all_products = lab.get_all_products()
    suggestions = [p for p in all_products if product_input.lower() in p.lower()]
    if suggestions:
        st.markdown(f"**📋 Найдено в области ({len(suggestions)}):**")
        suggestions_text = ""
        for s in suggestions[:15]:
            suggestions_text += f"• {s}\n"
        if len(suggestions) > 15:
            suggestions_text += f"... и еще {len(suggestions)-15}"
        st.text(suggestions_text)
    else:
        st.warning("❌ Ничего не найдено")

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
# ПАНЕЛЬ КНОПОК УПРАВЛЕНИЯ
# ============================================================
if st.session_state.tables_built:
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🌍 Выбрать все", use_container_width=True, key="btn_select_all"):
            if st.session_state.product_table:
                for i in range(len(st.session_state.product_table)):
                    st.session_state[f"prod_cb_{i}"] = True
                    st.session_state.product_checkboxes[i] = True
            if st.session_state.tnved_table:
                for i in range(len(st.session_state.tnved_table)):
                    st.session_state[f"tnved_cb_{i}"] = True
                    st.session_state.tnved_checkboxes[i] = True
            if st.session_state.standard_table:
                for i in range(len(st.session_state.standard_table)):
                    st.session_state[f"std_cb_{i}"] = True
                    st.session_state.standard_checkboxes[i] = True
            st.rerun()
    
    with col2:
        if st.button("🔍 Пересечение", type="primary", use_container_width=True, key="btn_intersect"):
            selected_product_sections = set()
            selected_tnved_sections = set()
            selected_standard_sections = set()
            
            if st.session_state.product_table:
                for idx, row in enumerate(st.session_state.product_table):
                    if st.session_state.get(f"prod_cb_{idx}", False):
                        selected_product_sections.update(row['_sections'])
            
            if st.session_state.tnved_table:
                for idx, row in enumerate(st.session_state.tnved_table):
                    if st.session_state.get(f"tnved_cb_{idx}", False):
                        selected_tnved_sections.update(row['_sections'])
            
            if st.session_state.standard_table:
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
        if st.button("📋 Показатели", disabled=not st.session_state.intersection_ready, use_container_width=True, key="btn_indicators"):
            from logic import extract_indicators
            
            lab = st.session_state.lab
            common_sections = st.session_state.intersection_result
            
            selected_std_names = []
            if st.session_state.standard_table:
                for idx, row in enumerate(st.session_state.standard_table):
                    if st.session_state.get(f"std_cb_{idx}", False):
                        selected_std_names.append(row['Стандарт'])
            
            indicators = extract_indicators(lab, common_sections, selected_std_names)
            st.session_state.indicators_result = indicators
            st.rerun()
    
    with col4:
        if st.button("💾 Экспорт", disabled=st.session_state.get('indicators_result') is None, use_container_width=True, key="btn_export"):
            if st.session_state.indicators_result:
                import pandas as pd
                from datetime import datetime
                
                df = pd.DataFrame(st.session_state.indicators_result)
                csv = df.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="Скачать CSV",
                    data=csv,
                    file_name=f"indicators_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )

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