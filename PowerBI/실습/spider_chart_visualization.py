import matplotlib.pyplot as plt
import numpy as np

# 1. Power BI 데이터 수집 및 Market별 Sales 평균 계산
data = dataset.dropna(subset=['Market', 'Sales'])
df_grouped = data.groupby('Market')['Sales'].mean().reset_index()

labels = df_grouped['Market'].tolist()
stats = df_grouped['Sales'].tolist()

# 2. 방사형 차트를 위해 시작점과 끝점 연결 (원형 다각형 닫기)
num_vars = len(labels)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

stats += stats[:1]
angles += angles[:1]
labels_closed = labels + [labels[0]]

# 3. 방사형 차트 그리기 (Polar projection)
fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))

# 배경 그리드 설정 및 시작 방향(Top) 조정
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)

# X축 레이블(Market) 및 위치 설정
plt.xticks(angles[:-1], labels, color='#333333', size=11, fontweight='bold')

# Y축(Sales 평균값) 레이블 설정 및 위치 지정
ax.set_rlabel_position(0)
plt.yticks(color="grey", size=9)

# 데이터 라인 및 채우기 색상 지정
ax.plot(angles, stats, color='#1f77b4', linewidth=2, linestyle='solid')
ax.fill(angles, stats, color='#1f77b4', alpha=0.25)

# 차트 제목 설정
plt.title('Average Sales by Market', size=15, color='#222222', weight='bold', y=1.1)

# 데이터 값 표시 (각 축 지점에 숫자로 평균 Sales 표시)
for angle, stat, label in zip(angles[:-1], stats[:-1], labels):
    # 값 위치를 살짝 외곽으로 조정
    ax.text(angle, stat * 1.05, f"{stat:,.1f}", 
            horizontalalignment='center', size=9, color='#1f77b4', weight='bold')

plt.tight_layout()
plt.show()