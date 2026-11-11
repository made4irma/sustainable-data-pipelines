-- Versione OTTIMIZZATA
-- 1. Solo le colonne necessarie
-- 2. Nessun ORDER BY intermedio
-- 3. Filtro diretto sul timestamp (sargable: puo' usare indici)
-- 4. Aggregazione direttamente, senza subquery inutili

SELECT
    DATE_TRUNC('month', ts) AS month,
    category,
    COUNT(*) AS tx_count,
    SUM(amount) AS revenue
FROM transactions
WHERE ts >= '2025-01-01'
GROUP BY 1, 2;

-- Variante per pipeline ripetute: pre-aggregazione incrementale.
-- La tabella riepilogo si aggiorna solo con i dati nuovi del giorno,
-- e le query a valle leggono migliaia di righe invece di milioni:
--
-- CREATE TABLE monthly_summary AS
-- SELECT DATE_TRUNC('month', ts) AS month, category,
--        COUNT(*) AS tx_count, SUM(amount) AS revenue
-- FROM transactions GROUP BY 1, 2;
