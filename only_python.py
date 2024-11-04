import time
import concurrent.futures
import multiprocessing
import numpy as np
import pandas as pd

# Task sizes
task_sizes = [100, 500, 1000, 5000, 10000]
iterations = 100

# Function to calculate square of each number
def calculate_squares(n):
    return [i ** 2 for i in range(n)]

# Function to calculate mean and variance
def calculate_mean_and_variance(results):
    mean = np.mean(results)
    variance = np.var(results)
    return mean, variance

# Sequential approach (no parallelism)
def sequential_approach(n):
    return [calculate_squares(n) for _ in range(iterations)]

# ThreadPoolExecutor approach
def threadpool_approach(n):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(calculate_squares, n) for _ in range(iterations)]
        return [future.result() for future in concurrent.futures.as_completed(futures)]

# Multiprocessing approach
def multiprocessing_approach(n):
    with multiprocessing.Pool() as pool:
        return pool.map(calculate_squares, [n] * iterations)

# Collect results in a DataFrame
results = []

# Run tests for each method and task size
for n in task_sizes:
    # Sequential (no parallelism)
    start_time = time.time()
    sequential_results = sequential_approach(n)
    duration = time.time() - start_time
    mean, variance = calculate_mean_and_variance(sequential_results)
    results.append(["Sequential", n, mean, variance, duration])
    
    # ThreadPoolExecutor
    start_time = time.time()
    threadpool_results = threadpool_approach(n)
    duration = time.time() - start_time
    mean, variance = calculate_mean_and_variance(threadpool_results)
    results.append(["ThreadPoolExecutor", n, mean, variance, duration])
    
    # Multiprocessing
    start_time = time.time()
    multiprocessing_results = multiprocessing_approach(n)
    duration = time.time() - start_time
    mean, variance = calculate_mean_and_variance(multiprocessing_results)
    results.append(["Multiprocessing", n, mean, variance, duration])

# Convert results to DataFrame and save as CSV
df = pd.DataFrame(results, columns=["Method", "Task Size (n)", "Mean", "Variance", "Execution Time (s)"])
df.to_csv("only_python_execution_times.csv", index=False)


