"""Боковая панель (выбор лаборатории, статистика)."""
import streamlit as st
from typing import Dict
from models import Laboratory


def render_sidebar(labs_data: Dict[str, Laboratory], current_lab: str):
    with st.sidebar:
        st.header("🔬 Лаборатория")

        lab_options = list(labs_data.keys())
        selected_lab = st.selectbox(
            "Выберите лабораторию:",
            options=lab_options,
            index=lab_options.index(current_lab) if current_lab in lab_options else 0,
            key="lab_selector"
        )

        if selected_lab != current_lab:
            st.session_state.current_lab = selected_lab
            st.session_state.lab = labs_data[selected_lab]
            st.rerun()

        st.divider()

        lab = labs_data[current_lab]
        st.markdown("### 📊 Статистика")
        st.write(f"**Всего разделов:** {len(lab.sections)}")
        st.write(f"**Продукции:** {len(lab.get_all_products())}")

        # ОТЛАДКА ТАБЛИЦЫ 3 (временно)
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🐞 ОТЛАДКА")

        if st.sidebar.button("Показать состояние"):
            st.sidebar.write(f"standard_list: {st.session_state.get('standard_list', 'не задано')}")
            st.sidebar.write(f"tnved_list: {st.session_state.get('tnved_list', 'не задано')}")
            st.sidebar.write(f"product_table: {'есть' if st.session_state.get('product_table') else 'нет'}")
            st.sidebar.write(f"standard_table строк: {len(st.session_state.get('standard_table', []))}")
            st.sidebar.write(f"standard_value (сырое): '{st.session_state.get('standard_value', '')}'")

            all_sections = st.session_state.get('all_product_sections_debug', [])
            st.sidebar.write(f"all_product_sections: {len(all_sections)} разделов")
            if all_sections:
                st.sidebar.write(f"Примеры: {all_sections[:5]}")