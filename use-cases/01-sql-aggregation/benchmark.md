# Benchmark: aggregazioni naive vs ottimizzate

> Stato: **da misurare**. La tabella sotto verrà compilata eseguendo le query
> seguendo [docs/metodologia.md](../../docs/metodologia.md).
> I valori attesi (letteratura e pratica comune) sono un risparmio di 3-10x.

## Setup

| Parametro | Valore |
|---|---|
| Dati | transactions.csv, 10M righe, dati sintetici (seed 42) |
| DBMS | PostgreSQL (da specificare versione) |
| Hardware | da specificare (CPU, TDP, RAM) |
| Data misura | da compilare |

## Risultati

| Query | Tempo (s) | CPU (s) | Energia stimata (Wh) |
|---|---|---|---|
| naive.sql | - | - | - |
| optimized.sql | - | - | - |
| **Risparmio** | - | - | - |

## Note

- Eseguire ogni query 3 volte, riportare la mediana delle ultime 2.
- Per l'energia: `energia (Wh) = tempo_cpu (s) × TDP (W) × utilizzo / 3600`.
