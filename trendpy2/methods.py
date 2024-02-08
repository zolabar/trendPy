import numpy as np
from scipy.optimize import curve_fit
import sympy as sym
from sympy import atan as arctan
from sympy import sqrt, sin, cos, tan, exp, log, ln
a, b, c, x = sym.symbols('a, b, c, x', real=True)

def linReg(x_in,y):
    '''
    Time series linear regression. Returns coefs in polynomial descending order.
    Coefs computed analytically.
    
    Examples
    ========    
    
    >>> from trendpy2 import methods as tm
    >>> import numpy as np    
    >>> x = np.array([1, 2, 3])
    >>> y = np.array([1, 1.5, 3.5])
    >>> tm.linReg(x, y)    
    >>> [1.25, -0.5]
    '''
    
    a = (np.inner(x_in,y) - (len(x_in) * np.mean(x_in) * np.mean(y))) / (np.inner(x_in,x_in) - (len(x_in) * ((np.mean(x_in))**2)))
    b = np.mean(y) - a * np.mean(x_in)
    return [a,b]

def polReg(x_in,y, deg):
    '''
    Time series polynomial regression. Returns coefs in polynomial descending order.
    Coefs computed numerically.
    
    Examples
    ========    
    
    >>> from trendpy2 import methods as tm
    >>> import numpy as np    
    >>> x = np.array([0, 1, 2])
    >>> y = np.array([0, 2, 4])
    >>> tm.polReg(x, y, 2)  
    >>> array([ 8.96585976e-17,  2.00000000e+00, -9.55246329e-17])
    '''
    
    coefs = np.polyfit(x_in, y, deg)
    return coefs

def freeReg(x_in, y_out, ansatz):
    '''
    Regression with user ansatz. The ansatz is expected to depend on three
    parameters, a, b, and c. The ansatz is expected to be a string with a 
    symbolic formulation. for instance: 'a*arctan(b*x_in+c)'.
    
    Examples
    ========    
    
    >>> from trendpy2 import methods as tm
    >>> import numpy as np    
    >>> x = np.array([0, 1, 2, 3])
    >>> y = 2*(1-3*np.exp(-x))
    >>> tm.freeReg(x, y, ansatz='a*(1-b*exp(-c*x))')
    >>> array([2., 3., 1.])     
    '''    
    test_func = sym.lambdify((x, a, b, c), eval(ansatz))
    
    res = curve_fit(test_func, x_in, y_out)

    return res[0]    


def trigReg(x_in, y):
    '''
    Time series sine regression. Returns amplitude, frequency and phase.
    
    Examples
    ========    
    
    >>> from trendpy2 import methods as tm
    >>> import numpy as np    
    >>> x = np.linspace(0, 2, 50)
    >>> y = 2*np.cos(x*2*np.pi*3+2)
    >>> tm.trigReg(x, y)
    >>> array([1.93690845, 2.94      , 2.38548967])
    
    
    '''    
    timestep = x_in[1]-x_in[0]
    x_in = np.fft.fftfreq(len(x_in), timestep)
    Y = np.fft.fft(y)

    index = np.argmax(abs(Y))
    
    amplitude = 2*np.absolute(Y[index])/len(x_in)
    frequenz = abs(x_in[index])
    angle = np.angle(Y[index])    
    
    coefs = np.array([amplitude, frequenz, angle])
    
    return coefs

def expReg(x_in,y):
    '''
    Time series exponential regression. 
    
    Examples
    ========    
    
    >>> from trendpy2 import methods as tm
    >>> import numpy as np    
    >>> x = np.array([0, 1, 2])
    >>> y = 2*np.exp(x)
    >>> tm.expReg(x, y)
    >>> array([2., 1.])     
    
    
    '''
    coef_first_step = linReg(x_in,np.log(y))
    b = coef_first_step[0]
    a = np.exp(coef_first_step[1])
    return [a,b]

def pred(ansatz, coef, x_in, freeRegAnsatz=None):
    '''
    Computes the predction for input x_in and the computed corresponding
    coefficients.
    ''' 
        
    if ansatz == 'linReg' or ansatz == 'polReg':
        values = np.poly1d(coef)(x_in)     
            
    if ansatz == 'trigReg':
        amplitude, frequenz, angle = coef
        values = amplitude*np.cos(2*np.pi*frequenz*x_in+angle)  
        
    if ansatz == 'expReg':
        values = coef[0]*np.exp(coef[1]*x_in) 
        
    if ansatz == 'freeReg':
        #print(eval(freeRegAnsatz))
        f = eval(freeRegAnsatz).subs(a, coef[0]).subs(b, coef[1]).subs(c, coef[2])
        f_num = sym.lambdify(x, f)       
        values = f_num(x_in)
        
        
    return  values 

def r2(y, y_pred):
        '''
        Coefficient of determination.
        '''
        wert = 1-np.sum((y-y_pred)**2)/np.sum((y-np.mean(y))**2)
        return wert


