import matplotlib.pyplot as plt
import seaborn as sns

# Power BI는 선택한 필드를 'dataset'이라는 pandas DataFrame으로 자동 생성합니다.
# 수치 데이터 중 결측치나 중복 제거를 원할 경우를 대비한 기본 전처리
data = dataset.dropna(subset=['Category', 'Sales', 'Discount', 'Profit', 'Quantity', 'Shipping Cost'])

# seaborn 스타일 설정
sns.set_theme(style="whitegrid", font_scale=0.9)

# 2행 3열 그리드 생성
fig, axes = plt.subplots(2, 3, figsize=(14, 8))
fig.suptitle('Distribution of Metrics by Category', fontsize=16, fontweight='bold', y=0.98)

# 비교할 지표 리스트
metrics = ['Sales', 'Discount', 'Profit', 'Quantity', 'Shipping Cost']
palette = 'Set2' # 색상 테마

# 각 지표별로 Boxplot 생성
for idx, metric in enumerate(metrics):
    row = idx // 3
    col = idx % 3
    ax = axes[row, col]
    
    sns.boxplot(
        data=data, 
        x='Category', 
        y=metric, 
        ax=ax, 
        palette=palette,
        fliersize=2  # 이상치(outlier) 점 크기 조정
    )
    
    ax.set_title(metric, fontsize=12, fontweight='bold')
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.tick_params(axis='x', rotation=15) # X축 카테고리 라벨 살짝 회전

# 6번째 빈 그래프(2행 3열 중 마지막) 숨기기
fig.delaxes(axes[1, 2])

# 레이아웃 정돈 및 출력
plt.tight_layout()
plt.show()