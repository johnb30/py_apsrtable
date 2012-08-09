def createModel(model):
    """
    Takes the model to be placed in the table, turns it into a list, and determines the number of models.

    Parameters
    ----------
    model : The model to be placed into the table, object. These should be pandas Series objects generated using statsmodel.

    Returns
    -------
    output : A dict with each variable name as the key and the beta values and standard erros as the values. 

    """
    params = dict(model.params)
    bse = dict(model.bse)
    pvals = dict(model.pvalues)
    output = dict((k, [params[k], bse.get(k), pvals.get(k)]) for k in sorted(params.iterkeys()))
    return output 
    
def startTable(file, caption, label, model_name=None, model_number=1, center='True'):
    #TODO: Add support for multiple models.
    #TODO: Move the tableSize calculation to the createModel function? Or it's own helper function?
    """
    Generates the top, or header, portion of a LaTeX table.

    Parameters
    ----------
    file : The output file to be written to, string.

    caption : The caption for the table (e.g. "OLS Results"), string. 

    label : The LaTeX label for the table (e.g. "tab:ols"), string. 

    model_name : Name of the model, string. Optional.

    model_number : Not needed for now. This will be used as the script expands.

    center : Whether or not the LaTeX table should be centered, boolean.

    Output
    ------
    Writes the header of the LaTeX table to the indicated file. 
    """
    file = open(file, 'w')
    tableSize = 'c '*(model_number)+'c'
    if model_name == None:
        name = 'Model 1'
    elif type(model_name) == str:
        name =  model_name
    else:
        print 'Please enter a valid string for the model_name, or let the name default to "Model 1"'
    if center == 'True':
        header = """
\\begin{table}
\caption{%s}
\center
\label{%s}
\\begin{center}
\\begin{tabular}{%s}
\hline\hline
&      %s\\\\
\hline
        """ % (caption, label, tableSize, name)
    elif center == 'False':
        header = """
\\begin{table}
\caption{%s}
\label{%s}
\\begin{tabular}{%s}
\hline\hline
%s
\hline
        """ % (caption, label, tableSize, name)
    else:
        print 'Please enter a valid string ("True" or "False") for the center argument'
    file.write(header)
    file.close()


def modelTable(file, model, parens='se'):
    #TODO: Do something to the variable names and label them generically...ie x1, x2
    #TODO: add support for changing of variable names
    """
    Generates the middle, which contains the actual model, of the LaTeX table using the model generated in the createModel function.

    Parameters
    ----------
    file : File to write the output to, string. Same as in the startTable function.

    model : The model to be placed into the table, dict. The dict generated by the createModel function.

    parens : Which values to put in the parentheses, string. Valid entries are 'se' for standard errors, 'pval' for two-tailed p values, and 'pval_one' for one-tailed p-values 

    Outputs
    -------
    Writes the middle of the LaTeX, which contains the actual model information, to the output file.
    """
    if type(model) == dict:
        if parens == 'se':
            file = open(file, 'a')                    
            for key, value in sorted(model.iteritems()):
                model = str(key) + '  &  ' + str(round(value[0],2)) + ' \\\\ \n     &     ' + '(' + str(round(value[1],2)) + ')' + ' \\\\ \n'
                file.write(model)            
            file.close()
        elif parens == 'pval':
            file = open(file, 'a')
            for key, value in sorted(model.iteritems()):
                if round(value[2],2) <= .05: 
                    model = str(key) + '  &  ' + str(round(value[0],2)) + ' \\\\ \n     &     ' + '(' + str(round(value[2],2)) + '*)' + ' \\\\ \n'
                    file.write(model)
                elif round(value[2],2) > .05:
                    model = str(key) + '  &  ' + str(round(value[0],2)) + ' \\\\ \n     &     ' + '(' + str(round(value[2],2)) + ')' + ' \\\\ \n'
                    file.write(model)  
            file.close()
        elif parens == 'pval_one':
            file = open(file, 'a')
            for key, value in sorted(model.iteritems()):
                if round((value[2]/2.)) <= .05:
                    model = str(key) + '  &  ' + str(round(value[0],2)) + ' \\\\ \n     &     ' + '(' + str(round((value[2]/2.),2)) + '*)' + ' \\\\ \n'
                    file.write(model)
                elif round((value[2]/2.)) > .05:
                    model = str(key) + '  &  ' + str(round(value[0],2)) + ' \\\\ \n     &     ' + '(' + str(round((value[2]/2.),2)) + '*)' + ' \\\\ \n'
                    file.write(model)
            file.close()
        else:
            print 'Please input a valid entry for the parens argument'
    else:
        print 'Please input a dict object for the model'

                  
def endTable(file, tableSize=2, center='True', parens='se'):
    """
    Generates the bottom, or footer, portion of a LaTeX table.

    Parameters
    ----------
    file : The output file to be written to, string.

    tableSize : The size of the table, int. Should remain 2 for now, will be used when the script expands to support more models. 
    
    center : Whether or not the LaTeX table is centered, boolean.

    parens : What values are included in the parentheses in the model portion generated by the modelTable function. Options are 'se', 'pval', 'pval_one'. 

    Output
    ------
    Writes the footer to the output table. 
    
    """

    file = open(file, 'a')
    if center == 'True':
        if parens == 'se':
            footer = """
\hline
\multicolumn{%d}{l}{\\footnotesize{Standard Errors in parentheses}}\\\\
\multicolumn{%d}{l}{\\footnotesize{$^*$ indicates significance at $p \le$ 0.05 }} 
\end{tabular}
\end{center}
\end{table}
            """ % (tableSize, tableSize)
        elif parens == 'pval':
            footer = """
\hline
\multicolumn{%d}{l}{\\footnotesize{$p$ values in parentheses}}\\\\
\multicolumn{%d}{l}{\\footnotesize{$^*$ indicates significance at $p \le$ 0.05 }} 
\end{tabular}
\end{center}
\end{table}
            """ % (tableSize, tableSize)
        elif parens == 'pval_one':
            footer = """
\hline
\multicolumn{%d}{l}{\\footnotesize{One-tailed $p$ values in parentheses}}\\\\
\multicolumn{%d}{l}{\\footnotesize{$^*$ indicates significance at $p \le$ 0.05 }} 
\end{tabular}
\end{center}
\end{table}
            """ % (tableSize, tableSize)
        else:
            print 'Please input a valid entry for the parens argument'
    elif center == 'False':
        footer = """
\hline
\multicolumn{%d}{l}{\\footnotesize{Standard Errors in parentheses}}\\\\
\multicolumn{%d}{l}{\\footnotesize{$^*$ indicates significance at $p \le$ 0.05 }} 
\end{tabular}
\end{table}
            """ % (tableSize, tableSize)
    file.write(footer)
    file.close()
    else:
        print 'Please input a valid entry for the center argument'


    


