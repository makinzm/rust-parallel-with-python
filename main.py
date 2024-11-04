import logging
import time
import csv
import rust_parallel_with_python as my_project
from parallel import parallel_square_computation

# ロガーの設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def measure_execution_time(func, *args, iterations=100):
    """指定した関数を複数回実行し、各回の実行時間をリストで返す。"""
    execution_times = []
    for _ in range(iterations):
        start_time = time.perf_counter()
        func(*args)
        end_time = time.perf_counter()
        execution_times.append(end_time - start_time)
    return execution_times

if __name__ == "__main__":
    task_sizes = [100, 500, 1000, 5000, 10000]  # タスク数のリスト
    iterations = 100  # 繰り返し回数

    # CSVファイルへの書き込み
    with open('execution_times.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Iteration', 'Python Time (s)', 'Rust Time (s)', 'Task Size (n)'])

        for n in task_sizes:
            logger.info(f"タスク数 {n} での計測を開始します。")

            # Python実装の実行時間計測
            python_times = measure_execution_time(parallel_square_computation, n, iterations=iterations)
            python_avg_time = sum(python_times) / iterations
            logger.info(f"Python実装の平均実行時間 (n={n}): {python_avg_time:.6f} 秒")

            # Rust実装の実行時間計測
            rust_times = measure_execution_time(my_project.parallel_computation, n, iterations=iterations)
            rust_avg_time = sum(rust_times) / iterations
            logger.info(f"Rust実装の平均実行時間 (n={n}): {rust_avg_time:.6f} 秒")

            for i in range(iterations):
                writer.writerow([i + 1, python_times[i], rust_times[i], n])

    logger.info("全ての実行時間の記録が 'execution_times.csv' に保存されました。")

