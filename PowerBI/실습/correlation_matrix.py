# Power BI Python 시각적 개체(Python visual)용 코드
# 사용법: 시각적 개체에 Profit, Discount, Sales, Shipping Cost 4개 필드를 값(Values)에 드래그한 뒤
#         이 스크립트를 Python 스크립트 편집기에 붙여넣기

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Power BI가 넘겨주는 데이터프레임 이름은 항상 'dataset'
df = dataset[['Profit', 'Discount', 'Sales', 'Shipping Cost']].copy()

# 숫자형 변환 (혹시 텍스트로 들어올 경우 대비)
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')
df = df.dropna()

# 상관계수 행렬 계산
corr = df.corr(method='pearson')

# 히트맵 그리기
plt.figure(figsize=(6, 5))
sns.heatmap(
    corr,
    annot=True,
    fmt='.2f',
    cmap='RdBu_r',
    vmin=-1, vmax=1,
    square=True,
    linewidths=0.5,
    cbar_kws={'label': 'Correlation'}
)
plt.title('Profit / Discount / Sales / Shipping Cost 상관관계 매트릭스')
plt.tight_layout()
plt.show()
