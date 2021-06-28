# DMAK: Decision Making Analysis Toolkit


What is it?
------------------------------------------------------------------------------------

**DMAK** is a Python package for Decision-Making Analysis using decision trees. 
**DMAK** allows the user to represent decision-making scenarios using different types
of nodes in a decision tree.


Main Features
------------------------------------------------------------------------------------

The package allows the user to define the following types of nodes in a decision
tree:

* Chance nodes.

* Decision nodes.

* End or Terminal nodes.

A run of the decision tree can be used using monetary expected values, but, the 
following utility functions can be used to represent risk adversion:

* Exponential.

* Logarithmic.

* Squared root.

Different types of analysis can be conducted easily, including:

* Decision analysis.

* Sensitivity analysis.

* Risk analysis.

For the terminal of end nodes, the user must supply Python functions to evaluate the
value of the node. This feature allows the user to use all capacity of Python
programming language. It is possibe to write functions to run a complete Monte Carlo 
simulation using other packages as scipy. In other scenarios, it is possible to 
build complex predictive models that feed the decision model using, for example, 
scikit-learn. Other great adventage of the **DMAK** is velocity where it is compared
with spreadsheets; in this sense, it is possible to run complex models in a 
fraction of the time required when a spreadsheet is used. 



Installation
------------------------------------------------------------------------------------

The current stable version can be installed from the command line using:

```bash
$ pip install dmak
``` 

at the command prompt.


Documentation
------------------------------------------------------------------------------------

Available at: https://jdvelasq.github.io/dmak


