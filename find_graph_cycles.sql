WITH RECURSIVE cycle_finder AS (
    -- Start with each edge
    SELECT edge_from, edge_to, ARRAY[edge_to::text] AS path
    FROM edges
    WHERE graph = 'insert graph id here'

    UNION ALL

    -- Recursively add edges
    SELECT ef.edge_from, e.edge_to, path || e.edge_to
    FROM cycle_finder ef
    JOIN edges e ON ef.edge_to = e.edge_from
    WHERE NOT e.edge_to = ANY(path) AND graph = 'insert graph id here'  -- Prevent revisiting nodes
)

SELECT DISTINCT path, edge_from, edge_to
FROM cycle_finder
where edge_from = edge_to

