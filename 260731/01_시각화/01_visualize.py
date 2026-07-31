import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('../data_prob/housePricing_reduced.csv', encoding='utf-8-sig')

print(df.info())
print(df.describe())
print('SalePrice 왜도:', round(df['SalePrice'].skew(), 2))

# ① SalePrice 히스토그램 + 왜도
skew_val = df['SalePrice'].skew()
plt.figure(figsize=(8, 5))
sns.histplot(df['SalePrice'], kde=True, bins=40, color='steelblue')
plt.axvline(df['SalePrice'].mean(), color='red', linestyle='--', label=f"평균: {df['SalePrice'].mean():,.0f}")
plt.text(0.98, 0.95, f'Skewness = {skew_val:.2f}', transform=plt.gca().transAxes,
         ha='right', va='top', fontsize=11, bbox=dict(boxstyle='round', fc='white', ec='gray'))
plt.title('SalePrice 분포')
plt.xlabel('SalePrice (USD)')
plt.legend()
plt.tight_layout()
plt.savefig('01_saleprice_hist.png', dpi=120)
plt.close()
print('저장: 01_saleprice_hist.png')

# ② OverallQual별 SalePrice 박스플롯
plt.figure(figsize=(9, 5.4))
sns.boxplot(x='OverallQual', y='SalePrice', data=df, hue='OverallQual', palette='Blues', legend=False)
plt.title('전반적 품질(OverallQual)별 SalePrice 분포')
plt.xlabel('OverallQual (1~10)')
plt.ylabel('SalePrice (USD)')
plt.figtext(0.5, 0.005,
            '※ 색 해석: 파란색이 진할수록 품질 등급이 높음 (연한 파랑=저품질 1, 진한 파랑=고품질 10)',
            ha='center', fontsize=9, color='dimgray')
plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.savefig('02_overallqual_boxplot.png', dpi=120)
plt.close()
print('저장: 02_overallqual_boxplot.png')

# ③ GrLivArea vs SalePrice 산점도 + 회귀선
plt.figure(figsize=(8, 5.4))
sns.regplot(x='GrLivArea', y='SalePrice', data=df,
            scatter_kws={'alpha': 0.4, 's': 15, 'label': '개별 주택'},
            line_kws={'color': 'red', 'label': '선형 회귀선(추세)'})
r_val = df['GrLivArea'].corr(df['SalePrice'])
plt.text(0.02, 0.95, f'r = {r_val:.2f}', transform=plt.gca().transAxes,
         fontsize=11, va='top', bbox=dict(boxstyle='round', fc='white', ec='gray'))
plt.title('GrLivArea vs SalePrice')
plt.xlabel('GrLivArea (지상 거주 면적, sq ft)')
plt.ylabel('SalePrice (USD)')
plt.legend(loc='lower right')
plt.figtext(0.5, 0.005,
            '※ 색 해석: 파란 점=주택 1채(진하게 겹칠수록 밀집 구간), 빨간 선=회귀 추세선, 붉은 음영=회귀선의 95% 신뢰구간',
            ha='center', fontsize=9, color='dimgray')
plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.savefig('03_grlivarea_scatter.png', dpi=120)
plt.close()
print('저장: 03_grlivarea_scatter.png')

# ④ Neighborhood별 평균 SalePrice 막대그래프 (값 정렬)
nbhd_mean = df.groupby('Neighborhood')['SalePrice'].mean().sort_values(ascending=False)
plt.figure(figsize=(11, 5.4))
sns.barplot(x=nbhd_mean.index, y=nbhd_mean.values, hue=nbhd_mean.index,
            palette='viridis', legend=False)
plt.xticks(rotation=75)
plt.title('지역(Neighborhood)별 평균 SalePrice')
plt.xlabel('Neighborhood')
plt.ylabel('평균 SalePrice (USD)')
plt.figtext(0.5, 0.005,
            '※ 색 해석: 평균가 순위를 따라 어두운 보라(고가 지역)→노랑(저가 지역)으로 변화 (viridis 팔레트, 막대 높이와 동일 정보)',
            ha='center', fontsize=9, color='dimgray')
plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.savefig('04_neighborhood_bar.png', dpi=120)
plt.close()
print('저장: 04_neighborhood_bar.png')

# ⑤ (선택) 수치형 feature 상관 히트맵
num_df = df.select_dtypes('number').drop(columns=['Id'])
corr = num_df.corr()
plt.figure(figsize=(10, 8.4))
ax = sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                 square=True, linewidths=0.5, annot_kws={'size': 7},
                 cbar_kws={'label': '피어슨 상관계수 r'})
plt.title('수치형 Feature 상관 히트맵')
plt.figtext(0.5, 0.005,
            '※ 색 해석: 빨강=양의 상관(함께 증가), 파랑=음의 상관(반대로 움직임), 색이 진할수록 관계가 강함 (|r|≥0.8 진한 빨강 = 다중공선성 위험)',
            ha='center', fontsize=9, color='dimgray')
plt.tight_layout(rect=[0, 0.02, 1, 1])
plt.savefig('05_corr_heatmap.png', dpi=120)
plt.close()
print('저장: 05_corr_heatmap.png')

# ── 해석 코멘트 ──────────────────────────────────────
print("""
[해석]
① SalePrice는 왜도 1.88의 우편향 분포. 대다수 주택은 10~20만불대에 몰려 있고,
   고가 주택 일부가 긴 꼬리를 형성함 (log 변환 시 정규분포에 가까워질 것으로 예상).
② OverallQual 등급이 오를수록 SalePrice 중앙값·분산이 함께 커지는 단조 증가 패턴.
   품질이 가격을 설명하는 핵심 변수(r=0.79)임을 시각적으로 뒷받침.
③ GrLivArea와 SalePrice는 r=0.71의 뚜렷한 선형 관계. 다만 4500sqft 이상인데
   가격이 낮은 이상치 2건이 존재해 회귀분석 시 별도 처리가 필요해 보임.
④ Neighborhood별 평균가는 최고(NoRidge 등 30만불대)와 최저(MeadowV 등 10만불대)
   사이 3배 이상 격차. 지역이 가격에 미치는 영향이 매우 큼.
⑤ 상관 히트맵에서 GarageCars-GarageArea(0.88), TotRmsAbvGrd-GrLivArea(0.83),
   TotalBsmtSF-1stFlrSF(0.82) 등이 강하게 상관되어 다중공선성 위험 쌍으로 확인됨
   → 과제 2에서 VIF로 정량 검증 예정.
""")
