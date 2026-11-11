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

Vedi  per le misure. Il risparmio atteso su questo pattern è tipicamente **3-10x** in tempo e CPU, con riduzione proporzionale dell'energia.

## Riproduzione

```bash
# 1. genera i dati (richiede Python 3.8+, nessuna libreria esterna)
python generate_data.py            # crea transactions.csv (~10M righe)

# 2. carica su PostgreSQL
psql -c "CREATE TABLE transactions (tx_id BIGINT, ts TIMESTAMP, customer_id BIGINT, category TEXT, amount NUMERIC(10,2));"
psql -c "\copy transactions FROM 'transactions.csv' WITH (FORMAT csv)"

# 3. misura
psql -c "\timing on" -f naive.sql
psql -c "\timing on" -f optimized.sql
```
