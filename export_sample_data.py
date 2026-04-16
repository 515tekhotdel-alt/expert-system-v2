"""
Экспорт первых 10 разделов из области ЦТС в CSV.
Запускать только в PyCharm, не в Streamlit!
"""

import pandas as pd
from data_loader import load_laboratories

print("🔄 Загрузка данных лабораторий...")
labs = load_laboratories()

# Берём ЦТС
lab_cts = labs.get("ИЛ ЦТС")
if not lab_cts:
    print("❌ Лаборатория ЦТС не найдена")
    exit()

print(f"📊 Всего разделов в ЦТС: {len(lab_cts.sections)}")

# Берём первые 10 разделов
sample_sections = lab_cts.sections[:30]

# Формируем данные для экспорта
rows = []
for section in sample_sections:
    # Продукции (первые 3)
    products = list(section.products)[:3]
    products_str = ", ".join(products) + ("..." if len(section.products) > 3 else "")

    # Стандарты (первые 3)
    standards = list(section.standards)[:3]
    standards_str = ", ".join(standards) + ("..." if len(section.standards) > 3 else "")

    # ТН ВЭД (первые 3)
    tnved = list(section.tnved_codes)[:3]
    tnved_str = ", ".join(tnved) + ("..." if len(section.tnved_codes) > 3 else "")

    # Показатели (первые 3)
    indicators = section.indicators[:3]
    indicators_str = "; ".join([f"{i.name}: {i.range_value[:30]}..." for i in indicators]) if indicators else ""

    rows.append({
        "Раздел": section.full_id,
        "Источник": section.source,
        "Номер": section.number,
        "Продукции (всего)": len(section.products),
        "Примеры продукции": products_str,
        "Стандарты (всего)": len(section.standards),
        "Примеры стандартов": standards_str,
        "ТН ВЭД (всего)": len(section.tnved_codes),
        "Примеры ТН ВЭД": tnved_str,
        "Показатели (всего)": len(section.indicators),
        "Примеры показателей": indicators_str
    })

# Сохраняем в CSV
df = pd.DataFrame(rows)
filename = "cts_sample_10_sections.csv"
df.to_csv(filename, index=False, encoding='utf-8-sig')

print(f"✅ Экспортировано {len(rows)} разделов в файл: {filename}")
print("\n📋 Первые 5 строк:")
print(df.head().to_string())