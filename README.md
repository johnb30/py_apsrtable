Overview
--------

py_apsrtable aims to be the python implemenation of the R package apsrtable (http://cran.r-project.org/web/packages/apsrtable/index.html).

Currently only one model per table is supported. Options for the model includes standard errors, two-tailed p values, and one-tailed p values.

In short, py_apsrtable is missing some of the functionality present in apsrtable, but provides some basis for generating well-formatted LaTeX output from python statiscal models.

Future
------

Long-term goals include support for multiple models, changing variable names, and 
changing header names.

Updates
-------

08.15.12 Changed the structure of the file around. The functions are now within the
class generateTable. 

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

    #Assign the generateTable class with the initial values
    a = py_apsrtable.generateTable('/path/to/file/table.tex', olsresult, center='True', parens='se')

    #Create the model to put used in py_apsrtable
    model = a.createModel()

    #Generate the first portion of the table
    a.startTable('OLS Results Table', 'tab:ols')

    #Middle of the table
    a.modelTable(model)

    #Bottom of the table
    a.endTable()


