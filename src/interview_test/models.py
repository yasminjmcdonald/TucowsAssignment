from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, ForeignKey, Float


Base = declarative_base()


class Graph(Base):
    __tablename__ = "graphs"

    id = Column(String, primary_key=True)
    name = Column(String)


class Node(Base):
    __tablename__ = "nodes"

    id = Column(String, primary_key=True)
    graph = Column(String, ForeignKey("graphs.id"), primary_key=True)
    name = Column(String)


class Edge(Base):
    __tablename__ = "edges"

    id = Column(String, primary_key=True)
    graph = Column(String, ForeignKey("graphs.id"), primary_key=True)
    edge_to = Column(String, ForeignKey("nodes.id"))
    edge_from = Column(String, ForeignKey("nodes.id"))
    cost = Column(Float)
