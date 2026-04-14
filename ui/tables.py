"""Компоненты таблиц с чекбоксами."""
import streamlit as st

def render_product_table():
    st.markdown("**📦 Таблица 1. Продукция**")
    st.info("Таблица продукции появится здесь")

def render_tnved_table():
    st.markdown("**📟 Таблица 2. ТН ВЭД**")
    st.info("Таблица ТН ВЭД появится здесь")

def render_standard_table():
    st.markdown("**📄 Таблица 3. Стандарты**")
    st.info("Таблица стандартов появится здесь")