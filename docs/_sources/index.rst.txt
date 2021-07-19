Smart-Choice: Decision-Making Analysis Toolkit
===============================================================================


**Author**

| Prof. Juan David Velásquez-Henao, MSc, PhD
| Universidad Nacional de Colombia, Sede Medellín.
| jdvelasq@unal.edu.co



**What is it?**

**Smart-Choice** is a Python package for Decision-Making Analysis using decision trees. 
**Smart-Choice** allows the user to define a decision tree directly in Python. The 
best experience can be obtained when the package is used in a notebook 
inside of Jupyter Lab or Google Colab. **Smart-Choice** has no limits in the size 
of the decision tree created, and it can efficiently run large trees. 
Different reports are available to facilitate tree analysis.


**Main Features**


The package allows the user to define the following types of nodes in a decision
tree:

* Chance nodes.

* Decision nodes.

* End or Terminal nodes.

In the package, all model values and probabilities are entered directly as 
node properties using typical data structures in Python. Thus, an user with
a basic knowledge of the programming language can use effectively the 
package. 

A run of the decision tree can be used using monetary expected values, but, the 
following utility functions can be used to represent risk adversion:

* Exponential.

* Logarithmic.


Different types of analysis can be conducted easily, including:

* Decision analysis.

* Sensitivity analysis.

* Risk analysis.

For the terminal of end nodes, the user must supply Python functions to evaluate the
value of the node. This feature allows the user to use all capacity of Python
programming language. It is possibe to write functions to run a complete Monte Carlo 
simulation using other packages as scipy. In other scenarios, it is possible to 
build complex predictive models that feed the decision model using, for example, 
scikit-learn. Other great adventage of the **Smart-Choice** is velocity where it is compared
with spreadsheets; it is possible to run complex models in a 
fraction of the time required when a spreadsheet is used. 


**Release Information**


* Date:   July 21, 2021  **Version**: 0.1.0


* Binary Installers:  `<https://pypi.org/project/smart-choice>`_


* Source Repository:  `<https://github.com/jdvelasq/smart-choice>`_


* Documentation:  `<https://jdvelasq.github.io/smart-choice/>`_


.. toctree::
   :maxdepth: 1

   installation
   reference
   



