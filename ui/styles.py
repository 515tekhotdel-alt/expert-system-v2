"""CSS стили для приложения."""
import streamlit as st


def apply_styles():
    st.markdown("""
    <style>
        /* Компактные заголовки и отступы */
        h1, h2, h3, h4 {
            margin: 10px 0px 5px 0px !important;
            padding: 0px !important;
        }
        
        hr {
            margin: 8px 0px !important;
        }
        
        /* Компактные кнопки */
        .stButton button {
            padding: 4px 8px !important;
            margin: 2px 0px !important;
        }
        
        /* Уменьшаем отступы в колонках */
        div[data-testid="column"] {
            padding: 0px 5px !important;
        }
        
        /* Таблицы с чекбоксами */
        .stCheckbox {
            padding: 0px !important;
            margin: 0px !important;
        }
        
        /* Таблица показателей */
        .indicators-table {
            border-collapse: collapse;
            width: 100%;
            font-size: 12px;
            margin: 5px 0;
        }
        
        .indicators-table td, .indicators-table th {
            border: 1px solid #ddd;
            padding: 3px 6px;
            vertical-align: top;
        }
        
        .indicators-table th {
            background-color: #f0f0f0;
            color: #000000 !important;
            font-weight: 600;
        }
        
        /* Для тёмной темы — заголовки всегда чёрные */
        .indicators-table th {
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
        }
        
        /* Уменьшаем шрифт в заголовках показателей */
        h3 {
            font-size: 18px !important;
        }
        
        h4 {
            font-size: 14px !important;
            font-weight: 600 !important;
            margin: 8px 0px 3px 0px !important;
        }
    </style>
    """, unsafe_allow_html=True)