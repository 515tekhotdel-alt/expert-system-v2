"""
Экспертная система ИЛ - версия 2.0
Точка входа в приложение Streamlit.
"""

import streamlit as st

from ui.sidebar import render_sidebar
from ui.inputs import render_inputs
from ui.buttons import render_buttons
from ui.tables import render_product_table, render_tnved_table, render_standard_table
from ui.results import render_intersection, render_indicators
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

# Применяем стили
apply_styles()

# ============================================================
# ЗАГОЛОВОК
# ============================================================
st.title("🔬 Экспертная система ИЛ v2.0")

# ============================================================
# САЙДБАР
# ============================================================
render_sidebar()

# ============================================================
# ОСНОВНОЙ ИНТЕРФЕЙС
# ============================================================
st.markdown("### 📦 Продукция")
render_inputs()

st.markdown("---")
render_buttons()

render_intersection()
render_indicators()

render_product_table()
render_tnved_table()
render_standard_table()