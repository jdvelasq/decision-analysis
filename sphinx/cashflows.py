r"""

>>> from hardDecisions.decisiontree import *
>>> from cashflows import *

>>> def my_credit(credit):
...     if credit == 0:
...         c = bullet_loan(amount=1000,
...                         nrate=interest_rate(const_value=10, periods=11, start=2019, freq='A'),
...                         dispoints=0,
...                         orgpoints=0,
...                         prepmt=None)
...     if credit == 1:
...         c = fixed_rate_loan(amount=1000, # monto
...                             nrate=10,    # tasa de interés
...                             freq='A',
...                             life=11,     # número de cuotas
...                             start=2019,
...                             grace=0,
...                             dispoints=0,
...                             orgpoints=0,
...                             prepmt=None,
...                             balloonpmt=None)
...     if credit == 2:
...         c = fixed_rate_loan(amount=1000, # monto
...                             nrate=9,    # tasa de interés
...                             freq='A',
...                             life=11,     # número de cuotas
...                             start=2019,
...                             grace=0,
...                             dispoints=2,
...                             orgpoints=1,
...                             prepmt=None,
...                             balloonpmt=None)
...     return sum(c.Int_Payment)


>>> tree = DecisionTree()

#0
>>> tree.decision_node(name='CREDIT',
...                    branches=[(  0,  1),
...                              (  1,  1),
...                              (  2,  1)],
...                    max=False)

>>> tree.terminal_node(expr='my_credit(CREDIT)')
>>> tree.display_nodes() # doctest: +NORMALIZE_WHITESPACE
Node 0
    Type: DECISION - Minimum Payoff
    Name: CREDIT
    Branches:
                    Value  Next Node
                    0.000  1
                    1.000  1
                    2.000  1
<BLANKLINE>
Node 1
    Type: TERMINAL
    Expr: my_credit(CREDIT)
<BLANKLINE>

>>> tree.build_tree()
>>> tree.evaluate(locals())
>>> tree.display_tree() # doctest: +NORMALIZE_WHITESPACE
|
| #0
| ExpVal=616.41
| (selected strategy)
\-------[D]
         |
         | #1
         | CREDIT=0
         | PathProb=0.00
         | ExpVal=1000.00
         +-------[T] my_credit(CREDIT)
         |
         | #2
         | CREDIT=1
         | PathProb=0.00
         | ExpVal=693.59
         +-------[T] my_credit(CREDIT)
         |
         | #3
         | CREDIT=2
         | PathProb=100.00
         | ExpVal=616.41
         | (selected strategy)
         \-------[T] my_credit(CREDIT)





"""
