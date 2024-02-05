<img src="figures/gallery_logo.PNG"  height="300"  />

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7009281.svg)](https://doi.org/10.5281/zenodo.7009281) Jupyter Lab:   [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/zolabar/trendPy/HEAD) Documentation: [![doc](https://img.shields.io/badge/Made%20with-Sphinx-1f425f.svg)](https://zolabar.github.io/trendPy/) WebApps: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/zolabar/trendPy/experimental?urlpath=voila%2Frender%2F/trendpy_webapp.ipynb) (binder) [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://zolabar-trendpy-trendpy2-app-kfqshb.streamlit.app/)

# Usage

```pip install trendpy2``` 

and use it as **trendpy2** as shown in the ```example.ipynb``` and approximate your time series with the following trends

* linear $f(x)=a\cdot x+b$
* polynomial $f(x)=a_n\cdot x^n+a_{n-1}\cdot x^{n-1}+...+a_0$
* exponential $f(x)=a\cdot e^{b\cdot x}$
* trigonometric $f(x)=a\cdot \cos(2\cdot \pi\cdot b\cdot x+c)$
* "free" (for max. three parameters) (e.g.```a*arctan(b*x+c)```, ```a*exp(b*x+c)```, ```a*(x*b)+c```), the intial guess for a, b, c is 1.

in your Python scripts or jupyter notebooks and use the best of the numerical and symbolic worlds to make predictions and assess the quality of your fit!

or use the one of the **WebApps** with the correspondig button above (voila app or streamlit app).

For more, have a look at the [**sphinx-documentation**](https://zolabar.github.io/trendPy/)!

### Voila App

<img src="figures/screenshot3.PNG"  />

### Streamlit App

<img src="figures/streamlit_app.png"  />

