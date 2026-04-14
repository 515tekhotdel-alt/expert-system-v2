"""Компонент боковой панели (выбор лаборатории, статистика)."""
import streamlit as st

def render_sidebar():
    st.sidebar.header("🔬 Лаборатория")
    st.sidebar.selectbox("Выберите лабораторию:", ["ИЛ ЦТС", "ИЛ ТЕХЭКСПЕРТ"])