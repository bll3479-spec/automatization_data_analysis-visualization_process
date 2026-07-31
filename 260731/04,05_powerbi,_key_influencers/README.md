# 과제 4·5. Power BI 시각 개체 5종 + 주요 영향 요인 (Key Influencers)

## 무엇을
`housePricing_reduced.csv`를 Power BI Desktop에 적재하여
① 대표 시각 개체 5종으로 보고서 페이지를 구성하고(과제 4),
② DAX 계산 열로 SalePrice를 High/Low 등급화한 뒤 Key Influencers 시각 개체로
고가 주택을 만드는 핵심 요인을 정량 도출(과제 5).

## 어떻게
- 데이터: 텍스트/CSV 가져오기로 `housePricing_reduced.csv` 로드 (1,460행)
- 과제 5용 계산 열 (테이블 도구 → 새 열, 중앙값 기준 High/Low):

```dax
SalePrice_등급 =
IF ( 'housePricing_reduced'[SalePrice]
      >= MEDIANX ( ALL ( 'housePricing_reduced' ), 'housePricing_reduced'[SalePrice] ),
    "High", "Low" )
```

## 과제 4 — 시각 개체 5종 (각 1줄 설명)

캡처: `슬라이서_적용_전.png` (기본 상태), `슬라이서_적용_후.png` (OverallQual 6~10 필터)

| # | 시각 개체 | 구성 | 설명 |
|---|---|---|---|
| ① | 카드 ×2 | 평균 SalePrice / Id 개수 | 핵심 KPI 요약 — 평균가 180.92천 USD, 주택 수 1,460채 (과제 1의 pandas 결과와 일치함을 교차 검증) |
| ② | 묶은 세로 막대 | Neighborhood별 평균 SalePrice, 내림차순 | 지역별 가격 격차 확인 — NoRidge(약 33만$)부터 하위 지역(약 10만$)까지 3배 이상 차이 |
| ③ | 분산형 차트 | X=GrLivArea, Y=SalePrice, 색=OverallQual, 세부정보=Id | 면적-가격의 양의 상관 + 같은 면적에서도 품질(색)이 높을수록 가격이 높음 |
| ④ | 꺾은선형 차트 | X=YearBuilt, Y=평균 SalePrice | 최근 건축일수록 평균가 상승 추세. 1900년 이전 구간은 표본이 적어 평균이 크게 출렁임(소표본 주의) |
| ⑤ | 슬라이서 | OverallQual 범위(1~10) | 조작 시 페이지 전체가 연동(교차 필터링) — 6~10 선택 시 평균가 180.92천→213.18천, 주택 수 1,460→922로 갱신됨을 전/후 캡처로 확인 |

## 과제 5 — Key Influencers: "SalePrice_등급 = High"를 만드는 요인

분석 대상 = `SalePrice_등급`(High), 설명 기준 = OverallQual·GrLivArea·Neighborhood·
ExterQual·KitchenQual·GarageCars·TotalBsmtSF·YearBuilt·CentralAir

**상위 영향 요인 3가지와 해석** (캡처: `key_influencers_1st~3rd_*.png`)

| 순위 | 요인 | 영향 | 해석 |
|---|---|---|---|
| 1 | **CentralAir = Y** | High 확률 **×7.21** | 중앙냉방 있는 집의 High 비율 ~53% vs 없는 집 ~7%. 다만 대부분의 주택이 이미 냉방을 갖추고 있어, "냉방 없음 → 거의 확실히 저가"라는 소수 집단에 대한 강한 신호에 가까움 |
| 2 | **GrLivArea +525.3sqft** | High 확률 **×5.59** | 거주 면적이 커질수록 High 확률이 연속적으로 상승 — 전 주택에 보편적으로 작동하는 요인 |
| 3 | **OverallQual +1.38** | High 확률 **×3.42** | 품질 등급 상승 시 High 확률 급등. 상세 차트에서 7등급 전후로 High 비율이 가파르게 오르는 임계 구간 확인 |

이하 KitchenQual=Gd(×2.60), GarageCars↑(×2.13), Neighborhood=NridgHt/StoneBr(×2.08/×2.03) 순.

**과제 1·2·3과의 정합성**: 면적(GrLivArea)·품질(OverallQual)이 최상위권 — 상관분석(r=0.71/0.79),
회귀모델의 결과와 세 가지 방법이 같은 결론으로 수렴. CentralAir가 배수 기준 1위인 것은
이진 변수의 비대칭 분포에서 오는 효과로, "배수가 가장 크다 ≠ 가장 보편적인 요인"이라는
Key Influencers 해석 시 유의점을 보여줌.

## 산출물
- `주택가격_시각화.pbix`: Power BI 보고서 파일 (시각 개체 5종 + SalePrice_등급 계산 열 + Key Influencers)
- `슬라이서_적용_전.png` / `슬라이서_적용_후.png`: 과제 4 보고서 페이지 및 슬라이서 상호작용 증빙
- `key_influencers_1st_CentralAir.png` / `2nd_GrLivArea.png` / `3rd_OverallQual.png`: 상위 요인 3종 상세 캡처
