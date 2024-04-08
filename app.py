import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import random


st.set_page_config(page_title="Graph Editor", page_icon="🧊",layout="wide")

class StochaticGraph:
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



if 'graph' not in st.session_state:
    st.session_state.graph = StochaticGraph()


graph_editor_cols = st.columns([0.4,0.2,0.2,0.2])



physiscs_on = graph_editor_cols[0].toggle("Activar físicas", key="physics_on")

with graph_editor_cols[3].popover("Añadir nodo",help="Añade un nodo al grafo",use_container_width=True):


    name =  st.text_input("Nombre del nodo", key="node_name")
    shape = st.selectbox("Forma del nodo", options=["circle", "ellipse", "database", "box", "text", "image", "circularImage", "diamond", "dot", "star", "triangle", "triangleDown", "hexagon", "square",], key="node_shape")
    color = st.color_picker("Color del nodo", key="node_color",value="#7BE141")
    if shape == "image" or shape == "circularImage":
        url = st.text_input("URL de la imagen", key="node_url", value="https://www.zooplus.co.uk/magazine/wp-content/uploads/2021/01/striped-grey-kitten.jpg")
    else:
        url = None
    if st.button("Añadir nodo"):
        if url is not None:
            if not st.session_state.graph.in_nodes(name):
                st.session_state.graph.add_node(Node(id=name, label=name,shape=shape,color=color,image=url))
            else:
                st.error("El nodo ya existe")
        else:
            if not st.session_state.graph.in_nodes(name):
                st.session_state.graph.add_node(Node(id=name, label=name,shape=shape,color=color))
            else:
                st.error("El nodo ya existe")

with graph_editor_cols[2].popover("Añadir arista",help="Añade una arista al grafo",use_container_width=True):

    name =  st.text_input("Nombre de la arista", key="edge_name")
    source = st.selectbox("Nodo origen", options=[node.id for node in st.session_state.graph.get_nodes()], key="edge_source")
    target = st.selectbox("Nodo destino", options=[node.id for node in st.session_state.graph.get_nodes()], key="edge_target")
    color = st.color_picker("Color de la arista", key="edge_color",value="#7BE141")
    if st.button("Añadir arista" ,disabled=st.session_state.graph.is_empty()):
        if not st.session_state.graph.in_nodes(source):
            st.error("El nodo origen no existe")
        elif not st.session_state.graph.in_nodes(target):
            st.error("El nodo destino no existe")
        else:
            if not st.session_state.graph.in_edges(source, target):
                st.session_state.graph.add_edge(Edge(source=source,
                                                    target=target,
                                                    label=name,
                                                    color=color,
                                                    smooth=True)
                                                )
                st.write(Edge(source=source, target=target, label=name, color=color).to_dict())
            else:
                st.error("La arista ya existe")

if st.session_state.graph.is_empty():
    st.info("No hay nodos en el grafo")
else:
    st.session_state.graph.render_graph(config={"height":500,
                                                "width":1024,
                                                "directed":True,
                                                "physics":physiscs_on,
                                                "hierarchical":False
                                                }
                                                )







