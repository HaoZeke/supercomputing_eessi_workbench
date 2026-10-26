"""One deterministic pi estimate. SAMPLE_COUNT sets the length."""

import os


def estimate(n: int, seed: int = 1) -> tuple[int, float]:
    x = seed
    hits = 0
    for _ in range(n):
        x = (1103515245 * x + 12345) % (2**31)
        a = x / 2**31
        x = (1103515245 * x + 12345) % (2**31)
        b = x / 2**31
        if a * a + b * b <= 1.0:
            hits += 1
    return hits, 4 * hits / n


def main() -> None:
    n = int(os.environ.get("SAMPLE_COUNT", "1000"))
    hits, est = estimate(n)
    print(f"samples={n} hits={hits} estimate={est:.4f}")


if __name__ == "__main__":
    main()
