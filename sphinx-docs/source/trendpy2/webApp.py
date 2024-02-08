# -*- coding: utf-8 -*-


import pandas as pd
import ipywidgets as widgets
from ipywidgets import interact, interactive
import plotly as plt
import plotly.express as px
import plotly.graph_objects as go
import io
from IPython.display import display, clear_output
from traitlets import traitlets
import trendpy2.methods as tm
from trendpy2 import __version__
import numpy as np
import warnings
import sympy as sym
from sympy import atan as arctan
from sympy import sqrt, sin, cos, tan, exp, log, ln
a, b, c, x = sym.symbols('a, b, c, x', real=True)

warnings.filterwarnings('ignore')

version = 'v' + __version__

class LoadedButton(widgets.Button):

    def __init__(self, value=None, *args, **kwargs):
        super(LoadedButton, self).__init__(*args, **kwargs)
        self.add_traits(value=traitlets.Any(value))


class App():
    
    def __init__(self):
        
        self.box_layout = widgets.Layout(display='flex',
                        justify_content='center')
        header = widgets.HTML(
            value=f'<h1 align="center">TrendPy WebApp<h1>\
            <h3 align="center">Visualization of trends in (time series) data {version}<h3>')
        
        logo = widgets.HTML(
            value='<img src="figures/logo.jpg" width="60" height="100" alt="TrendPy logo"></img>')
        
        logo_container = widgets.HBox([logo, header],layout=self.box_layout)
        display(logo_container)
        
        
        # In[3]:
        
        
        header2 = widgets.HTML(
            value='<h3 align="center">Upload a .csv file here<h3>')
        
        display(header2)
        
        
        # In[4]:
        
        
        self.uploaded_excel_file = widgets.FileUpload(accept=".csv", multiple=False)
        container = widgets.HBox([self.uploaded_excel_file],layout=self.box_layout)
        
        display(container)
        
        self.input_dropdown = widgets.Dropdown(
            options=[''],
            value='',
            description='Input (X):',
            disabled=False,
            )
        
        self.output_dropdown = widgets.Dropdown(
            options=[''],
            value='',
            description='Target (Y):',
            disabled=False,
            )
        
        self.trend_dropdown = widgets.Dropdown(
            options=['No trendline',
                     'linear',
                     'polynomial',
                     'trigonometric',
                     'exponential',
                     'manual'],
            value='No trendline',
            description='trendline:',
            disabled=False,
            )
        
        self.polynomial_deg_selection = widgets.Dropdown(
            options=[2,3,4,5,6],
            value=2,
            description='deg (polyn.)',
            disabled=True,
            )
        
        self.freeReg_ansatz_input = widgets.Text(
            value=' ',
            description='expression',
            disabled=True,
            )        
        
        
        self.r2_checkbox = widgets.Checkbox(
            value=False,
            description='Show R2 score',
            disabled=False,
            indent=True
        )
        
        # arrangement of dropdown menus
        dropdown_elements = widgets.HBox([self.input_dropdown, self.output_dropdown], layout=self.box_layout)
        trend_selection = widgets.HBox([self.trend_dropdown, self.polynomial_deg_selection, self.freeReg_ansatz_input], layout=self.box_layout)
        r2_container = widgets.HBox([self.r2_checkbox],layout=self.box_layout)
        
        
        # making all the widgets interactive, so no button needs to be pressed when changing a dropdown value      
        self.out2 = widgets.interactive_output(self.create_graphics, {'values_in': self.input_dropdown, 
                                                                 'values_out': self.output_dropdown, 
                                                                 'trend': self.trend_dropdown, 
                                                                 'deg': self.polynomial_deg_selection, 
                                                                 'expression': self.freeReg_ansatz_input, 
                                                                 'r2': self.r2_checkbox})
        
        self.out = widgets.Output()
        
        out2_container = widgets.HBox([self.out2],layout=self.box_layout)
        
        
        self.button = LoadedButton(description='Start calculation', 
                                   disable=False, 
                                   tooltip='Click to start calculation', 
                                   icon='check', 
                                   button_style='')
        
        self.button.on_click(self.create_pandas_dataframe)
        
        
        container2 = widgets.HBox([self.button],layout=self.box_layout)
        container_out = widgets.HBox([self.out],layout=self.box_layout)
        
        display(container2,container_out)        
        
        
        display(dropdown_elements, trend_selection, r2_container, out2_container)
        
        
        
        
        
        # In[22]:
        
        
        # defining a figure widget, that is created in the beginning and remains static, only graphs are updated
        # it is needed to define all needed graphs as empty ones here, so that you can use update_traces
        self.fig_widget = go.FigureWidget()
        self.fig_widget.layout.margin=dict(l=120, r=120, b=25, t=25)
        self.fig_widget.layout.height=400
        self.fig_widget.add_scatter(mode='markers', name='datapoints')
        self.fig_widget.add_scatter(mode='lines', name='trendline', line=dict(shape='spline'))
        self.fig_widget.update_layout(title_text="Time Series Regression", template='plotly')        
        
        return
    
    def create_pandas_dataframe(self, b):
        
        # resetting everything for a new calculation
        with self.out:
            clear_output()
        with self.out2:
            clear_output()
        self.input_dropdown.options = []
        self.output_dropdown.options = []
        self.fig_widget.update_traces(x=[],y=[],selector=({'name':'datapoints'}))
        self.fig_widget.update_traces(x=[],y=[],selector=({'name':'trendline'}))
        self.trend_dropdown.value='No trendline'
        self.polynomial_deg_selection.disabled=True
        self.freeReg_ansatz_input.disabled = True
        self.r2_checkbox.value=False
        self.r2_checkbox.disabled=True
            
        #checking whether data has been uploaded succesfully
        if (self.uploaded_excel_file.value=={}):
            self.button.button_style='warning'
            with self.out:
                print("No data entered. Please upload a .csv file.")
        
        else:
            try:
                
            
                #transforming the uploaded .csv file back to the type .csv in order to then create a pandas dataframe

                time_series_file = self.uploaded_excel_file.value[0].content

                time_series_data = pd.read_csv(io.BytesIO(time_series_file))
            
                #filling the drop down menus with the columns of the dataframe as options
                self.input_dropdown.options = time_series_data.select_dtypes(include='number').columns
                self.output_dropdown.options = time_series_data.select_dtypes(include='number').columns
                b.value = time_series_data

                self.button.button_style='success'
                
                with self.out: 
                    print("Data entered. Please select the X and Y values now. (Only works if header is in the first row of your file.)")
            except:
                self.button.button_style='warning'
                with self.out:
                    print('Invalid input! Make sure that header of the file is in first row and general format is correct!')
                
        return
    
    def create_graphics(self, values_in,values_out,trend,deg=2, expression='x', r2=False):
            if trend == 'polynomial':
                self.polynomial_deg_selection.disabled=False
            else:
                self.polynomial_deg_selection.disabled=True
                
            if trend == 'manual':
                self.freeReg_ansatz_input.disabled=False 
            else:
                self.freeReg_ansatz_input.disabled=True
                
            if values_in == '' or values_out=='':
                print("Please select your X and Y values in the dropdown menus above.")
            else:
                try: # sometimes an error is occuring when user hasn't changed the standard dropdown X and Y values yet
                     # through try/except the user does not see the error and won't notice it, because standard values are
                     # usually not going to be used
                    
                    # updateing the plot based on the input data
                    self.fig_widget.layout.xaxis.title = values_in
                    self.fig_widget.layout.yaxis.title = values_out
                    self.fig_widget.update_traces(x=self.button.value[values_in], 
                                                  y=self.button.value[values_out], 
                                                  selector=({'name':'datapoints'}))
                    if trend!="No trendline":
                        with self.out2:
                            clear_output()
                        self.r2_checkbox.disabled=False
                        self.calculate_trendline(values_in, values_out, trend, deg, expression, r2) # function that calculates and draws trendline is called
                    else:
                        self.fig_widget.update_traces(x=[],y=[],selector=({'name':'trendline'}))
                        self.r2_checkbox.disabled=True
                except:
                    pass
                
                return
            
            
    def calculate_trendline(self, values_in, values_out, trend, deg, expression, r2):
        sorted_df = self.button.value.sort_values(by=values_in) # without sorting trendlines can not be plotted correctly
        x_values=sorted_df[values_in].to_numpy()
        y_values=sorted_df[values_out].to_numpy()
        
        # in all cases coefficients are calculated first by calling function from methods.py
        # after that the predicted y-values are calculated by calling function from methods.py
        # with the data from y_pred-function it is then possible to plot the trendline
        # at last r2-score is calculated
        if trend=='linear':
            coefs=tm.linReg(x_values,y_values)
            print('coefficients: ', coefs)
            y_pred=tm.pred('linReg',coefs, x_values)
            self.fig_widget.update_traces(x=sorted_df[values_in], y=y_pred, selector=({'name':'trendline'}))
            self.fig_widget.update_layout(title_text=r"$f(x)=c_0\cdot x+c_1$")
            if r2==True:
                r2_score = tm.r2(y_values, y_pred)
                print('R2-score:     ', r2_score)
            
        elif trend=='polynomial':
            try:
                coefs = tm.polReg(x_values,y_values,deg)
                print('coefficients: ', coefs)
                y_pred = tm.pred('polReg', coefs, x_values)
                self.fig_widget.update_traces(x=sorted_df[values_in], y=y_pred, selector=({'name':'trendline'}), line=dict(shape='spline'))
                self.fig_widget.update_layout(title_text=r"$f(x)=c_0\cdot x^N+c_1 x^{N-1}+...+c_N$")
                if r2==True:
                    r2_score = tm.r2(y_values, y_pred)
                    print('R2-score:     ', r2_score)
            except:
                print('Selected regression might not be a good fit for the entered values! Please lower degree or choose other regression!')
        elif trend=='trigonometric':
            try:
                coefs = tm.trigReg(x_values,y_values)
                print('coefficients: ', coefs)
                y_pred = tm.pred('trigReg', coefs, x_values)
                self.fig_widget.update_traces(x=sorted_df[values_in], y=y_pred, selector=({'name':'trendline'}))
                self.fig_widget.update_layout(title_text=r"$f(x)=c_0\cdot \text(\cos(2\pi\cdot c_1+c_2))$")
                if r2==True:
                    r2_score = tm.r2(y_values, y_pred)
                    print('R2-score:     ', r2_score)
            except:
                print('Selected regression might not be a good fit for the entered values! Please choose other regression!')
        elif trend=='exponential':
            try:
                coefs = tm.expReg(x_values,y_values)
                print('coefficients: ', coefs)
                y_pred = tm.pred('expReg', coefs, x_values)
                self.fig_widget.update_traces(x=sorted_df[values_in], y=y_pred, selector=({'name':'trendline'}))
                self.fig_widget.update_layout(title_text=r"$f(x)=c_0\cdot e^{c_1\cdot x}$")
                if r2==True:
                    r2_score = tm.r2(y_values, y_pred)
                    print('R2-score:     ', r2_score)
            except:
                print('Selected regression might not be a good fit for the entered values! Please choose other regression!')

        elif trend=='manual':
            try:
                coefs = tm.freeReg(x_values,y_values, expression)
                print('coefficients: ', coefs)
                y_pred = tm.pred('freeReg', coefs, x_values, freeRegAnsatz=expression)
                self.fig_widget.update_traces(x=sorted_df[values_in], y=y_pred, selector=({'name':'trendline'}))
                self.fig_widget.update_layout(title_text=r"$f(x)=%s$" % sym.latex(eval(expression)))
                if r2==True:
                    r2_score = tm.r2(y_values, y_pred)
                    print('R2-score:     ', r2_score)
            except:
                print('Selected regression might not be a good fit for the entered values! Please choose other regression!')
        
        return  
    

            
    
    def show(self):
        
        display(self.fig_widget)
        
        return
        
        


