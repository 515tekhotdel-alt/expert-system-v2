"""Отображение результатов (пересечение, показатели)."""
import streamlit as st

def render_intersection():
    st.markdown("---")
    st.subheader("🔍 Результат пересечения")
    st.info("Результат пересечения появится здесь")


def render_indicators():
    st.markdown("---")
    st.subheader("📋 Показатели испытаний")
    st.info("Показатели появятся здесь")