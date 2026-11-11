"""Generatore di dati sintetici per il caso d'uso 01: aggregazioni SQL.

Produce transactions.csv: 10 milioni di transazioni e-commerce sintetiche.
Deterministico: stesso seed = stessi dati, per benchmark riproducibili.
Uso: python generate_data.py [--rows 10000000] [--seed 42]
"""
import argparse
import random
import time

CATEGORIES = ["electronics", "clothing", "grocery", "home", "books", "sports", "toys", "beauty"]

MONTH_DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def random_timestamp(rng: random.Random) -> str:
    """Timestamp casuale nel 2025, formato 'YYYY-MM-DD HH:MM:SS'."""
    day = rng.randrange(1, 366)
    sec = rng.randrange(0, 86400)
    for month, days in enumerate(MONTH_DAYS, 1):
        if day <= days:
            day_of_month = day
            break
        day -= days
    return (
        f"2025-{month:02d}-{day_of_month:02d} "
        f"{sec // 3600:02d}:{(sec % 3600) // 60:02d}:{sec % 60:02d}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera transazioni sintetiche.")
    parser.add_argument("--rows", type=int, default=10_000_000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", default="transactions.csv")
    parser.add_argument("--chunk", type=int, default=500_000,
                        help="righe per blocco, per limitare l'uso di memoria")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    t0 = time.time()
    with open(args.out, "w") as f:
        f.write("tx_id,ts,customer_id,category,amount\n")
        tx_id = 0
        while tx_id < args.rows:
            n = min(args.chunk, args.rows - tx_id)
            lines = []
            for _ in range(n):
                tx_id += 1
                customer = rng.randrange(1, 1_000_000)
                category = rng.choice(CATEGORIES)
                amount = round(rng.uniform(1.0, 500.0), 2)
                lines.append(f"{tx_id},{random_timestamp(rng)},{customer},{category},{amount}")
            f.write("\n".join(lines) + "\n")
    print(f"Scritte {args.rows} righe in {args.out} ({time.time() - t0:.1f}s)")


if __name__ == "__main__":
    main()
