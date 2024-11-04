import rust_parallel_with_python as my_project
from parallel import parallel_square_computation

# 10個の並列タスクを実行
rust_result = my_project.parallel_computation(100)
print(rust_result)

python_result = parallel_square_computation(100)
print(python_result)
