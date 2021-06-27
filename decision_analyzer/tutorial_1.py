r"""
Building a simple decision tree
===============================================================================

**Creation of the nodes.**

>>> from decision_analyzer.nodes import Nodes
>>> nodes = Nodes()
>>> nodes.decision(
...     name="BID",
...     branches=[
...         (500, "COMPBID"),
...         (700, "COMPBID"),
...     ],
...     max_=True,
... )

>>> nodes.chance(
...     name='COMPBID',
...     branches=[
...         (35.0,  400,  "PROFIT"),
...         (50.0,  600,  "PROFIT"),
...         (15.0,  800,  "PROFIT")
...    ]
... )

>>> nodes.terminal(
...     name="PROFIT",
...     user_fn=None,
... )

>>> nodes
Node 0
    Type: DECISION - Maximum Payoff
    Name: BID
    Branches:
                         Value  Next Node
                       500.000  COMPBID
                       700.000  COMPBID
<BLANKLINE>
Node 1
    Type: CHANCE
    Name: COMPBID
    Branches:
          Chance         Value  Next Node
           35.00       400.000  PROFIT
           50.00       600.000  PROFIT
           15.00       800.000  PROFIT
<BLANKLINE>
Node 2
    Type: TERMINAL
    Name: PROFIT
    User fn: (cumulative)
<BLANKLINE>


**Tree creation and building.**

>>> from decision_analyzer.decisiontree import DecisionTree
>>> tree = DecisionTree(variables=nodes, initial_variable="BID")
>>> tree.build()

**Visualization as text.**

>>> print(tree.export_text())
|
| #0
\-------[D]
         |
         | #1
         | BID=500
         +-------[C]
         |        |
         |        | #2
         |        | COMPBID=400
         |        | Prob=35.00
         |        +-------[T] PROFIT
         |        |
         |        | #3
         |        | COMPBID=600
         |        | Prob=50.00
         |        +-------[T] PROFIT
         |        |
         |        | #4
         |        | COMPBID=800
         |        | Prob=15.00
         |        |-------[T] PROFIT
         |
         | #5
         | BID=700
         \-------[C]
                  |
                  | #6
                  | COMPBID=400
                  | Prob=35.00
                  +-------[T] PROFIT
                  |
                  | #7
                  | COMPBID=600
                  | Prob=50.00
                  +-------[T] PROFIT
                  |
                  | #8
                  | COMPBID=800
                  | Prob=15.00
                  \-------[T] PROFIT


"""
