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
            font-size: 16px;
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
        
        /* Градиентный заголовок лаборатории */
        .lab-name {
            display: inline-block;
            padding: 12px 30px;
            border-radius: 40px;
            font-size: 28px;
            font-weight: 700;
            color: white;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
            margin-top: 5px;
        }
        
        .lab-cts {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        .lab-tehexpert {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        }
        
        .main-title {
            font-size: 20px;
            font-weight: 400;
            color: #555;
            margin-bottom: 5px;
        }
        
        /* Скрываем меню справа сверху */
        [data-testid="stMainMenu"] {
            display: none !important;
        }
        
        /* Общие стили для всех radio */
        div[data-testid="stRadio"] label {
            padding: 10px 15px !important;
            border-radius: 12px !important;
            margin-bottom: 8px !important;
            transition: all 0.3s ease !important;
            font-weight: 500 !important;
        }
        
        /* ЛАБОРАТОРИИ — фиолетовый и зелёный */
        [data-testid="stSidebar"] [data-testid="stRadio"]:first-of-type label:has(input[value="0"]:checked) {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
        }
        [data-testid="stSidebar"] [data-testid="stRadio"]:first-of-type label:has(input[value="1"]:checked) {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
            color: white !important;
            box-shadow: 0 4px 15px rgba(17, 153, 142, 0.4) !important;
        }
        
        /* РЕЖИМ ПОИСКА — синий и оранжевый */
        [data-testid="stSidebar"] [data-testid="stRadio"]:nth-of-type(2) label:has(input[value="0"]:checked) {
            background: linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%) !important;
            color: white !important;
            box-shadow: 0 4px 15px rgba(33, 147, 176, 0.4) !important;
        }
        [data-testid="stSidebar"] [data-testid="stRadio"]:nth-of-type(2) label:has(input[value="1"]:checked) {
            background: linear-gradient(135deg, #f2994a 0%, #f2c94c 100%) !important;
            color: white !important;
            box-shadow: 0 4px 15px rgba(242, 153, 74, 0.4) !important;
        }
        
        /* При наведении */
        div[data-testid="stRadio"] label:hover {
            background: rgba(102, 126, 234, 0.1) !important;
        }
        
        /* Таблица результатов поиска по показателю */
        .indicator-results-table {
            width: 100%;
            border-collapse: collapse;
            table-layout: auto;
            word-wrap: break-word;
        }
        .indicator-results-table th, .indicator-results-table td {
            border: 1px solid #ddd;
            padding: 6px 8px;
            text-align: left;
            vertical-align: top;
            word-wrap: break-word;
            white-space: normal;
        }
        .indicator-results-table th {
            background-color: #f2f2f2;
            font-weight: 600;
        }
        .indicator-results-table td:nth-child(2) {
            width: 1%;
            white-space: nowrap;
        }
        .indicator-results-table td:nth-child(1) {
            width: auto;
        }
        .indicator-results-table td:nth-child(3) {
            width: 25%;
        }
        .indicator-results-table td:nth-child(4) {
            width: 30%;
        }
        
    </style>
    """, unsafe_allow_html=True)