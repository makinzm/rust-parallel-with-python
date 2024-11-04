import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns

# CSVファイルをpolarsで読み込む
df = pl.read_csv('execution_times.csv')

# タスクサイズごとにデータをグループ化
task_sizes = df['Task Size (n)'].unique().to_list()

# グラフの設定
sns.set(style="whitegrid")
fig, axes = plt.subplots(len(task_sizes), 1, figsize=(10, 6 * len(task_sizes)), sharex=True)

# 各タスクサイズごとにプロット
for i, n in enumerate(task_sizes):
    ax = axes[i]
    subset = df.filter(pl.col('Task Size (n)') == n)
    
    # ヒストグラムのプロット
    sns.histplot(subset['Python Time (s)'], bins=30, color='blue', alpha=0.5, label='Python', ax=ax)
    sns.histplot(subset['Rust Time (s)'], bins=30, color='orange', alpha=0.5, label='Rust', ax=ax)
    
    # 平均実行時間の計算
    python_mean = subset['Python Time (s)'].mean()
    rust_mean = subset['Rust Time (s)'].mean()
    
    # 平均実行時間の線を追加
    ax.axvline(python_mean, color='blue', linestyle='--', label=f'Python Mean: {python_mean:.4f}s')
    ax.axvline(rust_mean, color='orange', linestyle='--', label=f'Rust Mean: {rust_mean:.4f}s')
    
    # グラフの設定
    ax.set_title(f'Task Size (n) = {n}')
    ax.set_xlabel('Execution Time (s)')
    ax.set_ylabel('Frequency')
    ax.legend()

# 全体の設定
plt.tight_layout()
plt.savefig('execution_times_histograms.png')
plt.show()

