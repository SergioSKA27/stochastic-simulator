from .graph import Graph
import pandas as pd
import sympy as sp
import numpy as np
import streamlit as st

from plotly import graph_objects as go

x='''def is_ergodic_chain(self):
        tdf = self.get_transition_matrix_df()
        return np.all(tdf.sum(axis=1) == 1) and np.all(tdf.values > 0)
    
    def is_absorbing_chain(self):
        tdf = self.get_transition_matrix_df()
        return np.all(tdf.sum(axis=1) == 1) and np.all(tdf.values >= 0)
    
    def is_irreducible_chain(self):
        tdf = self.get_transition_matrix_df()
        return np.all(tdf.sum(axis=1) == 1) and np.all(tdf.values > 0)
    
    '''
    
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

    def get_transition_matrix(self):
        matrix = {}
        for node in self.nodes:
            matrix[node.id] = {}
            for edge in self.edges:
                if edge.source == node.id:
                    matrix[node.id][edge.to] = float(edge.label)

        return matrix
    
    
    def get_transition_matrix_df(self):
        tm = self.get_transition_matrix()
        tdf = pd.DataFrame(tm).T.fillna(0)
        return tdf
    
    def get_numpy_transition_matrix(self):
        tdf = self.get_transition_matrix_df()
        return tdf.to_numpy(dtype="float64")
    
    @st.experimental_dialog("Propiedades De la Cadena de Markov",width="large")
    def render_properties(self):
        tdf = self.get_transition_matrix_df()
        st.write("Matriz de Transición")
        st.latex("T = "+ sp.latex(sp.Matrix(tdf.to_numpy())))
        with st.expander("Ver Matriz con Indicadores"):
            st.write(tdf)
        
        
        
        tabs = st.tabs(["Ergodicidad","Absorción","Irreducibilidad","Regularidad","Aperiodicidad"])
        with tabs[4]:
            st.subheader("Aperiodicidad")
            st.caption("""Una cadena de Markov $\{X_n\}$ con espacio de estados $E$ se dice que es aperiódica
                            si para cada estado $i \in E$, el periodo de $i$ es 1, es decir, si para cada estado
                            $i \in E$, se cumple que $d(i) = 1$, donde $d(i)$ es el máximo común divisor de los
                            tiempos de retorno al estado $i$
                        """)
            is_aperiodic = self.is_aperiodic_chain()
            if is_aperiodic:
                st.success("La cadena es aperiódica")
            else:
                st.error("La cadena no es aperiódica")
                
        with tabs[3]:
            st.subheader("Regularidad")
            st.caption("""
                         Una cadena de Markov $\{X_n\}$ con espacio de estados $E$ se dice que es regular
                         si todas sus clases de estados son recurrentes positivas, es decir, si para cada
                         estado $i \in E,$ se cumple que $\mathbb{P}(T_i < \infty | X_0 = i) = 1$, donde
                         $T_i$ es el primer tiempo de retorno al estado $i$
                       """)
            is_regular,logs = self.is_regular_chain()

            if is_regular:
                st.success("La cadena es regular")
            else:
                st.error("La cadena no es regular o no se ha alcanzado el límite de iteraciones necesarias")
        
            with st.expander("Logs de Iteraciones"):
                iterat = st.slider("Iteración",0,len(logs)-1,0)
                dflo = pd.DataFrame(logs[iterat],index=tdf.index,columns=tdf.columns)
                st.write(dflo)
                
                st.write("Graficas de la matriz de transición")
                
                fig = go.Figure()
                fig.add_trace(go.Heatmap(z=dflo.values,
                                         x=dflo.columns,
                                         y=dflo.index,
                                         colorscale='Viridis'))
                st.plotly_chart(fig)
                
                st.write("Grafica de Probabilidades")
                evente = st.selectbox("Evento",list(tdf.columns))
                prob = st.slider("T",0,len(logs)-1,0)
                
                gdf = pd.DataFrame(logs[prob],index=tdf.index,columns=tdf.columns)
                fig2 = go.Figure()
                fig2.add_trace(go.Scatter(x=gdf.index,
                                            y=gdf[evente],
                                            mode="lines+markers"))
                
                fig2.update_layout(title="Probabilidad de Transición de "+evente + " a los estados en el tiempo "+str(prob),
                                  xaxis_title="Estados",
                                  yaxis_title="Probabilidad")
                st.plotly_chart(fig2)
                
        with tabs[2]:
            st.subheader("Irreducibilidad")
            st.caption("""
                            Una cadena de Markov $\{X_n\}$ con espacio de estados $E$ se dice que es irreducible
                            si para cualquier par de estados $i,j \in E$, existe un entero $n \geq 0$ tal que
                            $\mathbb{P}(X_n = j | X_0 = i) > 0$
                        """)
            is_irreducible = self.is_irreducible_chain()
            if is_irreducible:
                st.success("La cadena es irreducible")
            else:
                st.error("La cadena no es irreducible")
                
        with tabs[1]:
            st.subheader("Absorción")
            st.caption(r"""
                            Una cadena de Markov $\{X_n\}$ con espacio de estados $E$ se dice que es absorbente
                            si existe un subconjunto $A \subset E$ tal que:
                            
1. $A$ es cerrado bajo la matriz de transición $T$
2. $T_{ii} = 1$ para todo $i \in A$
3. $T_{ij} = 0$ para todo $i \in A$ y $j \notin A$
                        """)
            is_absorbing = self.is_absorbing_chain()
            if is_absorbing:
                st.success("La cadena es absorbente")
            else:
                st.error("La cadena no es absorbente")
        
        with tabs[0]:
            is_ergodic = self.is_ergodic_chain()
            st.subheader("Ergodicidad")
            st.caption("""
                         Una cadena de Markov $\{X_n\}$ con espacio de estados $E$ se dice que es ergódica
                         si es irreducible y aperiódica
                       """)
            if is_ergodic:
                st.success("La cadena es ergódica")
            else:
                st.error("La cadena no es ergódica")

    @st.experimental_dialog("Calculo de Expresiones",width="large")
    def render_expression_calculation(self):
        st.write("Calculo de Expresiones")
        tdf = self.get_transition_matrix_df()
        st.write("Matriz de Transición")
        st.latex("T = "+ sp.latex(sp.Matrix(tdf.to_numpy())))
        with st.expander("Ver Matriz con Indicadores"):
            st.write(tdf)
    
        expr = st.text_area("Expresión",value="T**2")
        symexp = sp.parse_expr(expr,transformations="all")
        
        if st.button("Calcular"):
            result = symexp.subs("T",sp.Matrix(tdf.to_numpy()))
            st.latex(sp.latex(symexp)+" = "+sp.latex(result))
        
        
    def is_regular_chain(self,limit=1000):
        tdf = self.get_numpy_transition_matrix()
        logs = []
        for i in range(1,limit):
            result = np.linalg.matrix_power(tdf,i)
            
            if  i > 1 and (result  == logs[-1]).all():
                logs.append(result)
                return True,logs
            else:
                logs.append(result)
            
            
        return False,logs
        
    def is_ergodic_chain(self):
        tdf = self.get_transition_matrix_df()
        return np.all(tdf.sum(axis=1) == 1) and np.all(tdf.values > 0)
    
    def is_absorbing_chain(self):
        tdf = self.get_transition_matrix_df()
        for row in tdf.iterrows():
            if sum(list(map(int,row[1].values))) == 1:
                return True
        return False

    def is_irreducible_chain(self):
        tdf = self.get_transition_matrix_df()
        return np.all(tdf.sum(axis=1) == 1) and np.all(tdf.values > 0)
    
    def is_aperiodic_chain(self):
        tdf = self.get_transition_matrix_df()
        return np.all(tdf.sum(axis=1) == 1) and np.all(tdf.values > 0)
    
    def get_absorbing_states(self):
        tdf = self.get_transition_matrix_df()
        states = []
        for row in tdf.iterrows():
            if sum(list(map(int,row[1].values))) == 1:
                states.append(row)
        return states
    
    def get_canonical_form(self):
        tdf = self.get_transition_matrix_df()
        absorbing = self.get_absorbing_states()
        return absorbing