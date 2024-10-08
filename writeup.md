# Writeup

This is the writeup for the questions from the Tucows assignment.

## Database Design

The database is made up of three tables: graphs, nodes, and edges. The graphs
table has two columns, id and name, both of which are of type string. The id
serves as a unique identifier for a graph and is the primary key.

The nodes table contains three columns: id, graph, and name, all of which are
of type string. The id represents the node identifier, the name represents the
node name, and the graph column acts as a foreign key referencing the id in the
graphs table. Node ids are unique within a graph, but multiple graphs may have
nodes with the same ids. To address this, the primary key consists of the node
id and the graph id.

The edges table stores edges in a graph and has columns id, graph, edge_to,
edge_from, and cost. The id is of type string and cost is of type float. The
edge_to and edge_from columns are foreign keys referencing the id of a node in
the nodes table. The graph column is also a foreign key that references the id
of a graph in the graphs table. The primary keys are id and graph to ensure
uniqueness.

This setup ensures that all tables have a connection. The nodes table relates
to the graphs table via the graph id. The edges table relates to the nodes
table by node id and the graphs table by graph id. This guarantees that all
nodes and edges belong to a graph that exists in the graphs table and that the
nodes of an edge exist in the nodes table. If necessary, the graph XML can be
reconstructed using the information provided in the three tables.

## XML Parser

To parse the graph, the built-in xml library was used. For small amounts of
validation, this library suffices. If more complicated validation was required,
a library such as lxml would have been better as it includes a validating
parser.

## JSON Parser

Json is a built-in Python library that also requires no additional
installation. It is user-friendly and can easily convert between JSON data and
Python objects, which was necessary for this assignment.

## Find All Paths

To find all paths between two nodes, I've created a function that takes in a
graph of type default dictionary, a start node, an end node, and a path
variable that defaults to None. The default dictionary ensures that a KeyError
will not be thrown in case one of the nodes is not a key in the dictionary.
Instead, it will add the key to the dictionary and default the value to an
empty list. The function follows a depth-first search (DFS) to find all paths
in the graph. The function starts by adding the start node to the path list.
Then, it loops through all the values the start node points to and recursively
calls the function with a new start node. The function recurses until the stop
condition is met where the start node equals the end node. The function will
return all paths that exist between the start node and end excluding cycles.

## Find Cheapest Path

To find the cheapest path between a start node and an end node, another
recursive function was created which follows a similar DFS pattern as the
find_all_paths function. More logic was implement to add the costs of all the
edges in a path and set the shortest path to the path with the least cost. This
was done by passing in an edges_cost dictionary with key-value pairs of edges
and costs. The function will return the cheapest path between the start node
and the end node.

## Input/Output

I decided to use command line arguments instead of standard input and standard
output to make testing easier. I also believe it is more user-friendly.
