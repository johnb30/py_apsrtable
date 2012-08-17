class generateTable(object):
    
    def __init__(self, output, models, center='True', parens='se', var_names=None):
        """
        Parameters
        ----------
        output : File to write the table to, string.

        models : Models to placed in the LaTeX table, list. This should be a list of pandas object generated by statsmodels.

        center : Whether the table should be centered or not, boolean. Defaults to 'True'

        parens : What values should be in the parentheses, string. Options are 'se' for standard errors, 'pval' for p values, and 'pval_one' for one-tailed p values. Defaults to 'se'.

        var_names : Strings to be used as variable names, list. Optional. 

        Note
        ----

        When replacing the variable names it is important to look at the sorted ordering of the model (i.e. sorted(model.iteritems()) ) and order the list of replacement names accordingly. 

        """
        self.output = output
        self.models = models
        self.center = center
        self.parens = parens
        self.var_names = var_names

    def createModel(self):
        """
        Takes the model to be placed in the table, turns it into a list, and determines the number of models.

        Returns
        ------
        self.inputModel : A dict with each variable name as the key and a list of the beta values, standard errors, and p values for each model as the values. 

        """
        results = []
        for test_model in self.models:
            params = dict(test_model.params)
            bse = dict(test_model.bse)
            pvals = dict(test_model.pvalues)
            results.append(dict((k, [params[k], bse.get(k), pvals.get(k)]) for k in sorted(params.iterkeys())))
        tempModel = {}
        for key in results[0]:
            tempModel[key] = [results[0][key]]

        for model in results[1:len(results)]:
            for key in model:
                if key not in tempModel:
                    tempModel[key] = [['', '', '']]
        for i in range(1,len(results)):
            diff = set(tempModel) - set(results[i])
            for key in results[i]:
                tempModel[key].append(results[i][key])
            for key in diff:
                tempModel[key].append(['','',''])
        if self.var_names == None:
            self.inputModel = tempModel
        elif type(self.var_names) == list:
            replace = self.var_names
            newResults = []
            resultsList = sorted(tempModel.iteritems())
            for item in resultsList:
                newVar = list(item)
                newResults.append(newVar)
            for i in range(len(newResults)):
                newResults[i][0] = replace[i]
                self.inputModel = dict(newResults)

    def startTable(self, caption, label, model_name=None):
        """
        Generates the top, or header, portion of a LaTeX table.

        Parameters
        ----------
        caption : The caption for the table (e.g. "OLS Results"), string. 

        label : The LaTeX label for the table (e.g. "tab:ols"), string. 

        model_name : Name of the model, string. Optional. If not included model names default to 'Model 1', 'Model 2', etc.

        Output
        ------
        Writes the header of the LaTeX table to the indicated file. 
        
        """
        file = open(self.output, 'w')
        self.model_number = len(self.models)
        tableSize = 'c '*(self.model_number)+'c'
        if model_name == None:
            name = []
            for i in range(1, len(self.models)+1):
                name.append('Model ' + str(i))
            if self.center == 'True':
                header = """
\\begin{table}
\caption{%s}
\center
\label{%s}
\\begin{center}
\\begin{tabular}{%s}
\hline\hline
            """ % (caption, label, tableSize)
                for label in name:
                    header += '  &     %s' % (label)
                header += """
\\\\
\hline
"""
            elif self.center == 'False':
                header = """
\\begin{table}
\caption{%s}
\label{%s}
\\begin{tabular}{%s}
\hline\hline
            """ % (caption, label, tableSize)
                for label in name:
                    header += '  &     %s' % (label)
                header += """
\\\\
\hline
"""
            else:
                print 'Please enter a valid string ("True" or "False") for the center argument'
            file.write(header)
            file.close()
        elif len(self.models) == 1:
            name =  model_name
            if self.center == 'True':
                header = """
\\begin{table}
\caption{%s}
\center
\label{%s}
\\begin{center}
\\begin{tabular}{%s}
\hline\hline
     &   %s \\\\
\hline
            """ % (caption, label, tableSize)
                for label in name:
                    header += '  &     %s' % (label)
                header += """
\\\\
\hline
"""
            elif self.center == 'False':
                header = """
\\begin{table}
\caption{%s}
\label{%s}
\\begin{tabular}{%s}
\hline\hline
     &   %s \\\\
\hline
""" % (caption, label, tableSize)
                for label in name:
                    header += '  &     %s' % (label)
                header += """
\\\\
\hline
"""     
        elif len(self.models) > 1:
            name =  model_name
            if self.center == 'True':
                header = """
\\begin{table}
\caption{%s}
\center
\label{%s}
\\begin{center}
\\begin{tabular}{%s}
\hline\hline
""" % (caption, label, tableSize)
                for label in name:
                    header += '  &     %s' % (label)
                header += """\\\\
\hline
"""
            elif self.center == 'False':
                header = """
\\begin{table}
\caption{%s}
\label{%s}
\\begin{tabular}{%s}
\hline\hline
""" % (caption, label, tableSize)
                for label in name:
                    header += '  &     %s' % (label)
                header += """
\\\\
\hline
"""     
        else:
            print 'Please enter a valid list or string for model_name'


    def modelTable(self): 
        """
        Generates the middle, which contains the actual model, of the LaTeX table using the model generated in the createModel function.

        Outputs
        -------
        Writes the middle of the LaTeX, which contains the actual model information, to the output file.
        
        """
        if type(self.inputModel) == dict:
            if self.parens == 'se':
                file = open(self.output, 'a')                    
                text = ''
                for key in sorted(self.inputModel):
                    text += str(key)
                    for i in range(len(self.models)):
                        beta = self.inputModel[key][i][0]
                        if beta == '':
                            text += '  &   '
                        else:
                            int(beta)
                            text += '   &   ' +  str(round(beta,2))
                    text += """  \\\\  
                            """
                    for i in range(len(self.models)):
                        parens = self.inputModel[key][i][1]
                        if parens == '':
                            text += '  &   '
                        else:
                            if round(self.inputModel[key][i][2],2) <= .05:
                                int(parens)
                                text += '   &   ' +  '(' + str(round(parens,2)) + ')' + '*'
                            elif round(self.inputModel[key][i][2],2) > .05:
                                int(parens)
                                text += '   &   ' +  '(' + str(round(parens,2)) + ')'
                    text += """  \\\\
                            """
                file.write(text)            
                file.close()
            elif self.parens == 'pval':
                file = open(self.output, 'a')
                file = open(self.output, 'a')                    
                text = ''
                for key in sorted(self.inputModel):
                    text += str(key)
                    for i in range(len(self.models)):
                        beta = self.inputModel[key][i][0]
                        if beta == '':
                            text += '  &   '
                        else:
                            int(beta)
                            text += '   &   ' +  str(round(beta,2))
                    text += """  \\\\  
                            """

                    for i in range(len(self.models)):
                        parens = self.inputModel[key][i][2]
                        if parens == '':
                            text += '  &   '
                        else:
                            if round(self.inputModel[key][i][2],2) <= .05:
                                int(parens)
                                text += '   &   ' +  '(' + str(round(parens,2)) + ')' + '*'
                            elif round(self.inputModel[key][i][2],2) > .05:
                                int(parens)
                                text += '   &   ' +  '(' + str(round(parens,2)) + ')'
                    text += """  \\\\
                            """
                file.write(text)            
                file.close()
            elif self.parens == 'pval_one':
                file = open(self.output, 'a')                    
                text = ''
                for key in sorted(self.inputModel):
                    text += str(key)
                    for i in range(len(self.models)):
                        beta = self.inputModel[key][i][0]
                        if beta == '':
                            text += '  &   '
                        else:
                            int(beta)
                            text += '   &   ' +  str(round(beta,2))
                    text += """  \\\\  
                            """

                    for i in range(len(self.models)):
                        parens = (self.inputModel[key][i][2]/2.)
                        if parens == '':
                            text += '  &   '
                        else:
                            if round((self.inputModel[key][i][2]/2.),2) <= .05:
                                int(parens)
                                text += '   &   ' +  '(' + str(round(parens,2)) + ')' + '*'
                            elif round((self.inputModel[key][i][2]/2.),2) > .05:
                                int(parens)
                                text += '   &   ' +  '(' + str(round(parens,2)) + ')'
                    text += """  \\\\
                            """
                file.write(text)            
                file.close()
            else:
                print 'Please input a valid entry for the parens argument'
        else:
            print 'Please input a dict object for the model'

                      
    def endTable(self):
        """
        Generates the bottom, or footer, portion of a LaTeX table.

        Output
        ------
        Writes the footer to the output table. 
        
        """

        file = open(self.output, 'a')
        tableSize = self.model_number + 1
        if self.center == 'True':
            if self.parens == 'se':
                footer = """
\hline
\multicolumn{%d}{l}{\\footnotesize{Standard Errors in parentheses}}\\\\
\multicolumn{%d}{l}{\\footnotesize{$^*$ indicates significance at $p \le$ 0.05 }} 
\end{tabular}
\end{center}
\end{table}
                """ % (tableSize, tableSize)
            elif self.parens == 'pval':
                footer = """
\hline
\multicolumn{%d}{l}{\\footnotesize{$p$ values in parentheses}}\\\\
\multicolumn{%d}{l}{\\footnotesize{$^*$ indicates significance at $p \le$ 0.05 }} 
\end{tabular}
\end{center}
\end{table}
                """ % (tableSize, tableSize)
            elif self.parens == 'pval_one':
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
        elif self.center == 'False':
            footer = """
\hline
\multicolumn{%d}{l}{\\footnotesize{Standard Errors in parentheses}}\\\\
\multicolumn{%d}{l}{\\footnotesize{$^*$ indicates significance at $p \le$ 0.05 }} 
\end{tabular}
\end{table}
                """ % (tableSize, tableSize)
        file.write(footer)
        file.close()

    




