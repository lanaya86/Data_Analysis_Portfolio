# generate_data.py
# Скрипт для генерации агрегированных ежедневных данных за полгода по 30 странам NA/EU и вариантам A/B

import pandas as pd
import numpy as np
import os
import uuid
from datetime import date, timedelta

# Папка для сохранения результатов
BASEDIR = os.path.dirname(__file__)
OUTPUT_FILE = os.path.join(BASEDIR, 'ad_performance_test_aggregated.csv')

# Параметры генерации
END_DATE = date(2025, 6, 20)
NUM_DAYS = 180  # последние полгода
START_DATE = END_DATE - timedelta(days=NUM_DAYS - 1)
VARIATIONS = ['A', 'B']

# Список из 30 стран NA/EU
COUNTRIES = [
    'US', 'CA', 'MX',  # North America
    'DE', 'FR', 'UK', 'IT', 'ES', 'NL', 'BE', 'AT', 'CH', 'SE', 'NO', 'DK',
    'FI', 'IE', 'PT', 'GR', 'PL', 'CZ', 'HU', 'SK', 'SI', 'HR', 'RO', 'BG',
    'EE', 'LV', 'LT'   # European Union + UK
]

# Словари для моделирования показателей
# Средние показы по странам (варьируются для реалистичности)
np.random.seed(42)
geo_means = {country: np.random.randint(500, 2000) for country in COUNTRIES}
# CTR для вариантов A/B
ctr = {'A': 0.05, 'B': 0.06}

# Генерация списка дат
dates = [START_DATE + timedelta(days=i) for i in range(NUM_DAYS)]

# Собираем строки: каждая комбинация date × geo × variation
rows = []
for d in dates:
    for country in COUNTRIES:
        for var in VARIATIONS:
            # Импрессии и клики
            imps = np.random.poisson(lam=geo_means[country])
            clicks = np.random.binomial(n=imps, p=ctr[var])
            # Расход (spend) через CPM
            cpm = np.random.uniform(2.0, 5.0)
            spend = imps * cpm / 1000
            # Прибыль с шумом
            revenue_per_click = {'A': 2.5, 'B': 3.0}[var]
            profit = clicks * revenue_per_click - spend + np.random.normal(0, 5)
            # Добавляем строку
            rows.append({
                'id': str(uuid.uuid4()),               
                'datetime': d,                         
                'variation': var,                     
                'spend': round(spend, 2),             
                'geo': country,                        
                'impressions': int(imps),               
                'clicks': int(clicks),                  
                'profit': round(profit, 2)             
            })

# Создание DataFrame и явное приведение типов
df = pd.DataFrame(rows)
df['impressions'] = df['impressions'].astype('int64')
df['clicks'] = df['clicks'].astype('int64')
df['spend'] = df['spend'].astype('float64')
df['profit'] = df['profit'].astype('float64')

# Сохраняем в CSV без индекса
df.to_csv(OUTPUT_FILE, index=False)
print(f"Сгенерировано {len(df)} строк и сохранено: {OUTPUT_FILE}")
