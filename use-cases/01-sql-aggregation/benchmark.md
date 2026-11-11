# Benchmark: aggregazioni naive vs ottimizzate

> Misurato il 2026-11-11 seguendo [docs/metodologia.md](../../docs/metodologia.md).
> Tempo: mediana di 3 esecuzioni (prima scartata come warm-up nel calcolo).
> Energia: sensore RAPL `power/energy-pkg/` via `perf stat -r 2` (media di 2 esecuzioni).

## Setup

| Parametro | Valore |
|---|---|
| Dati | transactions.csv, 10.000.000 righe, dati sintetici (seed 42) |
| DBMS | PostgreSQL 16.15 (Ubuntu 24.04) |
| CPU | AMD Ryzen 7 5825U (8 core / 16 thread, TDP 15 W) |
| RAM | 16 GB |
| Tipo di misura | end-to-end: motore + serializzazione e trasferimento del risultato |

## Risultati

| Query | Tempo mediano (ms) | Energia CPU (J) | Energia (Wh) | Righe restituite |
|---|---|---|---|---|
| naive.sql | 10.138,8 | 858,02 | 0,238 | 10.000.000 |
| optimized.sql | 2.213,8 | 43,97 | 0,0122 | 96 |
| **Risparmio** | **-78% (4,6x)** | **-95% (19,5x)** | **-95%** | **~100.000x meno dati** |

## Lettura dei risultati

Il piano di esecuzione (EXPLAIN ANALYZE) mostra che **a livello di motore** le due query
sono vicine (1.663 ms vs 1.402 ms, entrambe Seq Scan su 10M righe: il filtro seleziona
l'intero anno, quindi l'indice su `ts` non viene usato).

La differenza enorme nasce dal **trasferimento del risultato**: la query naive restituisce
10 milioni di righe che il client deve ricevere e serializzare; l'ottimizzata ne restituisce
96 già aggregate. La misura è end-to-end, volutamente: in una pipeline reale il costo dello
spostamento dei dati è energia consumata esattamente come quella della CPU.

**Il risparmio, dunque, non è (solo) nell'ottimizzatore: è nel non spostare dati inutili.**

## Riproduzione

```bash
psql -d benchmarks -c "\timing on" -f naive.sql -o /dev/null
psql -d benchmarks -c "\timing on" -f optimized.sql -o /dev/null
sudo perf stat -e power/energy-pkg/ -r 2 psql -d benchmarks -f naive.sql -o /dev/null
sudo perf stat -e power/energy-pkg/ -r 2 psql -d benchmarks -f optimized.sql -o /dev/null
```

- Eseguire ogni query 3 volte, riportare la mediana delle ultime 2.
- `perf stat -r 2` ripete l'esecuzione e riporta la media dei Joule.
