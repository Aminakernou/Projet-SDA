from src.generator import generate_grid, generate_queries
from src.dijkstra import dijkstra
from src.benchmark import benchmark
from src.metrics import save_results
from src.ch import ContractionHierarchies

def ch_wrapper(ch, s, t):
    return ch.query(s, t)


def main():

    graph = generate_grid(
        rows=50,
        cols=50,
        seed=42
    )

    queries = generate_queries(
        graph,
        nb=100,
        seed=42
    )

    print("Benchmark Dijkstra...")
    dijkstra_results = benchmark(
        dijkstra,
        graph,
        queries
    )

    save_results(
        dijkstra_results,
        "dijkstra_results.csv"
    )

    print(dijkstra_results)

    print("Preprocessing CH...")
    ch = ContractionHierarchies(graph)
    ch.preprocess()

    for s, t in queries[:10]:
        d1, _ = dijkstra(graph, s, t)
        d2, _ = ch.query(s, t)

        print(
            "check:",
            d1[t],
            d2[t]
        )
    
    print("Benchmark CH...")
    ch_results = benchmark(
        lambda g, s, t: ch_wrapper(ch, s, t),
        graph,
        queries
    )

    save_results(
        ch_results,
        "ch_results.csv"
    )
    

    print(ch_results)


if __name__ == "__main__":
    main()