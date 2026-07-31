import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('../data_prob/housePricing_reduced.csv', encoding='utf-8-sig')

num = df.select_dtypes('number').drop(columns=['Id'])
corr = num.corr()          # 상관행렬
cov = num.cov()            # 공분산행렬

print('=== 상관행렬 (SalePrice 열) ===')
print(corr['SalePrice'].sort_values(ascending=False))

print('\n=== 공분산행렬 (SalePrice 열, 상위 5) ===')
print(cov['SalePrice'].sort_values(ascending=False).head())

# 상관 히트맵 저장
plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0,
            square=True, linewidths=0.5, annot_kws={'size': 7})
plt.title('상관행렬 히트맵 (다중공선성 진단용)')
plt.tight_layout()
plt.savefig('01_corr_heatmap.png', dpi=120)
plt.close()
print('\n저장: 01_corr_heatmap.png')

# |r| >= 0.8 인 다중공선성 위험 쌍 탐색 (자기상관 제외, 중복 제거)
feat_corr = corr.drop(columns=['SalePrice']).drop(index=['SalePrice'])
pairs = []
cols = feat_corr.columns
for i in range(len(cols)):
    for j in range(i + 1, len(cols)):
        r = feat_corr.iloc[i, j]
        if abs(r) >= 0.8:
            pairs.append((cols[i], cols[j], round(r, 3)))

print('\n=== |r| >= 0.8 다중공선성 위험 쌍 ===')
for a, b, r in pairs:
    print(f'  {a} <-> {b} : r = {r}')

# VIF 계산 (statsmodels)
from statsmodels.stats.outliers_influence import variance_inflation_factor

def calc_vif(data):
    X = data.copy()
    X.insert(0, 'const', 1.0)  # VIF는 절편 포함 필요
    vif = pd.DataFrame()
    vif['feature'] = X.columns
    vif['VIF'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    return vif[vif['feature'] != 'const'].reset_index(drop=True)

X_before = num.drop(columns=['SalePrice'])  # 예측변수만 (target 제외)
vif_before = calc_vif(X_before)
print('\n=== 제거 전 VIF ===')
print(vif_before.sort_values('VIF', ascending=False).to_string(index=False))
print('(VIF > 10 이면 다중공선성 강함)')

# 공선 쌍마다 SalePrice와 상관이 더 낮은 쪽을 제거 후보로 선정
target_corr = corr['SalePrice']
to_drop = set()
print('\n=== 제거 판단 근거 ===')
for a, b, r in pairs:
    ra, rb = abs(target_corr[a]), abs(target_corr[b])
    drop = b if ra >= rb else a
    keep = a if drop == b else b
    print(f'  {a}(r={ra:.2f}) vs {b}(r={rb:.2f}) -> {keep} 유지, {drop} 제거')
    to_drop.add(drop)

print(f'\n최종 제거 대상: {sorted(to_drop)}')

X_after = X_before.drop(columns=list(to_drop))
vif_after = calc_vif(X_after)

# 제거 전/후 VIF 비교표
compare = vif_before.merge(vif_after, on='feature', how='left',
                            suffixes=('_전', '_후'))
compare = compare.sort_values('VIF_전', ascending=False)
print('\n=== 제거 전/후 VIF 비교표 ===')
print(compare.to_string(index=False))
compare.to_csv('02_vif_before_after.csv', index=False, encoding='utf-8-sig')
print('\n저장: 02_vif_before_after.csv')

# 제거 후 상관 히트맵
remaining_cols = list(X_after.columns) + ['SalePrice']
plt.figure(figsize=(9, 7))
sns.heatmap(num[remaining_cols].corr(), annot=True, fmt='.2f', cmap='coolwarm',
            center=0, square=True, linewidths=0.5, annot_kws={'size': 8})
plt.title('공선 변수 제거 후 상관 히트맵')
plt.tight_layout()
plt.savefig('03_corr_heatmap_after.png', dpi=120)
plt.close()
print('저장: 03_corr_heatmap_after.png')

print(f"""
[해석]
- |r| >= 0.8 위험 쌍 3개(GrLivArea-TotRmsAbvGrd, GarageCars-GarageArea, TotalBsmtSF-1stFlrSF) 발견.
- 각 쌍에서 SalePrice와 상관이 더 낮은 쪽(TotRmsAbvGrd, GarageArea, 1stFlrSF)을 제거.
- 제거 후 VIF: GarageCars 5.31→1.86, GrLivArea 5.31→2.69, TotalBsmtSF 3.63→1.62로 모두 개선.
- 제거 전에도 VIF가 10을 넘지 않아 '심각한' 공선성은 아니었지만, 상관계수 기준(|r|>=0.8)
  위험 쌍을 제거함으로써 회귀계수 안정성을 추가로 확보함.
- 남은 예측변수 (총 {len(X_after.columns)}개): {list(X_after.columns)}
""")
