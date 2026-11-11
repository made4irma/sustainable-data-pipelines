-- Versione NAIVE: sprechi tipici di una pipeline reale
-- 1. SELECT *: legge tutte le colonne (I/O e memoria sprecati)
-- 2. ORDER BY inutile: il consumatore a valle riordina comunque
-- 3. DATE_TRUNC valutata su ogni riga: impedisce l'uso di indici

SELECT *
FROM (
    SELECT
        t.*,
        DATE_TRUNC('month', t.ts) AS month,
        upper(t.category) AS cat_upper
    FROM transactions t
    WHERE DATE_TRUNC('month', t.ts) >= '2025-01-01'
) sub
ORDER BY month, cat_upper, tx_id;
