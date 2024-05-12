import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config

class Graph:
    def __init__(self, nodes: list = None , edges: list = None):
        self.nodes: list = nodes if nodes is not None else []
        self.edges: list = edges if edges is not None else []
        self._node_set: set = set()
        self._edge_set: set = set()

    def add_node(self, node: Node):
        self.nodes.append(node)
        self._node_set.add(node.id)

    def add_edge(self, edge: Edge):
        self.edges.append(edge)
        data = edge.to_dict()
        self._edge_set.add((data["source"], data["to"], data["label"]))

    def get_nodes(self):
        return self.nodes

    def get_edges(self):
        return self.edges

    def is_empty(self):
        return len(self.nodes) == 0

    def in_nodes(self, id: str):
        return any(node.id == id for node in self.nodes)

    def in_edges(self, id_source: str, id_target: str):
        for edge in self.edges:
            dict_edge = edge.to_dict()
            if dict_edge["source"] == id_source and dict_edge["to"] == id_target:
                return True

        return False

    def get_adjacency(self):
        matrix = []
        for node in self.nodes:
            row = {node.id: []}
            for node2 in self.nodes:
                if self.in_edges(node.id, node2.id):
                    row[node.id].append(node2.id)

            matrix.append(row)
        return matrix

    def get_incidence(self):
        matrix = []
        for edge in self.edges:
            row = {edge.source: []}
            for node in self.nodes:
                if edge.to == node.id:
                    row[edge.source].append(node.id)

            matrix.append(row)
        return matrix


    def to_dot(self,t="digraph"):
        dot = f"{t} G {{\n"
        if len(self.edges) == 0:
            for node in self.nodes:
                node_dict = node.to_dict()
                dot += f'{node_dict["id"]} [label="{node_dict["label"]}"];\n'
        else:
            nodeids  = []
            for node in self.edges:
                edge_dict = node.to_dict()
                if edge_dict["source"] not in nodeids:
                    nodeids.append(edge_dict["source"])
                if edge_dict["to"] not in nodeids:
                    nodeids.append(edge_dict["to"])

                dot += f'{edge_dict["source"]} -> {edge_dict["to"]} [label="{edge_dict["label"]}"];\n'

            for node in self.nodes:
                if node.id not in nodeids:
                    node_dict = node.to_dict()
                    dot += f'{node_dict["id"]} [label="{node_dict["label"]}"];\n'
        dot += "}"
        return dot

    @st.experimental_fragment
    def render_graph(self,config: dict = None):
        if config is None:
            config = Config(height=500,
                            width=500,
                            directed=True,
                            physics=True,
                            hierarchical=False
                        )
        else:
            config = Config(**config)

        fragment = agraph(self.nodes, self.edges, config=config)
        st.write(fragment)
       
            

    def get_json(self):
        return {
            "nodes": [node.to_dict() for node in self.nodes],
            "edges": [edge.to_dict() for edge in self.edges]
        }
        
    def load_json(self, data: dict):
        self.nodes = [Node(**node) for node in data["nodes"]]
        self.edges = []
        for edge in data["edges"]:
            source = edge["source"]
            target = edge["to"]
            label = edge["label"]
            del edge["source"]
            del edge["to"]
            del edge["label"]
            del edge["from"]
            
            self.add_edge(Edge(source=source, target=target, label=label, **edge))
            

    @property
    def ssnodes(self):
        return self._node_set
    
    @property
    def sedges(self):
        return self._edge_set
