============
py_apsrtable
============

Overview
--------

py_apsrtable aims to be the python implemenation of the R package apsrtable
(http://cran.r-project.org/web/packages/apsrtable/index.html).

py_asprtable takes as its input a model, or set of models, generated by the python packages statsmodels
(http://statsmodels.sourceforge.net/) and pandas (http://pandas.pydata.org/), and
outputs a LaTeX table formatted in a manner consistent with common political science
formatting. The formatting is also nice for other applications. 

Options for the models includes standard errors, two-tailed p values, and one-tailed p values. The variable and model names can be changed, and the stars (*) can be placed next to the values in parentheses if the p value is less than or equal to .05. 

Future
------

Currently the "magic" stars are only added for p values lower than .05. Eventually I would like to add an option to change the level at which the stars appear.
Maybe even have an option for having a different number of stars at different levels of p. None of these are particularly pressing for me. 


Example
-------

Usage for a single model::
    
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

    #Add the results to a list. The functions require the results to be in a list.
    models = [olsresult]

    #Check the order of the variable names
    print sorted(olsresult.params.iteritems())

    #Define the names to replace the variables
    replaceNames = ['Armed', 'Gross National Product', 'GNPDEFL', 'Population', 'Unemployment', 'Year', 'intercept']

    #Assign the generateTable class with the initial values
    a = py_apsrtable.generateTable('/path/to/file/table.tex', models, center = 'True', parens= 'se' , var_names = replaceNames)

    #Create the model to be used
    a.create_model()

    #Generate the first portion of the table
    a.start_table('OLS Results Table', 'tab:ols', model_name=None)

    #Middle of the table
    a.model_table(stars=True)

    #Bottom of the table
    a.end_table()

Usage for multiple models::

    #Imports
    import py_apsrtable
    import scikits.statsmodels.api as sm
    import pandas as pd

    #Generate some data to use
    data = sm.datasets.longley.load()
    df = pd.DataFrame(data.exog, columns=data.exog_name)
    y = data.endog
    df['intercept'] = 1.

    #Generate three separate models, each with different numbers of variables. 
    olsresult = sm.OLS(y, df).fit()
    olsresult2 = sm.OLS(y, df[['GNP', 'UNEMP', 'ARMED']]).fit()
    olsresult3 = sm.OLS(y, df[['GNP', 'POP', 'ARMED', 'YEAR']]).fit()

    #Put the models into a list
    models = [olsresult, olsresult2, olsresult3]

    #Check the order of the variable names
    print sorted(olsresult.params.iteritems())

    #Define the names to replace the variables
    replaceNames = ['Armed', 'Gross National Product', 'GNPDEFL', 'Population', 'Unemployment', 'Year', 'intercept']

    #Assign the generateTable class with the initial values
    a = py_apsrtable.generateTable('/path/to/file/table.tex', models, center = 'True', parens= 'se' , var_names = replaceNames)

    #Create the model to be used in py_apsrtable
    a.create_model()

    #Generate the first portion of the table
    a.start_table('OLS Results Table', 'tab:ols', model_name=None)

    #Middle of the table
    a.model_table(stars=True)

    #Bottom of the table
    a.end_table()



