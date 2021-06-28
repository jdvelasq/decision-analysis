r"""
Building a decision tree (based on SuperTree)
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
>>> tree.print_nodes()
#0   {'name': 'BID', 'type': 'DECISION', 'max': True, 'successors': [1, 14]}
#1   {'name': 'COMPBID', 'type': 'CHANCE', 'successors': [2, 6, 10], 'tag_name': 'BID', 'tag_value': 500}
#2   {'name': 'COST', 'type': 'CHANCE', 'successors': [3, 4, 5], 'tag_name': 'COMPBID', 'tag_value': 400, 'tag_prob': 35.0}
#3   {'name': 'PROFIT', 'type': 'TERMINAL', 'tag_name': 'COST', 'tag_value': 200, 'tag_prob': 25.0}
#4   {'name': 'PROFIT', 'type': 'TERMINAL', 'tag_name': 'COST', 'tag_value': 400, 'tag_prob': 50.0}
#5   {'name': 'PROFIT', 'type': 'TERMINAL', 'tag_name': 'COST', 'tag_value': 600, 'tag_prob': 25.0}
#6   {'name': 'COST', 'type': 'CHANCE', 'successors': [7, 8, 9], 'tag_name': 'COMPBID', 'tag_value': 600, 'tag_prob': 50.0}
#7   {'name': 'PROFIT', 'type': 'TERMINAL', 'tag_name': 'COST', 'tag_value': 200, 'tag_prob': 25.0}
#8   {'name': 'PROFIT', 'type': 'TERMINAL', 'tag_name': 'COST', 'tag_value': 400, 'tag_prob': 50.0}
#9   {'name': 'PROFIT', 'type': 'TERMINAL', 'tag_name': 'COST', 'tag_value': 600, 'tag_prob': 25.0}
#10  {'name': 'COST', 'type': 'CHANCE', 'successors': [11, 12, 13], 'tag_name': 'COMPBID', 'tag_value': 800, 'tag_prob': 15.0}
#11  {'name': 'PROFIT', 'type': 'TERMINAL', 'tag_name': 'COST', 'tag_value': 200, 'tag_prob': 25.0}
#12  {'name': 'PROFIT', 'type': 'TERMINAL', 'tag_name': 'COST', 'tag_value': 400, 'tag_prob': 50.0}
#13  {'name': 'PROFIT', 'type': 'TERMINAL', 'tag_name': 'COST', 'tag_value': 600, 'tag_prob': 25.0}
#14  {'name': 'COMPBID', 'type': 'CHANCE', 'successors': [15, 19, 23], 'tag_name': 'BID', 'tag_value': 700}
#15  {'name': 'COST', 'type': 'CHANCE', 'successors': [16, 17, 18], 'tag_name': 'COMPBID', 'tag_value': 400, 'tag_prob': 35.0}
#16  {'name': 'PROFIT', 'type': 'TERMINAL', 'tag_name': 'COST', 'tag_value': 200, 'tag_prob': 25.0}
#17  {'name': 'PROFIT', 'type': 'TERMINAL', 'tag_name': 'COST', 'tag_value': 400, 'tag_prob': 50.0}
#18  {'name': 'PROFIT', 'type': 'TERMINAL', 'tag_name': 'COST', 'tag_value': 600, 'tag_prob': 25.0}
#19  {'name': 'COST', 'type': 'CHANCE', 'successors': [20, 21, 22], 'tag_name': 'COMPBID', 'tag_value': 600, 'tag_prob': 50.0}
#20  {'name': 'PROFIT', 'type': 'TERMINAL', 'tag_name': 'COST', 'tag_value': 200, 'tag_prob': 25.0}
#21  {'name': 'PROFIT', 'type': 'TERMINAL', 'tag_name': 'COST', 'tag_value': 400, 'tag_prob': 50.0}
#22  {'name': 'PROFIT', 'type': 'TERMINAL', 'tag_name': 'COST', 'tag_value': 600, 'tag_prob': 25.0}
#23  {'name': 'COST', 'type': 'CHANCE', 'successors': [24, 25, 26], 'tag_name': 'COMPBID', 'tag_value': 800, 'tag_prob': 15.0}
#24  {'name': 'PROFIT', 'type': 'TERMINAL', 'tag_name': 'COST', 'tag_value': 200, 'tag_prob': 25.0}
#25  {'name': 'PROFIT', 'type': 'TERMINAL', 'tag_name': 'COST', 'tag_value': 400, 'tag_prob': 50.0}
#26  {'name': 'PROFIT', 'type': 'TERMINAL', 'tag_name': 'COST', 'tag_value': 600, 'tag_prob': 25.0}


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



**Subtree export.**

>>> print(tree.export_text(max_deep=0))
|
| #0
\-------[D]


>>> print(tree.export_text(max_deep=1))
|
| #0
\-------[D]
         |
         | #1
         | BID=500
         +-------[C]
         |
         | #14
         | BID=700
         \-------[C]


>>> print(tree.export_text(max_deep=2))
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
         |        |
         |        | #6
         |        | COMPBID=600
         |        | Prob=50.00
         |        +-------[C]
         |        |
         |        | #10
         |        | COMPBID=800
         |        | Prob=15.00
         |        \-------[C]
         |
         | #14
         | BID=700
         \-------[C]
                  |
                  | #15
                  | COMPBID=400
                  | Prob=35.00
                  +-------[C]
                  |
                  | #19
                  | COMPBID=600
                  | Prob=50.00
                  +-------[C]
                  |
                  | #23
                  | COMPBID=800
                  | Prob=15.00
                  \-------[C]
  

**Tree evaluation.**

>>> tree.evaluate()

>>> print(tree.export_text())
|
| #0
| ExpVal=65.00
| (selected strategy)
\-------[D]
         |
         | #1
         | BID=500
         | ExpVal=65.00
         | (selected strategy)
         +-------[C]
         |        |
         |        | #2
         |        | COMPBID=400
         |        | Prob=35.00
         |        | ExpVal=0.00
         |        | (selected strategy)
         |        +-------[C]
         |        |        |
         |        |        | #3
         |        |        | COST=200
         |        |        | Prob=25.00
         |        |        | PathProb=8.75
         |        |        | (selected strategy)
         |        |        +-------[T] PROFIT=0.00
         |        |        |
         |        |        | #4
         |        |        | COST=400
         |        |        | Prob=50.00
         |        |        | PathProb=17.50
         |        |        | (selected strategy)
         |        |        +-------[T] PROFIT=0.00
         |        |        |
         |        |        | #5
         |        |        | COST=600
         |        |        | Prob=25.00
         |        |        | PathProb=8.75
         |        |        | (selected strategy)
         |        |        \-------[T] PROFIT=0.00
         |        |
         |        | #6
         |        | COMPBID=600
         |        | Prob=50.00
         |        | ExpVal=100.00
         |        | (selected strategy)
         |        +-------[C]
         |        |        |
         |        |        | #7
         |        |        | COST=200
         |        |        | Prob=25.00
         |        |        | PathProb=12.50
         |        |        | (selected strategy)
         |        |        +-------[T] PROFIT=300.00
         |        |        |
         |        |        | #8
         |        |        | COST=400
         |        |        | Prob=50.00
         |        |        | PathProb=25.00
         |        |        | (selected strategy)
         |        |        +-------[T] PROFIT=100.00
         |        |        |
         |        |        | #9
         |        |        | COST=600
         |        |        | Prob=25.00
         |        |        | PathProb=12.50
         |        |        | (selected strategy)
         |        |        \-------[T] PROFIT=-100.00
         |        |
         |        | #10
         |        | COMPBID=800
         |        | Prob=15.00
         |        | ExpVal=100.00
         |        | (selected strategy)
         |        \-------[C]
         |                 |
         |                 | #11
         |                 | COST=200
         |                 | Prob=25.00
         |                 | PathProb=3.75
         |                 | (selected strategy)
         |                 +-------[T] PROFIT=300.00
         |                 |
         |                 | #12
         |                 | COST=400
         |                 | Prob=50.00
         |                 | PathProb=7.50
         |                 | (selected strategy)
         |                 +-------[T] PROFIT=100.00
         |                 |
         |                 | #13
         |                 | COST=600
         |                 | Prob=25.00
         |                 | PathProb=3.75
         |                 | (selected strategy)
         |                 \-------[T] PROFIT=-100.00
         |
         | #14
         | BID=700
         | ExpVal=45.00
         \-------[C]
                  |
                  | #15
                  | COMPBID=400
                  | Prob=35.00
                  | ExpVal=0.00
                  +-------[C]
                  |        |
                  |        | #16
                  |        | COST=200
                  |        | Prob=25.00
                  |        | PathProb=0.00
                  |        +-------[T] PROFIT=0.00
                  |        |
                  |        | #17
                  |        | COST=400
                  |        | Prob=50.00
                  |        | PathProb=0.00
                  |        +-------[T] PROFIT=0.00
                  |        |
                  |        | #18
                  |        | COST=600
                  |        | Prob=25.00
                  |        | PathProb=0.00
                  |        \-------[T] PROFIT=0.00
                  |
                  | #19
                  | COMPBID=600
                  | Prob=50.00
                  | ExpVal=0.00
                  +-------[C]
                  |        |
                  |        | #20
                  |        | COST=200
                  |        | Prob=25.00
                  |        | PathProb=0.00
                  |        +-------[T] PROFIT=0.00
                  |        |
                  |        | #21
                  |        | COST=400
                  |        | Prob=50.00
                  |        | PathProb=0.00
                  |        +-------[T] PROFIT=0.00
                  |        |
                  |        | #22
                  |        | COST=600
                  |        | Prob=25.00
                  |        | PathProb=0.00
                  |        \-------[T] PROFIT=0.00
                  |
                  | #23
                  | COMPBID=800
                  | Prob=15.00
                  | ExpVal=300.00
                  \-------[C]
                           |
                           | #24
                           | COST=200
                           | Prob=25.00
                           | PathProb=0.00
                           +-------[T] PROFIT=500.00
                           |
                           | #25
                           | COST=400
                           | Prob=50.00
                           | PathProb=0.00
                           +-------[T] PROFIT=300.00
                           |
                           | #26
                           | COST=600
                           | Prob=25.00
                           | PathProb=0.00
                           \-------[T] PROFIT=100.00



>>> print(tree.export_text(strategy=True))
|
| #0
| ExpVal=65.00
| (selected strategy)
\-------[D]
         |
         | #1
         | BID=500
         | ExpVal=65.00
         | (selected strategy)
         \-------[C]
                  |
                  | #2
                  | COMPBID=400
                  | Prob=35.00
                  | ExpVal=0.00
                  | (selected strategy)
                  +-------[C]
                  |        |
                  |        | #3
                  |        | COST=200
                  |        | Prob=25.00
                  |        | PathProb=8.75
                  |        | (selected strategy)
                  |        +-------[T] PROFIT=0.00
                  |        |
                  |        | #4
                  |        | COST=400
                  |        | Prob=50.00
                  |        | PathProb=17.50
                  |        | (selected strategy)
                  |        +-------[T] PROFIT=0.00
                  |        |
                  |        | #5
                  |        | COST=600
                  |        | Prob=25.00
                  |        | PathProb=8.75
                  |        | (selected strategy)
                  |        \-------[T] PROFIT=0.00
                  |
                  | #6
                  | COMPBID=600
                  | Prob=50.00
                  | ExpVal=100.00
                  | (selected strategy)
                  +-------[C]
                  |        |
                  |        | #7
                  |        | COST=200
                  |        | Prob=25.00
                  |        | PathProb=12.50
                  |        | (selected strategy)
                  |        +-------[T] PROFIT=300.00
                  |        |
                  |        | #8
                  |        | COST=400
                  |        | Prob=50.00
                  |        | PathProb=25.00
                  |        | (selected strategy)
                  |        +-------[T] PROFIT=100.00
                  |        |
                  |        | #9
                  |        | COST=600
                  |        | Prob=25.00
                  |        | PathProb=12.50
                  |        | (selected strategy)
                  |        \-------[T] PROFIT=-100.00
                  |
                  | #10
                  | COMPBID=800
                  | Prob=15.00
                  | ExpVal=100.00
                  | (selected strategy)
                  \-------[C]
                           |
                           | #11
                           | COST=200
                           | Prob=25.00
                           | PathProb=3.75
                           | (selected strategy)
                           +-------[T] PROFIT=300.00
                           |
                           | #12
                           | COST=400
                           | Prob=50.00
                           | PathProb=7.50
                           | (selected strategy)
                           +-------[T] PROFIT=100.00
                           |
                           | #13
                           | COST=600
                           | Prob=25.00
                           | PathProb=3.75
                           | (selected strategy)
                           \-------[T] PROFIT=-100.00








>>> print(tree.export_text(risk_profile=True))
|
| #0
| ExpVal=65.00
| Risk Profile:
|         Value  Prob
|       -100.00 16.25
|          0.00 35.00
|        100.00 32.50
|        300.00 16.25
| (selected strategy)
\-------[D]
         |
         | #1
         | BID=500
         | ExpVal=65.00
         | Risk Profile:
         |         Value  Prob
         |       -100.00 16.25
         |          0.00 35.00
         |        100.00 32.50
         |        300.00 16.25
         | (selected strategy)
         +-------[C]
         |        |
         |        | #2
         |        | COMPBID=400
         |        | Prob=35.00
         |        | ExpVal=0.00
         |        | Risk Profile:
         |        |         Value  Prob
         |        |          0.00 35.00
         |        | (selected strategy)
         |        +-------[C]
         |        |        |
         |        |        | #3
         |        |        | COST=200
         |        |        | Prob=25.00
         |        |        | PathProb=8.75
         |        |        | (selected strategy)
         |        |        +-------[T] PROFIT=0.00
         |        |        |
         |        |        | #4
         |        |        | COST=400
         |        |        | Prob=50.00
         |        |        | PathProb=17.50
         |        |        | (selected strategy)
         |        |        +-------[T] PROFIT=0.00
         |        |        |
         |        |        | #5
         |        |        | COST=600
         |        |        | Prob=25.00
         |        |        | PathProb=8.75
         |        |        | (selected strategy)
         |        |        \-------[T] PROFIT=0.00
         |        |
         |        | #6
         |        | COMPBID=600
         |        | Prob=50.00
         |        | ExpVal=100.00
         |        | Risk Profile:
         |        |         Value  Prob
         |        |       -100.00 12.50
         |        |        100.00 25.00
         |        |        300.00 12.50
         |        | (selected strategy)
         |        +-------[C]
         |        |        |
         |        |        | #7
         |        |        | COST=200
         |        |        | Prob=25.00
         |        |        | PathProb=12.50
         |        |        | (selected strategy)
         |        |        +-------[T] PROFIT=300.00
         |        |        |
         |        |        | #8
         |        |        | COST=400
         |        |        | Prob=50.00
         |        |        | PathProb=25.00
         |        |        | (selected strategy)
         |        |        +-------[T] PROFIT=100.00
         |        |        |
         |        |        | #9
         |        |        | COST=600
         |        |        | Prob=25.00
         |        |        | PathProb=12.50
         |        |        | (selected strategy)
         |        |        \-------[T] PROFIT=-100.00
         |        |
         |        | #10
         |        | COMPBID=800
         |        | Prob=15.00
         |        | ExpVal=100.00
         |        | Risk Profile:
         |        |         Value  Prob
         |        |       -100.00  3.75
         |        |        100.00  7.50
         |        |        300.00  3.75
         |        | (selected strategy)
         |        \-------[C]
         |                 |
         |                 | #11
         |                 | COST=200
         |                 | Prob=25.00
         |                 | PathProb=3.75
         |                 | (selected strategy)
         |                 +-------[T] PROFIT=300.00
         |                 |
         |                 | #12
         |                 | COST=400
         |                 | Prob=50.00
         |                 | PathProb=7.50
         |                 | (selected strategy)
         |                 +-------[T] PROFIT=100.00
         |                 |
         |                 | #13
         |                 | COST=600
         |                 | Prob=25.00
         |                 | PathProb=3.75
         |                 | (selected strategy)
         |                 \-------[T] PROFIT=-100.00
         |
         | #14
         | BID=700
         | ExpVal=45.00
         \-------[C]
                  |
                  | #15
                  | COMPBID=400
                  | Prob=35.00
                  | ExpVal=0.00
                  +-------[C]
                  |        |
                  |        | #16
                  |        | COST=200
                  |        | Prob=25.00
                  |        | PathProb=0.00
                  |        +-------[T] PROFIT=0.00
                  |        |
                  |        | #17
                  |        | COST=400
                  |        | Prob=50.00
                  |        | PathProb=0.00
                  |        +-------[T] PROFIT=0.00
                  |        |
                  |        | #18
                  |        | COST=600
                  |        | Prob=25.00
                  |        | PathProb=0.00
                  |        \-------[T] PROFIT=0.00
                  |
                  | #19
                  | COMPBID=600
                  | Prob=50.00
                  | ExpVal=0.00
                  +-------[C]
                  |        |
                  |        | #20
                  |        | COST=200
                  |        | Prob=25.00
                  |        | PathProb=0.00
                  |        +-------[T] PROFIT=0.00
                  |        |
                  |        | #21
                  |        | COST=400
                  |        | Prob=50.00
                  |        | PathProb=0.00
                  |        +-------[T] PROFIT=0.00
                  |        |
                  |        | #22
                  |        | COST=600
                  |        | Prob=25.00
                  |        | PathProb=0.00
                  |        \-------[T] PROFIT=0.00
                  |
                  | #23
                  | COMPBID=800
                  | Prob=15.00
                  | ExpVal=300.00
                  \-------[C]
                           |
                           | #24
                           | COST=200
                           | Prob=25.00
                           | PathProb=0.00
                           +-------[T] PROFIT=500.00
                           |
                           | #25
                           | COST=400
                           | Prob=50.00
                           | PathProb=0.00
                           +-------[T] PROFIT=300.00
                           |
                           | #26
                           | COST=600
                           | Prob=25.00
                           | PathProb=0.00
                           \-------[T] PROFIT=100.00


**Probabilistic senstitivity**

>>> b500 = []
>>> b700 = []
>>> for p in range(0, 101, 10):
...     tree.variables['COST']['branches'] = [
...         (p, 200, "PROFIT"),
...         (0, 400, "PROFIT"),
...         (100 - p, 600, "PROFIT"),
...     ]
...     tree.build()
...     tree.evaluate()
...     b500.append(tree.nodes[1]["ExpVal"])
...     b700.append(tree.nodes[14]["ExpVal"])

>>> b500
[-65.0, -39.0, -13.0, 13.0, 39.0, 65.0, 91.0, 117.0, 143.0, 169.0, 195.0]

>>> b700
[15.0, 21.0, 27.0, 33.0, 39.0, 45.0, 51.0, 57.0, 63.0, 69.0, 75.0]



"""
