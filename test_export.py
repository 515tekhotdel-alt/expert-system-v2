import streamlit as st
import pandas as pd
import io
from datetime import datetime
import base64

st.title("Тест экспорта (автоскачивание)")

# Тестовые данные
if st.button("Создать тестовые данные"):
    st.session_state.test_data = [
        {'Стандарт': 'ГОСТ 123', 'Раздел': 'ч1_3', 'Показатель': 'Масса', 'Значение': 'от 1 до 10'},
        {'Стандарт': 'ГОСТ 123', 'Раздел': 'ч1_3', 'Показатель': 'Объём', 'Значение': 'от 5 до 15'},
    ]
    st.success("Тестовые данные созданы")

if st.button("💾 Экспорт"):
    if 'test_data' in st.session_state:
        output = io.BytesIO()
        
        all_rows = []
        all_rows.append({'Раздел': 'ТЕСТ', 'Параметр': 'Лаборатория', 'Значение': 'ИЛ ЦТС'})
        all_rows.append({'Раздел': '', 'Параметр': '', 'Значение': ''})
        
        for row in st.session_state.test_data:
            all_rows.append({
                'Раздел': '',
                'Параметр': row['Стандарт'],
                'Значение': f"[{row['Раздел']}] {row['Показатель']}: {row['Значение']}"
            })
        
        df = pd.DataFrame(all_rows)
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Отчёт', index=False)
            worksheet = writer.sheets['Отчёт']
            worksheet.column_dimensions['A'].width = 30
            worksheet.column_dimensions['B'].width = 40
            worksheet.column_dimensions['C'].width = 50
        
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        
        # Автоматическое скачивание через JavaScript
        js = f"""
        <script>
            var link = document.createElement('a');
            link.download = 'test_{datetime.now().strftime("%H%M%S")}.xlsx';
            link.href = 'data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        </script>
        """
        st.components.v1.html(js, height=0)
        st.success("✅ Файл скачивается...")
    else:
        st.warning("Сначала создайте тестовые данные")