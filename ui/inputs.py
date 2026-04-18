"""Поля ввода (продукция, ТН ВЭД, стандарты)."""
import streamlit as st
from st_keyup import st_keyup


def render_product_input(default_value: str = "") -> str:
    """Поле ввода продукции с автодополнением (заглушка)."""
    return st.text_input(
        "📦 Продукция",
        value=default_value,
        placeholder="например: белье, замша, стекло",
        key="product_input_main"
    )


def render_tnved_input(default_list: list) -> str:
    """Поле ввода кодов ТН ВЭД."""
    default_text = ", ".join(default_list) if default_list else ""
    return st.text_area(
        "📟 Коды ТН ВЭД",
        value=default_text,
        placeholder="6115, 6116, 6117",
        height=80,
        key="tnved_input_main"
    )


def render_standard_input(default_list: list) -> str:
    """Поле ввода стандартов."""
    default_text = ", ".join(default_list) if default_list else ""
    return st.text_area(
        "📄 Стандарты",
        value=default_text,
        placeholder="ГОСТ 1234-2020, МР 2915-82",
        height=80,
        key="standard_input_main"
    )


def render_mode_selector():
    """Переключатель режима работы."""
    # Инициализация
    if 'search_mode' not in st.session_state:
        st.session_state.search_mode = "Поиск по стандартам"

    def set_mode():
        new_mode = st.session_state.mode_selector_widget
        if st.session_state.search_mode != new_mode:
            # Сбрасываем все таблицы и результаты
            st.session_state.product_table = None
            st.session_state.tnved_table = None
            st.session_state.standard_table = None
            st.session_state.tables_built = False
            st.session_state.intersection_result = None
            st.session_state.intersection_ready = False
            st.session_state.indicators_result = None
            st.session_state.indicator_results = None
            st.session_state.select_all_state = False
            st.session_state.export_ready = False
            # Очищаем чекбоксы
            for key in list(st.session_state.keys()):
                if key.startswith(('prod_cb_', 'tnved_cb_', 'std_cb_')):
                    del st.session_state[key]
            st.session_state.product_checkboxes = {}
            st.session_state.tnved_checkboxes = {}
            st.session_state.standard_checkboxes = {}

        st.session_state.search_mode = new_mode

    st.radio(
        "Режим поиска",
        options=["Поиск по стандартам", "Поиск по показателям"],
        index=0 if st.session_state.search_mode == "Поиск по стандартам" else 1,
        horizontal=True,
        key="mode_selector_widget",
        on_change=set_mode,
        label_visibility="collapsed"
    )
    return st.session_state.search_mode

def render_indicator_input(default_value: str = "") -> str:
    """Поле ввода показателя с живыми автоподсказками."""
    indicator_input = st_keyup(
        "📄 Показатель",
        value=default_value,
        placeholder="например: винилацетат",
        key="indicator_keyup",
        label_visibility="visible"
    )
    return indicator_input