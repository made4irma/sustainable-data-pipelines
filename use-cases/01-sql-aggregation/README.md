# Caso d'uso 01: aggregazioni SQL

## Lo scenario

Una tabella di transazioni di e-commerce (dati sintetici): 10 milioni di righe. La pipeline giornaliera calcola il fatturato per categoria e mese.

## Il problema

La versione **naive** introduce tre sprechi classici:

1. `SELECT *` dove bastano 3 colonne: più I/O, più memoria, meno uso degli indici.
2. `ORDER BY` inutile in una pipeline intermedia: il risultato viene comunque riordinato a valle.
3. Funzioni applicate alla colonna nel `WHERE` (`DATE_TRUNC` su ogni riga) che impediscono l'uso di indici e pre-aggregazioni.

## La strategia di ottimizzazione

1. Proiettare **solo le colonne necessarie**.
2. Eliminare ordinamenti non richiesti dal consumatore finale.
3. **Pre-aggregare** con una tabella riepilogo (o vista materializzata): le query a valle leggono migliaia di righe invece di milioni.
4. Filtrare il prima possibile (predicate pushdown manuale).

## Risultati

Vedi [benchmark](benchmark.md) per le misure. Il risparmio atteso su questo pattern è tipicamente 3-10x in tempo e CPU, con riduzione proporzionale dell'energia.

## Riproduzione

```bash
# 1. genera i dati (richiede Python 3.8+, nessuna libreria esterna)
python generate_data.py            # crea transactions.csv (~10M righe)

# 2. crea il database e carica i dati su PostgreSQL
createdb benchmarks
psql -d benchmarks -c "CREATE TABLE transactions (tx_id BIGINT, ts TIMESTAMP, customer_id BIGINT, category TEXT, amount NUMERIC(10,2));"
psql -d benchmarks -c "\copy transactions FROM 'transactions.csv' WITH (FORMAT csv, HEADER true)"

# 3. crea l'indice e aggiorna le statistiche
psql -d benchmarks -c "CREATE INDEX idx_transactions_ts ON transactions (ts);"
psql -d benchmarks -c "ANALYZE transactions;"

# 4. misura (vedi docs/metodologia.md: mediana di 3 esecuzioni)
psql -d benchmarks -c "\timing on" -f naive.sql -o /dev/null
psql -d benchmarks -c "\timing on" -f optimized.sql -o /dev/null
```
