import logging
import time
import rust_parallel_with_python as my_project
from parallel import parallel_square_computation

# ロガーの設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def measure_execution_time(func, *args, iterations=100):
    """指定した関数を複数回実行し、平均実行時間を計測する。"""
    total_time = 0.0
    for _ in range(iterations):
        start_time = time.perf_counter()
        func(*args)
        end_time = time.perf_counter()
        total_time += (end_time - start_time)
    average_time = total_time / iterations
    return average_time

if __name__ == "__main__":
    n = 1000  # 並列タスクの数
    iterations = 100  # 繰り返し回数

    # Rust実装の実行時間計測
    rust_avg_time = measure_execution_time(my_project.parallel_computation, n, iterations=iterations)
    logger.info(f"Rust実装の平均実行時間: {rust_avg_time:.6f} 秒")

    # Python実装の実行時間計測
    python_avg_time = measure_execution_time(parallel_square_computation, n, iterations=iterations)
    logger.info(f"Python実装の平均実行時間: {python_avg_time:.6f} 秒")

