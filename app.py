"""
Экспертная система ИЛ - версия 2.0
Точка входа в приложение Streamlit.
"""

import streamlit as st

# Заглушки для импорта будущих модулей
# from models import Laboratory
# from data_loader import load_laboratory_data
# from ui.sidebar import render_sidebar
# from ui.inputs import render_inputs
# from ui.tables import render_tables
# from ui.buttons import render_buttons
# from ui.results import render_results

# ============================================================
# КОНФИГУРАЦИЯ СТРАНИЦЫ
# ============================================================
st.set_page_config(
    page_title="Экспертная система ИЛ v2",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# ЗАГОЛОВОК
# ============================================================
st.title("🔬 Экспертная система ИЛ v2.0")
st.markdown("---")

# ============================================================
# ЗАГЛУШКА ОСНОВНОГО ИНТЕРФЕЙСА
# ============================================================
st.info("🚧 Программа в разработке. Следите за обновлениями!")
st.markdown("Пока здесь только каркас приложения.")

# ============================================================
# САЙДБАР (заглушка)
# ============================================================
with st.sidebar:
    st.header("🔬 Лаборатория")
    st.selectbox("Выберите лабораторию:", ["ИЛ ЦТС", "ИЛ ТЕХЭКСПЕРТ"])
    st.divider()
    st.button("⚡ Тестовые данные", disabled=True)