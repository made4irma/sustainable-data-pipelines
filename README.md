# sustainable-data-pipelines

Divulgazione su **data management a basso consumo energetico**: pipeline SQL ottimizzate, dati sintetici riproducibili e benchmark di consumo misurabili.

## Perché questo progetto

Ogni query che gira su un data warehouse consuma energia: CPU, memoria, I/O, rete. A scala di milioni di query al giorno, la differenza tra una query scritta male e una ottimizzata si misura in kWh reali. Questo repository mostra, con esempi concreti e riproducibili, **quanto si può risparmiare** semplicemente scrivendo meglio le stesse trasformazioni.

## Struttura

```
sustainable-data-pipelines/
├── docs/
│   └── metodologia.md          # come misuriamo tempo, CPU ed energia
└── use-cases/
    └── 01-sql-aggregation/     # aggregazioni: naive vs ottimizzata
        ├── README.md           # il caso d'uso spiegato
        ├── generate_data.py    # generatore di dati sintetici
        ├── naive.sql           # la query "come non farla"
        ├── optimized.sql       # la query ottimizzata
        └── benchmark.md        # risultati misurati
```

## Come riprodurre i benchmark

1. Genera i dati sintetici: `python use-cases/01-sql-aggregation/generate_data.py`
2. Carica le tabelle sul tuo database (istruzioni nel README del caso d'uso)
3. Esegui le due query e misura con la metodologia in `docs/metodologia.md`
4. Confronta i tuoi risultati con quelli in `benchmark.md`

## Licenza

MIT
