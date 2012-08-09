Overview
--------

py_apsrtable aims to be the python implemenation of the R package apsrtable (http://cran.r-project.org/web/packages/apsrtable/index.html).

Currently only one model per table is supported. Options for the model includes standard errors, two-tailed p values, and one-tailed p values.

In short, py_apsrtable is missing some of the functionality present in apsrtable, but provides some basis for generating well-formatted LaTeX output from python statiscal models.

Future
------

Long-term goals include support for multiple models, changing variable names, and changing header names. Also, I hope to integrate the functions into a class and make the flow more coherent.

Example
-------

Usage is as follows:
    
    #Imports
    import py_apsrtable
    import scikits.statsmodels.api as sm
    import pandas as pd

    #Generate some data to use
    data = sm.datasets.longley.load()
    df = pd.DataFrame(data.exog, columns=data.exog_name)
    y = data.endog
    df['intercept'] = 1.

    #Generate the OLS output and store it in olsresult
    olsresult = sm.OLS(y, df).fit()

    #Create the model to put used in py_apsrtable
    model = py_apsrtable.createModel(olsresult)

    #Generate the first portion of the table
    py_apsrtable.startTable('/path/to/file/table.tex', 'OLS Results Table', 'tab:ols', center='True', parens='se')

    #Middle of the table
    py_apsrtable.modelTable('/path/to/file/table.tex', model, parens='se')

    #Bottom of the table
    py_apsrtable.endTable('/path/to/file/table.tex', center='True', parens='se')


