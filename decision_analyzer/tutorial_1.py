"""
Building a simple decision tree
===============================================================================



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


"""
