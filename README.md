Tucows Assignment
=========

*Populates database tables graph, nodes, and edges with the information given a directed graph XML. 
Queries the database tables with the query parameters given in a JSON input file. Returns a JSON file with 
answers to the given queries.*

To view the accompanying writeup, please see [writeup.md](./writeup.md).

Installation
------------

1. Create virtual environment.

```
python3 -m venv venv
cd venv/bin
source activate
```
2. Install the requirements in the virtual environment.

```
pip install -e .
```

3. Add environment variable `SQLALCHEMY_DATABASE_URL` with database URL 
(Ex. `postgresql://postgres:test1234@localhost/GraphApplicationDatabase`)

```
export SQLALCHEMY_DATABASE_URL="postgresql://postgres:test1234@localhost/GraphApplicationDatabase"
```

4. To create the graphs, nodes, and edges tables in the database, run the following sql:

```
CREATE TABLE IF NOT EXISTS graphs (
  id varchar(10),
  name varchar(20),
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS nodes (
  id varchar(10),
  name varchar(20),
  graph varchar(20),
  FOREIGN KEY (graph) REFERENCES graphs(id),
  PRIMARY KEY (id, graph)
);

CREATE TABLE IF NOT EXISTS edges (
  id varchar(10),
  edge_from varchar(10),
  edge_to varchar(10),
  graph varchar(20),
  cost float,
  FOREIGN KEY (graph) REFERENCES graphs(id),
  FOREIGN KEY (edge_from, graph) REFERENCES nodes(id, graph),
  FOREIGN KEY (edge_to, graph) REFERENCES nodes(id, graph),
  PRIMARY KEY (id, graph)
);
```

Execution 
------------
1. To populate the database tables, run the command below. Refer to graph.xml 
on how to structure a directed graph. 

```
interview_test load graph.xml
```

2. To query the database for paths and cheapest paths between a start node and an end node,
run the command below. Refer to input.json on how to structure the paths and cheapest paths queries.

```
interview_test query g1 input.json output.json
```
