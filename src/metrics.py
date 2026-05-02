import csv


def save_results(results, filename):
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=results.keys()
        )
        writer.writeheader()
        writer.writerow(results)