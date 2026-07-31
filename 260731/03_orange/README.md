# 과제 3. Orange 회귀모델 개발 (4가지 알고리즘 비교)

## 무엇을
노코드 도구 Orange로 주택가격(SalePrice) 회귀 파이프라인을 구성하고,
4가지 알고리즘의 성능을 5-fold 교차검증으로 비교. 과제 2의 다중공선성 제거 결과를 입력 변수 선정에 반영.

## 어떻게 (워크플로우 구성)
워크플로우 파일: `../pred_houseprice.ows`

```
File(reduced) → Select Columns → Preprocess(Normalize) ─┬→ Test and Score (5-fold CV, 모델 비교)
                                                        └→ Data Sampler ─(80%)→ 모델 4종 학습
                                                                         ─(20% Remaining)→ Predictions → 모델별 Scatter Plot 4종
```

- **File**: `housePricing_reduced.csv` (16 feature + SalePrice), SalePrice를 target으로 지정
- **Select Columns**: 과제 2에서 제거 결정한 공선 변수 3개(`GarageArea`, `TotRmsAbvGrd`, `1stFlrSF`)를 Ignored로 이동
- **Preprocess**: Normalize Features(표준화) — 거리 기반 모델(kNN)의 스케일 민감성 대응
- **Test and Score**: 전처리된 전체 데이터(1460행)로 5-fold Cross Validation
- **Data Sampler**: 80/20 분할 — 80%로 모델 학습, 20%(Remaining Data)는 학습에 쓰지 않고
  Predictions에 공급해 홀드아웃 방식의 실제값 vs 예측값 시각화에 사용
- **모델 4종**: Linear Regression, AdaBoost, Gradient Boosting, kNN

## 결과 (Test & Score, 5-fold CV)

| 모델 | R² (Normalize 적용) | R² (Discretize, 참고) |
|---|---|---|
| **Gradient Boosting** | **0.840** | 0.864 |
| kNN | 0.823 | 0.816 |
| AdaBoost | 0.811 | 0.836 |
| Linear Regression | 0.803 | 0.830 |

**전처리 비교 실험**: Discretize(5구간 이산화) → Normalize(표준화)로 교체 시,
거리 기반인 kNN만 성능이 상승(0.816→0.823)하고 트리·선형 계열은 하락.
트리 계열의 하락은 Normalize의 악영향이 아니라, 이산화가 제공하던
스무딩(잡음 제거) 효과가 사라진 결과로 해석됨. 어느 구성에서도 **최고 모델은
Gradient Boosting으로 동일**.

## 최고 성능 모델 선정 근거
**Gradient Boosting** — ① R² 0.840으로 4개 모델 중 최고, RMSE·MAE도 최소.
② 모델 간 쌍대 비교표(Compare models by MSE)에서 모든 상대 모델에 대해
우위 확률 90% 이상. ③ 실제값 vs 예측값 산점도에서 대각선(y=x) 주변 산포가
가장 작아 수치 지표와 시각적 판독이 일치.

## 산출물
- `회귀모델_전체_프로세스_캔버스.png`: 워크플로우 전체 캔버스 캡처
- `회귀모델_test&score_결과표.png`: 전처리 전/후 R² 비교표
- `모델비교_scatter.html`: 모델 4종의 실제값 vs 예측값 산점도 (Orange 리포트)
- `../pred_houseprice.ows`: 완성 워크플로우 파일
