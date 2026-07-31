# 과제 2. 공분산 · 다중공선성 진단과 제거

## 무엇을
`housePricing_reduced.csv`의 수치형 예측변수 12개(Id, SalePrice 제외)를 대상으로
상관행렬·공분산행렬 산출 → |r|≥0.8 위험 쌍 탐색 → VIF 계산 → 공선 변수 제거 → 개선 확인.

## 어떻게
`02_multicollinearity.py` 실행 (`python3 02_multicollinearity.py`)
- `df.corr()` / `df.cov()`로 상관·공분산행렬 산출, 히트맵 시각화
- 상관행렬에서 |r|≥0.8인 변수 쌍을 전수 탐색
- `statsmodels.variance_inflation_factor`로 VIF 계산
- 각 위험 쌍에서 SalePrice와 상관이 더 낮은 변수를 자동 판별해 제거
- 제거 전/후 VIF를 비교표로 산출

## 결과 요약

**|r| ≥ 0.8 위험 쌍 3개**
| 쌍 | r |
|---|---|
| GarageCars ↔ GarageArea | 0.88 |
| GrLivArea ↔ TotRmsAbvGrd | 0.83 |
| TotalBsmtSF ↔ 1stFlrSF | 0.82 |

**제거 판단**: 각 쌍에서 SalePrice와의 상관이 더 낮은 변수 제거
→ 제거: `GarageArea`, `TotRmsAbvGrd`, `1stFlrSF`

**VIF 개선 (제거 전 → 후)**
| feature | VIF 전 | VIF 후 |
|---|---|---|
| GarageCars | 5.31 | 1.86 |
| GrLivArea | 5.31 | 2.69 |
| TotalBsmtSF | 3.63 | 1.62 |

(제거 전에도 모든 VIF가 10 미만이라 "심각한" 공선성은 아니었지만, 상관 기준 위험 쌍을 제거해
회귀계수 안정성을 추가로 확보함.)

**최종 남은 예측변수 (9개)**
`OverallQual, GrLivArea, GarageCars, TotalBsmtSF, FullBath, YearBuilt, YearRemodAdd, Fireplaces, LotArea`
(+ 범주형 Neighborhood, ExterQual, KitchenQual, CentralAir는 별도 유지, + target SalePrice)

→ 이 목록이 과제 3(Orange 회귀모델)의 Select Columns 입력으로 그대로 사용됨.

## 산출물
- `01_corr_heatmap.png`: 제거 전 상관 히트맵
- `02_vif_before_after.csv`: VIF 제거 전/후 비교표
- `03_corr_heatmap_after.png`: 제거 후 상관 히트맵
