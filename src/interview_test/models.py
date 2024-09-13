from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, ForeignKey, Float


Base = declarative_base()


class Graph(Base):
    __tablename__ = "graphs"

    id = Column(String, primary_key=True)
    graph_name = Column(String)


class Edge(Base):
    __tablename__ = "edges"

    graph_id = Column(String, ForeignKey("graphs.id"), primary_key=True)
    edge_id = Column(String, primary_key=True)
    edge_to = Column(String)
    edge_from = Column(String)
    cost = Column(Float)
