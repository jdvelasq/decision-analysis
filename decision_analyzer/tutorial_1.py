r"""
Building a simple decision tree
===============================================================================

**Profit function.**

PROFIT = (BID-COST) * (1 if BID < COMPBID else 0)

>>> def profit(BID, COST, COMPBID):
...     return (BID - COST) * (1 if BID < COMPBID else 0)




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
...         (35.0,  400,  "COST"),
...         (50.0,  600,  "COST"),
...         (15.0,  800,  "COST")
...     ]
... )

>>> nodes.chance(
...     name='COST',
...     branches=[
...         (25.0,  200,  "PROFIT"),
...         (50.0,  400,  "PROFIT"),
...         (25.0,  600,  "PROFIT"),
...     ]
... )


>>> nodes.terminal(
...     name="PROFIT",
...     user_fn=profit,
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
           35.00       400.000  COST
           50.00       600.000  COST
           15.00       800.000  COST
<BLANKLINE>
Node 2
    Type: CHANCE
    Name: COST
    Branches:
          Chance         Value  Next Node
           25.00       200.000  PROFIT
           50.00       400.000  PROFIT
           25.00       600.000  PROFIT
<BLANKLINE>
Node 3
    Type: TERMINAL
    Name: PROFIT
    User fn: (User fn)
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
         |        +-------[C]
         |        |        |
         |        |        | #3
         |        |        | COST=200
         |        |        | Prob=25.00
         |        |        +-------[T] PROFIT
         |        |        |
         |        |        | #4
         |        |        | COST=400
         |        |        | Prob=50.00
         |        |        +-------[T] PROFIT
         |        |        |
         |        |        | #5
         |        |        | COST=600
         |        |        | Prob=25.00
         |        |        \-------[T] PROFIT
         |        |
         |        | #6
         |        | COMPBID=600
         |        | Prob=50.00
         |        +-------[C]
         |        |        |
         |        |        | #7
         |        |        | COST=200
         |        |        | Prob=25.00
         |        |        +-------[T] PROFIT
         |        |        |
         |        |        | #8
         |        |        | COST=400
         |        |        | Prob=50.00
         |        |        +-------[T] PROFIT
         |        |        |
         |        |        | #9
         |        |        | COST=600
         |        |        | Prob=25.00
         |        |        \-------[T] PROFIT
         |        |
         |        | #10
         |        | COMPBID=800
         |        | Prob=15.00
         |        \-------[C]
         |                 |
         |                 | #11
         |                 | COST=200
         |                 | Prob=25.00
         |                 +-------[T] PROFIT
         |                 |
         |                 | #12
         |                 | COST=400
         |                 | Prob=50.00
         |                 +-------[T] PROFIT
         |                 |
         |                 | #13
         |                 | COST=600
         |                 | Prob=25.00
         |                 \-------[T] PROFIT
         |
         | #14
         | BID=700
         \-------[C]
                  |
                  | #15
                  | COMPBID=400
                  | Prob=35.00
                  +-------[C]
                  |        |
                  |        | #16
                  |        | COST=200
                  |        | Prob=25.00
                  |        +-------[T] PROFIT
                  |        |
                  |        | #17
                  |        | COST=400
                  |        | Prob=50.00
                  |        +-------[T] PROFIT
                  |        |
                  |        | #18
                  |        | COST=600
                  |        | Prob=25.00
                  |        \-------[T] PROFIT
                  |
                  | #19
                  | COMPBID=600
                  | Prob=50.00
                  +-------[C]
                  |        |
                  |        | #20
                  |        | COST=200
                  |        | Prob=25.00
                  |        +-------[T] PROFIT
                  |        |
                  |        | #21
                  |        | COST=400
                  |        | Prob=50.00
                  |        +-------[T] PROFIT
                  |        |
                  |        | #22
                  |        | COST=600
                  |        | Prob=25.00
                  |        \-------[T] PROFIT
                  |
                  | #23
                  | COMPBID=800
                  | Prob=15.00
                  \-------[C]
                           |
                           | #24
                           | COST=200
                           | Prob=25.00
                           +-------[T] PROFIT
                           |
                           | #25
                           | COST=400
                           | Prob=50.00
                           +-------[T] PROFIT
                           |
                           | #26
                           | COST=600
                           | Prob=25.00
                           \-------[T] PROFIT



**Tree evaluation.**

>>> tree.evaluate()
>>> print(tree.export_text())

"""
