# 과제 1. 주요 Feature 시각화

## 무엇을
`housePricing_reduced.csv`(16피처+target)를 이용해 SalePrice와 주요 변수 간의 분포·관계를 시각화.

## 어떻게
`01_visualize.py` 실행 (`python3 01_visualize.py`)
- pandas로 CSV 로드(`encoding='utf-8-sig'`), `df.info()`/`df.describe()`로 구조 확인
- seaborn/matplotlib으로 그래프 5종 생성 (한글 폰트: NanumGothic)

## 결과 요약
| 파일 | 내용 | 핵심 결과 |
|---|---|---|
| 01_saleprice_hist.png | SalePrice 히스토그램 | 왜도 1.88, 우편향 분포 |
| 02_overallqual_boxplot.png | OverallQual별 박스플롯 | 품질↑ → 가격 중앙값·분산 동반 상승 |
| 03_grlivarea_scatter.png | GrLivArea 산점도+회귀선 | r=0.71, 이상치 2건 존재 |
| 04_neighborhood_bar.png | 지역별 평균가 막대(정렬) | 최고~최저 지역 간 3배 이상 격차 |
| 05_corr_heatmap.png | 수치형 변수 상관 히트맵 | 다중공선성 위험 쌍 4개 육안 확인 (과제 2로 연결) |

상세 해석은 `01_visualize.py` 실행 시 콘솔 출력 참고.
