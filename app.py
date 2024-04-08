import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from components import Graph
import random


st.set_page_config(page_title="Graph Editor", page_icon="🧊",layout="wide")




if 'graph' not in st.session_state:
    st.session_state.graph = Graph()



st.title("M@C Grapher",help="Crea y edita grafos de manera sencilla")
graph_editor_cols = st.columns([0.7,0.3])


# Graph Editor
physiscs_on = graph_editor_cols[1].toggle("Activar físicas", key="physics_on",value=True,help="Activa la simulación de físicas en la gráfica")

with graph_editor_cols[1].popover("Añadir nodo",help="Añade un nodo al grafo",use_container_width=True):


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

with graph_editor_cols[1].popover("Añadir arista",help="Añade una arista al grafo",use_container_width=True):

    name =  st.text_input("Nombre de la arista", key="edge_name")
    source = st.selectbox("Nodo origen", options=[node.id for node in st.session_state.graph.get_nodes()], key="edge_source")
    target = st.selectbox("Nodo destino", options=[node.id for node in st.session_state.graph.get_nodes()], key="edge_target")
    color = st.color_picker("Color de la arista", key="edge_color",value="#000000")
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
                                                    smooth=True,
                                                    length=100,)
                                                )
                #st.write(Edge(source=source, target=target, label=name, color=color).to_dict())
            else:
                st.error("La arista ya existe")

if st.session_state.graph.is_empty():
    with graph_editor_cols[0]:
        st.info("No hay nodos en el grafo")
else:
    with graph_editor_cols[0]:
        tabs = st.tabs(["Gráfica Interactiva", "Gráfica Simple"])
        with tabs[0]:
            st.session_state.graph.render_graph(config={"height":500,
                                                    "width":1024,
                                                    "directed":True,
                                                    "physics":physiscs_on,
                                                    "hierarchical":False
                                                    }
                                                    )
        with tabs[1]:

            st.graphviz_chart(st.session_state.graph.to_dot())


#Graph Configuration
with st.popover("Propiedades de la gráfica",help="Visualiza y edita las propiedades de la gráfica",use_container_width=True):
    st.graphviz_chart(st.session_state.graph.to_dot())




