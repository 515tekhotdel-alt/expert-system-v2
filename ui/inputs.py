"""Поля ввода (продукция, ТН ВЭД, стандарты)."""
import streamlit as st

def render_inputs():
    st.text_input("📦 Продукция", placeholder="например: белье, замша, стекло")
    st.text_area("📟 Коды ТН ВЭД", placeholder="6115, 6116, 6117", height=80)
    st.text_area("📄 Стандарты", placeholder="ГОСТ 1234-2020, МР 2915-82", height=80)