WITH RECURSIVE cycle_detection AS (
    -- Base case: Start by selecting all edges in a specific graph (replace `GRAPH_ID` with the ID of the graph you want to query)
    SELECT
        e.edge_from,
        e.edge_to,
        ARRAY[e.edge_from::text] AS path,  -- Initialize the path with the starting node
        false AS cycle_detected,
        e.graph
    FROM
        edges e
    WHERE e.graph = 'g5'  -- Filter for the specific graph

    UNION ALL

    -- Recursive case: Traverse the graph by following edges and extending the path
    SELECT
        e.edge_from,
        e.edge_to,
        cd.path || e.edge_from,  -- Extend the path by appending the current node
        e.edge_to = ANY(cd.path) AS cycle_detected,  -- Check if the next node already exists in the path
        e.graph
    FROM
        edges e
    JOIN
        cycle_detection cd ON e.edge_from = cd.edge_to
    WHERE
        e.graph = cd.graph
        AND NOT cd.cycle_detected  -- Only continue if no cycle has been detected so far
)

-- Select all detected cycles
SELECT
    n_from.name AS from_node_name,
    n_to.name AS to_node_name,
    array_to_string(ARRAY(SELECT n.name FROM nodes n WHERE n.id = ANY(cd.path) AND n.graph = 'g5'), ' -> ') AS cycle_path
FROM
    cycle_detection cd
JOIN
    nodes n_from ON cd.graph = n_from.graph AND cd.edge_from = n_from.id
JOIN
    nodes n_to ON cd.graph = n_to.graph AND cd.edge_to = n_to.id
WHERE
    cd.cycle_detected = true;