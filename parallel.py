import concurrent.futures

# Pythonで並列に指定された長さの2乗を計算する関数
def parallel_square_computation(n):
    def compute_square(i):
        return i * i

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # スレッドプールを使用して並列に計算を行う
        results = list(executor.map(compute_square, range(n)))
    
    return results

