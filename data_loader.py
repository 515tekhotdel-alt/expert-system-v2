"""
Загрузка данных из Google Sheets и преобразование в модели.
"""

import re
import pandas as pd
import requests
import io
import streamlit as st
from typing import Dict, List, Set

from models import Laboratory, Section, Indicator


@st.cache_data(ttl=3600, show_spinner="Загрузка данных лабораторий...")
def load_laboratories() -> Dict[str, Laboratory]:
    """
    Загружает данные всех лабораторий из Google Sheets.
    Возвращает словарь {название_лаборатории: Laboratory}.
    Пока ЗАГЛУШКА — будет наполняться постепенно.
    """
    # TODO: реализовать загрузку из Google Sheets
    # Пока возвращаем пустые лаборатории
    
    lab1 = Laboratory(name="ИЛ ЦТС")
    lab2 = Laboratory(name="ИЛ ТЕХЭКСПЕРТ")
    
    return {
        "ИЛ ЦТС": lab1,
        "ИЛ ТЕХЭКСПЕРТ": lab2
    }


def parse_excel_to_sections(excel_content: bytes, source_name: str) -> List[Section]:
    """
    Парсит Excel-файл и возвращает список разделов (Section).
    source_name: 'ч1' или 'ч2'
    ПОКА ЗАГЛУШКА.
    """
    # TODO: перенести логику парсинга из старого кода
    return []