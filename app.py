"""
Экспертная система ИЛ - версия 2.0
Точка входа в приложение Streamlit.
"""

import streamlit as st
from typing import List, Set

# Импорты наших модулей
from models import Laboratory
from data_loader import load_laboratories
from ui.sidebar import render_sidebar
from ui.inputs import render_product_input, render_tnved_input, render_standard_input
from ui.buttons import render_action_buttons
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

def parse_input_text(text: str) -> list:
    if not text:
        return []
    # Заменяем все разделители на запятую
    for sep in [';', '\n', '\r', '\t']:
        text = text.replace(sep, ',')
    return [item.strip() for item in text.split(',') if item.strip()]

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
    
    # Поля ввода
    if 'product_query' not in st.session_state:
        st.session_state.product_query = ''
    if 'tnved_list' not in st.session_state:
        st.session_state.tnved_list = []
    if 'standard_list' not in st.session_state:
        st.session_state.standard_list = []
    
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
# ОСНОВНОЙ ИНТЕРФЕЙС
# ============================================================
# ============================================================
# ПОЛЯ ВВОДА
# ============================================================
# Поле продукции
product_query = render_product_input(st.session_state.product_query)
st.session_state.product_query = product_query

# Автоподсказки
if product_query and len(product_query) >= 2:
    lab = st.session_state.lab
    all_products = lab.get_all_products()
    suggestions = [p for p in all_products if product_query.lower() in p.lower()]
    if suggestions:
        st.markdown(f"**📋 Найдено в области ({len(suggestions)}):**")
        suggestions_text = ""
        for s in suggestions[:15]:
            suggestions_text += f"• {s}\n"
        if len(suggestions) > 15:
            suggestions_text += f"... и еще {len(suggestions)-15}"
        st.text(suggestions_text)

# Поля ТН ВЭД и Стандартов
col1, col2 = st.columns(2)
with col1:
    tnved_text = render_tnved_input(st.session_state.tnved_list)
with col2:
    standard_text = render_standard_input(st.session_state.standard_list)

# Кнопка "Таблицы"
st.markdown("---")
if st.button("📊 Построить таблицы", type="primary", use_container_width=True, key="btn_build"):
    from logic import search_products, filter_by_tnved, filter_by_standard_and_tnved, group_sections_for_display
    
    # Сохраняем введённые значения
    st.session_state.tnved_list = parse_input_text(tnved_text)
    st.session_state.standard_list = parse_input_text(standard_text) 
    
    lab = st.session_state.lab
    
    # 1. Таблица продукции
    if product_query:
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
    else:
        st.session_state.product_table = None
    
    # 2. Таблица ТН ВЭД
    tnved_list = st.session_state.tnved_list
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
    standard_list = st.session_state.standard_list
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
    st.rerun()

# ============================================================
# ПАНЕЛЬ КНОПОК
# ============================================================
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    if st.button("🌍 Выбрать все", disabled=not st.session_state.tables_built, use_container_width=True, key="btn_select_all"):
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
    if st.button("🔍 Пересечение", type="primary", disabled=not st.session_state.tables_built, use_container_width=True, key="btn_intersect"):
        from logic import intersect_sections
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
    if st.button("🗑️ Очистить", disabled=not st.session_state.tables_built, use_container_width=True, key="btn_clear"):
        # Очищаем переменные
        st.session_state.product_query = ""
        st.session_state.tnved_list = []
        st.session_state.standard_list = []
        
        # Удаляем ключи виджетов, чтобы они пересоздались с пустыми значениями
        for widget_key in ["product_input_main", "tnved_input_main", "standard_input_main"]:
            if widget_key in st.session_state:
                del st.session_state[widget_key]
        
        # Очищаем таблицы
        st.session_state.product_table = None
        st.session_state.tnved_table = None
        st.session_state.standard_table = None
        
        # Очищаем чекбоксы
        for key in list(st.session_state.keys()):
            if key.startswith(('prod_cb_', 'tnved_cb_', 'std_cb_', 'product_checkboxes', 'tnved_checkboxes', 'standard_checkboxes')):
                del st.session_state[key]
        
        st.session_state.selected_products = set()
        st.session_state.selected_tnved = set()
        st.session_state.selected_standards = set()
        st.session_state.intersection_result = None
        st.session_state.intersection_ready = False
        st.session_state.indicators_result = None
        st.session_state.tables_built = False
        st.rerun()

with col5:
    if st.button("💾 Экспорт", disabled=st.session_state.get('indicators_result') is None, use_container_width=True, key="btn_export"):
        pass

with col6:
    if st.button("⚡ Тест", use_container_width=True, key="btn_test"):
        st.session_state.product_query = "белье"
        st.session_state.tnved_list = ["6115", "6116", "6117"]
        st.session_state.standard_list = ["МР 2915-82", "МУ 4395-87"]
        
        # Удаляем ключи виджетов, чтобы они пересоздались с новыми значениями
        for widget_key in ["product_input_main", "tnved_input_main", "standard_input_main"]:
            if widget_key in st.session_state:
                del st.session_state[widget_key]
        
        st.rerun()

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