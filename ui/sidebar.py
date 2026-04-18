"""Боковая панель (выбор лаборатории, статистика)."""
import streamlit as st
from typing import Dict
from models import Laboratory
import os


def render_sidebar(labs_data: Dict[str, Laboratory], current_lab: str):
    with st.sidebar:
        st.header("Лаборатория")

        lab_options = list(labs_data.keys())

        # Красивые названия с иконками
        lab_display = []
        for lab in lab_options:
            if lab == "ИЛ ЦТС":
                lab_display.append("🧬 ИЛ ЦТС")
            else:
                lab_display.append("🧪 ИЛ ТЕХЭКСПЕРТ")

        current_index = lab_options.index(current_lab) if current_lab in lab_options else 0

        selected_index = st.radio(
            "🔍 Выберите лабораторию:",
            options=range(len(lab_options)),
            format_func=lambda i: lab_display[i],
            index=current_index,
            key="lab_selector"
        )
        selected_lab = lab_options[selected_index]

        if selected_lab != current_lab:
            st.session_state.current_lab = selected_lab
            st.session_state.lab = labs_data[selected_lab]
            # НЕ сбрасываем search_mode — оставляем как было
            st.rerun()


        st.divider()
        st.markdown("**Режим поиска**")
        from ui.inputs import render_mode_selector
        mode = render_mode_selector()

