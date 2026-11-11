# Metodologia di misurazione

## Cosa misuriamo

Per ogni query riportiamo tre metriche:

| Metrica | Strumento | Unità |
|---|---|---|
| Tempo di esecuzione | `EXPLAIN ANALYZE` o cronometro del client | secondi |
| Tempo CPU | `time` / viste di sistema del DBMS | CPU-secondi |
| Energia stimata | tempo CPU × TDP del processore, oppure RAPL/CodeCarbon | Joule o Wh |

## Stima dell'energia

Il metodo più semplice e riproducibile:

```
energia (J) = tempo_cpu (s) × TDP (W) × fattore_di_utilizzo
```

- **TDP**: Thermal Design Power del processore (es. 65 W per un desktop moderno, ~250 W per un server). È un limite, non un consumo reale: il fattore di utilizzo (tipicamente 0.5-0.8 per query CPU-bound) lo corregge.
- Per misure più accurate su Linux: **RAPL** via `perf stat -e power/energy-pkg/`, o la libreria Python **CodeCarbon** (`pip install codecarbon`), che stima anche le emissioni di CO2 in base alla rete elettrica locale.

## Regole del benchmark

1. **Stesso hardware, stessi dati, stesse condizioni** per le query confrontate.
2. Cache fredda: eseguire ogni query almeno 3 volte, scartare la prima (warm-up) e riportare la mediana delle successive, oppure svuotare la cache del DBMS tra le esecuzioni.
3. Riportare sempre: dimensione dei dati, versione del DBMS, hardware, data della misura.
4. Le stime energetiche sono indicative: servono a confrontare approcci, non a certificare consumi assoluti.
