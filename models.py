from database import Base
from sqlalchemy import Column, String, ForeignKey, Float


class Graphs(Base):
    __tablename__ = "graphs"

    id = Column(String, primary_key=True, unique=True)
    graph_name = Column(String, unique=True)


class Edges(Base):
    __tablename__ = 'edges'

    id = Column(String, primary_key=True, unique=True)
    edge_to = Column(String)
    edge_from = Column(String)
    cost = Column(Float)
    graph_id = Column(String, ForeignKey("graphs.id"))
