from .graph import Graph


class StochasticGraph(Graph):
    def __init__(self, nodes: list = None, edges: list = None):
        super().__init__(nodes, edges)

    @property
    def nodes(self):
        return self._nodes
    
    @nodes.setter
    def nodes(self, nodes):
        self._nodes = nodes
    
    @property
    def edges(self):
        return self._edges
    
    @edges.setter
    def edges(self, edges):
        self._edges = edges