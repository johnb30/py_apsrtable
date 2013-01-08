============
py_apsrtable
============

Overview
--------

py_apsrtable aims to be the python implemenation of the R package apsrtable
(http://cran.r-project.org/web/packages/apsrtable/index.html).

py_asprtable takes as its input a model, or set of models, generated by the 
python packages statsmodels (http://statsmodels.sourceforge.net/) and pandas
(http://pandas.pydata.org/), and outputs a LaTeX table formatted in a manner
consistent with common political science formatting.
The formatting is also nice for other applications. 

Options for the models includes standard errors, two-tailed p values, and 
one-tailed p values. The variable and model names can be changed, and the stars
(*) can be placed next to the values in parentheses depending on the
significance level defined by the user. 

Updates
-------

#####01.07.13

- Added the ability to print the table to the Python shell instead of writing to
  a file. 

#####01.02.13

- Simplified the execution down to one function.
- Added the ability to change the signficance level.
- Refactored the code some to be cleaner. 

Future
------

The N and other statistics need to be reported at the bottom of the table.

Eventually I would like to add an option to add a different number of stars for
different p-values. 

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
    replaceNames = ['Armed', 'Gross National Product', 'GNPDEFL', 'Population', 
    'Unemployment', 'Year', 'intercept']

    #Assign the generateTable class with the initial values
    #Print is an alternate option for the output argument
    a = py_apsrtable.generateTable('/path/to/file/table.tex', models, 
    center = 'True', parens= 'se', sig_level=0.05, var_names = replaceNames)

    #Create the table
    a.create_table(caption='OLS Results Table', label='tab:ols', model_name = None, stars=True)

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
    replaceNames = ['Armed', 'Gross National Product', 'GNPDEFL', 'Population', 
    'Unemployment', 'Year', 'intercept']

    #Assign the generateTable class with the initial values
    a = py_apsrtable.generateTable('print', models, center = 'True', parens= 'se', sig_level=0.10, var_names = replaceNames)

    #Create the table
    a.create_table(caption='OLS Results Table', lable='tab:ols', model_name = None, stars=True)

An example of the final PDF output generated by the above code can be seen 
[here](http://johnbeieler.org/code/downloads/example.pdf).

