"""Панель кнопок управления."""
import streamlit as st

def render_buttons():
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.button("🌍 Выбрать все", disabled=True, key="btn_select_all")
    with col2:
        st.button("🔍 Пересечение", type="primary", disabled=True, key="btn_intersect")
    with col3:
        st.button("📋 Показатели", disabled=True, key="btn_indicators")
    with col4:
        st.button("🗑️ Очистить", disabled=True, key="btn_clear")
    with col5:
        st.button("💾 Экспорт", disabled=True, key="btn_export")
    with col6:
        st.button("⚡ Тест", key="btn_test")