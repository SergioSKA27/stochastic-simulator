import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config

class Graph:
    def __init__(self, nodes: list = [] , edges: list = []):
        self.nodes = nodes
        self.edges = edges

    def add_node(self, node: Node):
        self.nodes.append(node)

    def add_edge(self, edge: Edge):
        self.edges.append(edge)

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

        return agraph(nodes=self.nodes, edges=self.edges, config=config)
