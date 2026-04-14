"""Панель кнопок управления."""
import streamlit as st


def render_action_buttons():
    """Отображает панель кнопок (Выбрать все, Пересечение, Показатели, Очистить, Экспорт, Тест)."""
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.button(
            "🌍 Выбрать все",
            disabled=not st.session_state.get('tables_built', False),
            use_container_width=True,
            key="btn_select_all"
        )
    
    with col2:
        st.button(
            "🔍 Пересечение",
            type="primary",
            disabled=not st.session_state.get('tables_built', False),
            use_container_width=True,
            key="btn_intersect"
        )
    
    with col3:
        st.button(
            "📋 Показатели",
            disabled=not st.session_state.get('intersection_ready', False),
            use_container_width=True,
            key="btn_indicators"
        )
    
    with col4:
        st.button(
            "🗑️ Очистить",
            disabled=not st.session_state.get('tables_built', False),
            use_container_width=True,
            key="btn_clear"
        )
    
    with col5:
        st.button(
            "💾 Экспорт",
            disabled=st.session_state.get('indicators_result') is None,
            use_container_width=True,
            key="btn_export"
        )
    
    with col6:
        st.button(
            "⚡ Тест",
            use_container_width=True,
            key="btn_test"
        )