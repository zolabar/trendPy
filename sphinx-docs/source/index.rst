.. trendPy-main documentation master file, created by
   sphinx-quickstart on Mon Jul  4 14:34:02 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to TrendPy's documentation!
===================================
The TrendPy Python package was created by the
university course WW21DSB of the Cooperative State University Mannheim (DHBW) in collaboration with the lecturer Zoufiné Lauer-Baré. The package offers you a bunch of helpful methods
which will allow you to create powerful time series regressions for your python project on a very easy way.

With this documentation you will get a simple step by step introduction to the trendPy package
and you will learn how to use this package with all its included methods for your very own project.

The full trendPy github repository can be found `here <https://github.com/zolabar/trendPy>`_.

The trendpy2 package makes it easy to approxmiate time series regressions in a determinstic way. The trendpy2 package supports you to easily fit your data. The following trends are supported:

* linear :math:`f(x)=a\cdot x+b`
* polynomial :math:`f(x)=a_n\cdot x^n+a_{n-1}\cdot x^{n-1}+...+a_0`
* exponential :math:`f(x)=a\cdot e^{b\cdot x}`
* trigonometric :math:`f(x)=a\cdot \cos(2\cdot \pi\cdot b\cdot x+c)`
* "free", for max. three parameters, e.g. (the intial guess for a, b, c is 1.)
    - :math:`a \cdot \arctan(b\cdot x+c)`
    - :math:`a\cdot \exp(b\cdot x)`
    - :math:`a\cdot x` 

trendpy2 is deterministic, i.e. complementary to `trendpy <https://github.com/RonsenbergVI/trendpy>`_, which uses a stochastic approach.

A standalone feature of the trendpy2 package is, that it combines least-squares approaches, Fourier analysis approaches, numerical Python packages as Numpy and Scipy
and the symbolic Python package Sympy for time series regressions.

Thanks to he web near visualization package Plotly, the web apps allow a smoth interative experience!


..                   Panel buttons for navigation to "getting started" or "trendPy package"
.. --------------------------------------------------------------------------------------------------

.. panels::

   From installation to advanced usage of the package. A step by step introduction into TrendPy.

  .. link-button:: getting_started
     :type: ref
     :text: getting started
     :classes: btn-outline-primary btn-block stretched-link
   ---

   Take a look inside the code of a specific method of the trendPy package.

  .. link-button:: trendPyPackage
     :type: ref
     :text: modules
     :classes: btn-outline-primary btn-block stretched-link


.. -------------------------------------------------------------------------------------------------
..                                 Table of Contents (visible on the lft)

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: trendPy:

   getting_started
   trendPyPackage



.. ------------------------------------------------------------------------------------------------



