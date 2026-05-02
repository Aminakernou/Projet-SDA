import time
import csv
import statistics

def benchmark(algo, graph, queries):
    times = []
    extractions = []
    relaxations = []

    for s, t in queries:
        start = time.perf_counter()

        dist, stats = algo(graph, s, t)

        elapsed = time.perf_counter() - start

        times.append(elapsed)
        extractions.append(stats["extractions"])
        relaxations.append(stats["relaxations"])

    result = {
        "avg": statistics.mean(times),
        "p50": statistics.median(times),
        "p95": statistics.quantiles(times, n=100)[94],
        "throughput": len(queries) / sum(times),
        "avg_extractions": statistics.mean(extractions),
        "avg_relaxations": statistics.mean(relaxations)
    }

    return result
