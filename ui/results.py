"""Отображение результатов (пересечение, показатели)."""
import streamlit as st
from typing import Set, List, Dict


def render_intersection_result(common_sections: Set[str]):
    """Отображает результат пересечения."""
    from logic import group_sections_for_display
    
    st.markdown("---")
    st.subheader("🔍 Результат пересечения")
    
    if common_sections:
        st.success(f"✅ ОБЩИЕ РАЗДЕЛЫ: {group_sections_for_display(common_sections)}")
    else:
        st.error("❌ Пересечение не найдено. Проверьте выбор в таблицах.")


def render_indicators_result(indicators: List[Dict]):
    """Отображает показатели испытаний, сгруппированные по стандартам и разделам."""
    st.markdown("---")
    st.subheader("📋 Показатели испытаний")
    
    if not indicators:
        st.info("ℹ️ Нет данных о показателях в выбранных разделах")
        return
    
    # Группируем по стандартам
    from collections import defaultdict
    by_standard = defaultdict(lambda: defaultdict(list))
    
    for ind in indicators:
        std = ind.get('standard', '—')
        sec = ind.get('section', '—')
        by_standard[std][sec].append(ind)
    
    # Отображаем
    for std, sections in by_standard.items():
        st.markdown(f"### 📄 Стандарт: {std}")
        
        for sec, inds in sections.items():
            # Форматируем раздел для отображения
            if '_' in sec:
                src, num = sec.split('_', 1)
                display_sec = f"{src}: {num}"
            else:
                display_sec = sec
            
            st.markdown(f"**Раздел {display_sec}**")
            
            # Строим HTML-таблицу
            html = '<table class="indicators-table">'
            html += '<thead><tr><th>Показатель</th><th>Значение</th></tr></thead><tbody>'
            
            for ind in inds:
                name = ind.get('name', '').strip()  # убираем \n в начале и конце
                range_val = ind.get('range', '').strip().replace('\r\n', '<br>').replace('\n', '<br>').replace('\r', '<br>')
                html += f'<tr><td>{name}</td><td>{range_val}</td></tr>'
            
            html += '</tbody></table>'
            st.markdown(html, unsafe_allow_html=True)
            st.markdown("---")