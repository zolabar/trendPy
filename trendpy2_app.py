import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import trendpy2.models as tpm
from trendpy2 import __version__
import numpy as np
import sympy as sym
from sympy import atan as arctan
from sympy import sqrt, sin, cos, tan, exp, log, ln
a, b, c, x = sym.symbols('a, b, c, x', real=True)





def main():
    st.title(f"TrendPy App")


    # Upload CSV file through Streamlit widget
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file, comment='#').select_dtypes(include=np.number)

      

        # Allow the user to select two columns for plotting
        col1, col2 = st.columns(2)  # Use st.columns for horizontal layout
        selected_x_column = col1.selectbox("Select X-axis column:", df.columns)
        selected_y_column = col2.selectbox("Select Y-axis column:", df.columns)
        
        trend_list = ['just raw data',
                      'linear',
                      'polynomial',
                      'trigonometric',
                      'exponential',
                      'manual']
        
        col_trend_1, col_trend_2 = st.columns(2)  # Use st.columns for horizontal layout
        
        trend = col_trend_1.selectbox('trend', trend_list)
        if trend == 'polynomial':
            degree = col_trend_2.selectbox('degree', [1, 2, 3, 4, 5, 6 ])
            
        if trend == 'manual':
            ansatz = st.text_input('ansatz')            
        
        x = df[selected_x_column].to_numpy()
        y = df[selected_y_column].to_numpy()
       
        if trend == 'linear':
            st.latex('f(x)=c_0 x+c_1')
            
        if trend == 'polynomial':
            st.latex('f(x)=\sum_{k=0}^n c_{n-k} x^{n-k}')        
            
        if trend == 'trigonometric':
            st.latex('f(x)=c_0\cdot\cos(c_1\cdot 2\pi\cdot x+c_2)') 

        if trend == 'exponential':
            st.latex('f(x)=c_0\cdot \exp(c_1\cdot x)')   
                         

        # Create a scatter plot using Plotly Graph Objects
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name='Data'))
        fig.update_layout(title_text="Scatter Plot", xaxis_title=selected_x_column, yaxis_title=selected_y_column)
        if trend == 'linear':
            fit = tpm.Trend(x, y, 'linReg')
            r2 = round(fit.r2, 2)
            x = np.linspace(x[0], x[-1], 500)
            fig.update_layout(title_text=f"coefs: {fit.coef}")
            fig.add_trace(go.Scatter(x=x, y=fit.pred(x), mode='lines', name=f'Fit, r2={r2}'))
        if trend == 'polynomial':
            fit = tpm.Trend(x, y, 'polReg', degree)
            r2 = round(fit.r2, 2)
            x = np.linspace(x[0], x[-1], 500)
            fig.update_layout(title_text=f"coefs: {fit.coef}")
            fig.add_trace(go.Scatter(x=x, y=fit.pred(x), mode='lines', name=f'Fit, r2={r2}'))      
        if trend == 'trigonometric':
            fit = tpm.Trend(x, y, 'trigReg')
            r2 = round(fit.r2, 2)
            x = np.linspace(x[0], x[-1], 500)
            fig.update_layout(title_text=f"coefs: {fit.coef}")
            fig.add_trace(go.Scatter(x=x, y=fit.pred(x), mode='lines', name=f'Fit, r2={r2}'))           
        if trend == 'exponential':
            fit = tpm.Trend(x, y, 'expReg')
            r2 = round(fit.r2, 2)
            x = np.linspace(x[0], x[-1], 500)
            fig.update_layout(title_text=f"coefs: {fit.coef}")
            fig.add_trace(go.Scatter(x=x, y=fit.pred(x), mode='lines', name=f'Fit, r2={r2}'))          
        if trend == 'manual':          
            try:
                 fit = tpm.Trend(x, y, ansatz='freeReg', freeRegAnsatz=ansatz)
                 r2 = round(fit.r2, 2)
                 x = np.linspace(x[0], x[-1], 500)
                 fig.update_layout(title_text=f"coefs: {fit.coef}")
                 fig.add_trace(go.Scatter(x=x, y=fit.pred(x), mode='lines', name=f'Fit, r2={r2}'))                 
            except:
                print('Enter function expression, like: a*x+b or a*arctan(b*x+c))')
        
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
