import streamlit as st
from streamlit_agraph import Node, Edge
from components import StochasticGraph
import json
import pandas as pd
import sympy as sp

st.set_page_config(page_title="Graph Editor", page_icon="🧊",layout="wide")




if 'graph' not in st.session_state:
    st.session_state.graph = StochasticGraph()

if "states_set" not in st.session_state:
    st.session_state.states_set = set()

if "proyectname" not in st.session_state:
    st.session_state.proyectname = "Proyecto"

proyect_name = st.text_input("Nombre del proyecto", key="proyect_name",max_chars=20,value=st.session_state.proyectname)
if len(proyect_name) > 0 and proyect_name != st.session_state.proyectname:
    st.session_state.proyectname = proyect_name


st.title("M@C Grapher",help="Crea y edita grafos de manera sencilla")
graph_editor_cols = st.columns([0.7,0.3])


# Graph Editor
physiscs_on = graph_editor_cols[1].toggle("Activar físicas", key="physics_on",value=True,help="Activa la simulación de físicas en la gráfica")

with graph_editor_cols[1].popover("Añadir nodo",help="Añade un nodo al grafo",use_container_width=True):


    name =  st.text_input("Nombre del nodo", key="node_name",max_chars=10)
    shape = st.selectbox("Forma del nodo", options=["circle", "ellipse", "database", "box", "text", "image", "circularImage", "diamond", "dot", "star", "triangle", "triangleDown", "hexagon", "square",], key="node_shape")
    color = st.color_picker("Color del nodo", key="node_color",value="#7BE141")
    if shape == "image" or shape == "circularImage":
        url = st.text_input("URL de la imagen", key="node_url", value="https://www.zooplus.co.uk/magazine/wp-content/uploads/2021/01/striped-grey-kitten.jpg")
    else:
        url = None
    if st.button("Añadir nodo",disabled=len(name) == 0):
        if url is not None:
            if not st.session_state.graph.in_nodes(name):
                st.session_state.graph.add_node(Node(id=name, label=name,shape=shape,color=color,image=url))
                st.session_state.states_set.add(name)
            else:
                st.error("El nodo ya existe")
        else:
            if not st.session_state.graph.in_nodes(name):
                st.session_state.graph.add_node(Node(id=name, label=name,shape=shape,color=color))
                st.session_state.states_set.add(name)
            else:
                st.error("El nodo ya existe")

with graph_editor_cols[1].popover("Añadir arista",help="Añade una arista al grafo",use_container_width=True):

    nameedege =  st.number_input("Peso de la arista",key="edge_weight",min_value=0.0,max_value=1.0,step=0.1,format="%.2f")
    nodelist = [node.id for node in st.session_state.graph.get_nodes()]
    source = st.selectbox("Nodo origen", options=nodelist, key="edge_source")
    target = st.selectbox("Nodo destino", options=nodelist, key="edge_target")
    color = st.color_picker("Color de la arista", key="edge_color",value="#000000")
    if st.checkbox("Crear arista de regreso", key="edge_back"):
        nameedege2 = st.number_input("Peso de la arista de regreso",key="edge_weight2",min_value=0.0,max_value=1.0,step=0.1,format="%.2f")
    else:
        nameedege2 = None
        
    if st.button("Añadir arista" ,disabled=st.session_state.graph.is_empty()):
        if not st.session_state.graph.in_nodes(source) or not st.session_state.graph.in_nodes(target):
            st.error("El nodo origen o destino no existe!")
        else:
            if not st.session_state.graph.in_edges(source, target):
                st.session_state.graph.add_edge(Edge(source=source,
                                                    target=target,
                                                    label="%0.2f"%nameedege,
                                                    color=color,
                                                    smooth=True,
                                                    length=150,)
                                                )
                
                st.write(Edge(source=source, target=target, label=nameedege, color=color).to_dict())
            else:
                st.error("La arista ya existe")
            
            if nameedege2 is not None and source != target:
                if not st.session_state.graph.in_edges(target, source):
                    st.session_state.graph.add_edge(Edge(source=target,
                                                        target=source,
                                                        label="%0.2f"%nameedege2,
                                                        color=color,
                                                        smooth=True,
                                                        length=150,)
                                                    )
                else:
                    st.error("La arista de regreso ya existe")

with graph_editor_cols[1].popover("Limpiar grafo",help="Elimina todos los nodos y aristas del grafo",use_container_width=True):
    if st.button("Limpiar grafo"):
        st.session_state.graph = StochasticGraph()

with graph_editor_cols[1].popover("Cargar Configuración",help="Carga la configuración de un grafo previamente guardado",use_container_width=True):
    file = st.file_uploader("Selecciona un archivo JSON",type=["json"])
    if file is not None:
        data = json.load(file)
        st.session_state.graph = StochasticGraph()
        st.session_state.graph.load_json(data)
        st.session_state.proyectname = file.name.split(".")[0]
    

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


if st.button("Mostrar propiedades",disabled=st.session_state.graph.is_empty()):
    st.session_state.graph.render_properties()
#Graph Configuration
with st.popover("Propiedades de la gráfica",help="Visualiza y edita las propiedades de la gráfica",use_container_width=True):
    cols = st.columns([0.5,0.5])

    with cols[0].container(border=True):
        st.subheader("Propiedades")
        st.write("$$D(G) = "+str(len(st.session_state.graph.get_nodes()))+r"\ \text{vértices}$$")
        st.write("$$E(G) = "+str(len(st.session_state.graph.get_edges()))+r"\ \text{aristas}$$")
        st.write(st.session_state.graph.get_adjacency())


st.write(st.session_state.graph.get_canonical_form())
st.download_button("Descargar configuración",
                   data=json.dumps(st.session_state.graph.get_json()),
                   file_name=str(st.session_state.proyectname+".json"),
                   mime="application/json")

