import homework7
import time


def benchmark(data_chunk):
    a = 2 ** data_chunk
    return "Done"


if __name__ == '__main__':
    start_time = time.process_time()
    pool = homework7.ProcessPool()
    results = pool.map(benchmark,
                       [1000, 1000,1000, 1000,1000, 1000,1000, 1000,1000, 1000,1000, 1000,1000, 1000,1000, 1000,1000, 1000,1000, 1000,1000, 1000,1000, 1000,])
    print("results:", results)
    print("spend time:", time.perf_counter() - start_time)