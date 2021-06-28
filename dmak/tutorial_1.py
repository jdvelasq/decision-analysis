r"""
Building a basic decision tree
===============================================================================

This is a classical bid example which was adapted example of the book "Decision 
Analisis for the Professional". 

A company has decided to submit a proposal in a tender. There are two possible 
bid values: $500 and $700. The costs are uncertain, and the expert has determined 
that they could be:

* $200 with a probability of 25%.

* $400 with a probability of 50%.

* $600 with a probability of 25%.

On the other hand, there is a competing company for which it has been estimated
that it could present the following possible proposals:

* $400 with a probability of 35%.

* $500 with a probability of 50%.

* $800 with a probability of 15%.

The profit of the company is calculated as a proposal minus costs if it wins
the bid, and zero if it loses it.


**Profit function.**

The profit of the company can be computed using the following equation:


    PROFIT = (BID-COST) * (1 if BID < COMPBID else 0)


which is written in code as:

>>> def profit(BID, COST, COMPBID):
...     return (BID - COST) * (1 if BID < COMPBID else 0)


**Creation of the nodes.**

The first step is to create the variables. The first variable is the value of
the proposal. The branches are composed of the the possible values of the
proposal, and the name of the following node. COMPBID is the node representing
the proposal of the competing company.


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

The second variable is the proposal of the competing company. The branches are
composed of the probability, the value of the branch, and the name of the 
following node.

>>> nodes.chance(
...     name='COMPBID',
...     branches=[
...         (35.0,  400,  "COST"),
...         (50.0,  600,  "COST"),
...         (15.0,  800,  "COST")
...     ]
... )

The third variable are the costs.

>>> nodes.chance(
...     name='COST',
...     branches=[
...         (25.0,  200,  "PROFIT"),
...         (50.0,  400,  "PROFIT"),
...         (25.0,  600,  "PROFIT"),
...     ]
... )

And the fourth variable is the profit. Note that this node uses a custom user
function (defined above) for computing the profit.

>>> nodes.terminal(
...     name="PROFIT",
...     user_fn=profit,
... )


The defined variables can be seen as follows.

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


**Decision tree creation.**

In the following code, the decision tree is specified by defining the variables
used and the name of the variable in the root of the tree.

>>> from decision_analyzer.decisiontree import DecisionTree
>>> tree = DecisionTree(
...     variables=nodes,
...     initial_variable="BID"
... )

Next, the internal structure of the decision tree is builded:

>>> tree.build()

The structure is conformed of the nodes of the tree; the first value is the id
number of the node; `successors` indicates the nodes in the branches. Note
that, in this point the tree has not been evaluated.

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


**Visualization.**


The tree can be viewed using the plot function. 

>>> tree.plot()

.. image:: ./images/tut-1-fig-1.png
    :width: 650px
    :align: center


The decision tree can be exported as text using the `export_text` function.

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



**Subtree visualization.**

>>> tree.plot(max_deep=2)

.. image:: ./images/tut-1-fig-2.png
    :width: 450px
    :align: center

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


.. image:: ./images/tut-1-fig-3.png
    :width: 700px
    :align: center

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








"""
