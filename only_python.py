import time
import csv
import concurrent.futures
import multiprocessing
import numpy as np

# Task sizes
task_sizes = [100, 500, 1000, 5000, 10000]
iterations = 100

# Function to calculate square of each number
def calculate_squares(n):
    return [i ** 2 for i in range(n)]

# Function to measure execution time for each method
def measure_execution_time(func, *args, iterations=100):
    execution_times = []
    for _ in range(iterations):
        start_time = time.perf_counter()
        func(*args)
        end_time = time.perf_counter()
        execution_times.append(end_time - start_time)
    return execution_times

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

# CSV writing
with open('only_python_execution_times.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Iteration', 'Method', 'Execution Time (s)', 'Task Size (n)'])

    for n in task_sizes:
        # Measure and record execution time for each method
        # Sequential
        sequential_times = measure_execution_time(sequential_approach, n, iterations=iterations)
        for i in range(iterations):
            writer.writerow([i + 1, 'Sequential', sequential_times[i], n])

        # ThreadPoolExecutor
        threadpool_times = measure_execution_time(threadpool_approach, n, iterations=iterations)
        for i in range(iterations):
            writer.writerow([i + 1, 'ThreadPoolExecutor', threadpool_times[i], n])

        # Multiprocessing
        multiprocessing_times = measure_execution_time(multiprocessing_approach, n, iterations=iterations)
        for i in range(iterations):
            writer.writerow([i + 1, 'Multiprocessing', multiprocessing_times[i], n])

