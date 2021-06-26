# r""" Super Tree

# >>> from hardDecisions.decisiontree import *
# >>> tree = DecisionTree()


# >>> tree.decision_node(name='BID',
# ...                    branches=[(500,  1),
# ...                            (700,  1)],
# ...                    max=True)


# >>> tree.chance_node(name='COMPBID',
# ...                  branches=[(35.0,  400,  2),
# ...                          (50.0,  600,  2),
# ...                          (15.0,  800,  2)])


# >>> tree.chance_node(name='COST',
# ...                  branches=[(25.0,  200,  3),
# ...                            (50.0,  400,  3),
# ...                            (25.0,  600,  3)])


# >>> tree.terminal_node(expr='(BID-COST) * (1 if BID < COMPBID else 0)')


# >>> tree.display_nodes() # doctest: +NORMALIZE_WHITESPACE
# Node 0
#     Type: DECISION - Maximum Payoff
#     Name: BID
#     Branches:
#                          Value  Next Node
#                        500.000  1
#                        700.000  1
# <BLANKLINE>
# Node 1
#     Type: CHANCE
#     Name: COMPBID
#     Branches:
#           Chance         Value  Next Node
#            35.00       400.000  2
#            50.00       600.000  2
#            15.00       800.000  2
# <BLANKLINE>
# Node 2
#     Type: CHANCE
#     Name: COST
#     Branches:
#           Chance         Value  Next Node
#            25.00       200.000  3
#            50.00       400.000  3
#            25.00       600.000  3
# <BLANKLINE>
# Node 3
#     Type: TERMINAL
#     Expr: (BID-COST) * (1 if BID < COMPBID else 0)
# <BLANKLINE>


# >>> tree.build_tree()


# >>> tree.display_tree() # doctest: +NORMALIZE_WHITESPACE
# |
# | #0
# \-------[D]
#         |
#         | #1
#         | BID=500
#         +-------[C]
#         |        |
#         |        | #2
#         |        | COMPBID=400
#         |        | Prob=35.00
#         |        +-------[C]
#         |        |        |
#         |        |        | #3
#         |        |        | COST=200
#         |        |        | Prob=25.00
#         |        |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#         |        |        |
#         |        |        | #4
#         |        |        | COST=400
#         |        |        | Prob=50.00
#         |        |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#         |        |        |
#         |        |        | #5
#         |        |        | COST=600
#         |        |        | Prob=25.00
#         |        |        \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#         |        |
#         |        | #6
#         |        | COMPBID=600
#         |        | Prob=50.00
#         |        +-------[C]
#         |        |        |
#         |        |        | #7
#         |        |        | COST=200
#         |        |        | Prob=25.00
#         |        |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#         |        |        |
#         |        |        | #8
#         |        |        | COST=400
#         |        |        | Prob=50.00
#         |        |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#         |        |        |
#         |        |        | #9
#         |        |        | COST=600
#         |        |        | Prob=25.00
#         |        |        \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#         |        |
#         |        | #10
#         |        | COMPBID=800
#         |        | Prob=15.00
#         |        \-------[C]
#         |                 |
#         |                 | #11
#         |                 | COST=200
#         |                 | Prob=25.00
#         |                 +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#         |                 |
#         |                 | #12
#         |                 | COST=400
#         |                 | Prob=50.00
#         |                 +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#         |                 |
#         |                 | #13
#         |                 | COST=600
#         |                 | Prob=25.00
#         |                 \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#         |
#         | #14
#         | BID=700
#         \-------[C]
#                  |
#                  | #15
#                  | COMPBID=400
#                  | Prob=35.00
#                  +-------[C]
#                  |        |
#                  |        | #16
#                  |        | COST=200
#                  |        | Prob=25.00
#                  |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                  |        |
#                  |        | #17
#                  |        | COST=400
#                  |        | Prob=50.00
#                  |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                  |        |
#                  |        | #18
#                  |        | COST=600
#                  |        | Prob=25.00
#                  |        \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                  |
#                  | #19
#                  | COMPBID=600
#                  | Prob=50.00
#                  +-------[C]
#                  |        |
#                  |        | #20
#                  |        | COST=200
#                  |        | Prob=25.00
#                  |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                  |        |
#                  |        | #21
#                  |        | COST=400
#                  |        | Prob=50.00
#                  |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                  |        |
#                  |        | #22
#                  |        | COST=600
#                  |        | Prob=25.00
#                  |        \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                  |
#                  | #23
#                  | COMPBID=800
#                  | Prob=15.00
#                  \-------[C]
#                           |
#                           | #24
#                           | COST=200
#                           | Prob=25.00
#                           +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                           |
#                           | #25
#                           | COST=400
#                           | Prob=50.00
#                           +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                           |
#                           | #26
#                           | COST=600
#                           | Prob=25.00
#                           \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)


# >>> tree.display_tree(maxdeep=0) # doctest: +NORMALIZE_WHITESPACE
# |
# | #0
# \-------[D]


# >>> tree.display_tree(maxdeep=1) # doctest: +NORMALIZE_WHITESPACE
# |
# | #0
# \-------[D]
#         |
#         | #1
#         | BID=500
#         +-------[C]
#         |
#         | #14
#         | BID=700
#         \-------[C]


# >>> tree.display_tree(maxdeep=2) # doctest: +NORMALIZE_WHITESPACE
# |
# | #0
# \-------[D]
#         |
#         | #1
#         | BID=500
#         +-------[C]
#         |        |
#         |        | #2
#         |        | COMPBID=400
#         |        | Prob=35.00
#         |        +-------[C]
#         |        |
#         |        | #6
#         |        | COMPBID=600
#         |        | Prob=50.00
#         |        +-------[C]
#         |        |
#         |        | #10
#         |        | COMPBID=800
#         |        | Prob=15.00
#         |        \-------[C]
#         |
#         | #14
#         | BID=700
#         \-------[C]
#                  |
#                  | #15
#                  | COMPBID=400
#                  | Prob=35.00
#                  +-------[C]
#                  |
#                  | #19
#                  | COMPBID=600
#                  | Prob=50.00
#                  +-------[C]
#                  |
#                  | #23
#                  | COMPBID=800
#                  | Prob=15.00
#                  \-------[C]


# >>> tree.display_tree(maxdeep=3) # doctest: +NORMALIZE_WHITESPACE
# |
# | #0
# \-------[D]
#         |
#         | #1
#         | BID=500
#         +-------[C]
#         |        |
#         |        | #2
#         |        | COMPBID=400
#         |        | Prob=35.00
#         |        +-------[C]
#         |        |        |
#         |        |        | #3
#         |        |        | COST=200
#         |        |        | Prob=25.00
#         |        |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#         |        |        |
#         |        |        | #4
#         |        |        | COST=400
#         |        |        | Prob=50.00
#         |        |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#         |        |        |
#         |        |        | #5
#         |        |        | COST=600
#         |        |        | Prob=25.00
#         |        |        \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#         |        |
#         |        | #6
#         |        | COMPBID=600
#         |        | Prob=50.00
#         |        +-------[C]
#         |        |        |
#         |        |        | #7
#         |        |        | COST=200
#         |        |        | Prob=25.00
#         |        |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#         |        |        |
#         |        |        | #8
#         |        |        | COST=400
#         |        |        | Prob=50.00
#         |        |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#         |        |        |
#         |        |        | #9
#         |        |        | COST=600
#         |        |        | Prob=25.00
#         |        |        \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#         |        |
#         |        | #10
#         |        | COMPBID=800
#         |        | Prob=15.00
#         |        \-------[C]
#         |                 |
#         |                 | #11
#         |                 | COST=200
#         |                 | Prob=25.00
#         |                 +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#         |                 |
#         |                 | #12
#         |                 | COST=400
#         |                 | Prob=50.00
#         |                 +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#         |                 |
#         |                 | #13
#         |                 | COST=600
#         |                 | Prob=25.00
#         |                 \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#         |
#         | #14
#         | BID=700
#         \-------[C]
#                  |
#                  | #15
#                  | COMPBID=400
#                  | Prob=35.00
#                  +-------[C]
#                  |        |
#                  |        | #16
#                  |        | COST=200
#                  |        | Prob=25.00
#                  |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                  |        |
#                  |        | #17
#                  |        | COST=400
#                  |        | Prob=50.00
#                  |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                  |        |
#                  |        | #18
#                  |        | COST=600
#                  |        | Prob=25.00
#                  |        \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                  |
#                  | #19
#                  | COMPBID=600
#                  | Prob=50.00
#                  +-------[C]
#                  |        |
#                  |        | #20
#                  |        | COST=200
#                  |        | Prob=25.00
#                  |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                  |        |
#                  |        | #21
#                  |        | COST=400
#                  |        | Prob=50.00
#                  |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                  |        |
#                  |        | #22
#                  |        | COST=600
#                  |        | Prob=25.00
#                  |        \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                  |
#                  | #23
#                  | COMPBID=800
#                  | Prob=15.00
#                  \-------[C]
#                           |
#                           | #24
#                           | COST=200
#                           | Prob=25.00
#                           +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                           |
#                           | #25
#                           | COST=400
#                           | Prob=50.00
#                           +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                           |
#                           | #26
#                           | COST=600
#                           | Prob=25.00
#                           \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)


# >>> tree.evaluate()
# >>> tree.display_tree() # doctest: +NORMALIZE_WHITESPACE
# |
# | #0
# | ExpVal=65.00
# | (selected strategy)
# \-------[D]
#          |
#          | #1
#          | BID=500
#          | ExpVal=65.00
#          | (selected strategy)
#          +-------[C]
#          |        |
#          |        | #2
#          |        | COMPBID=400
#          |        | Prob=35.00
#          |        | ExpVal=0.00
#          |        | (selected strategy)
#          |        +-------[C]
#          |        |        |
#          |        |        | #3
#          |        |        | COST=200
#          |        |        | Prob=25.00
#          |        |        | PathProb=8.75
#          |        |        | ExpVal=0.00
#          |        |        | (selected strategy)
#          |        |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#          |        |        |
#          |        |        | #4
#          |        |        | COST=400
#          |        |        | Prob=50.00
#          |        |        | PathProb=17.50
#          |        |        | ExpVal=0.00
#          |        |        | (selected strategy)
#          |        |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#          |        |        |
#          |        |        | #5
#          |        |        | COST=600
#          |        |        | Prob=25.00
#          |        |        | PathProb=8.75
#          |        |        | ExpVal=0.00
#          |        |        | (selected strategy)
#          |        |        \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#          |        |
#          |        | #6
#          |        | COMPBID=600
#          |        | Prob=50.00
#          |        | ExpVal=100.00
#          |        | (selected strategy)
#          |        +-------[C]
#          |        |        |
#          |        |        | #7
#          |        |        | COST=200
#          |        |        | Prob=25.00
#          |        |        | PathProb=12.50
#          |        |        | ExpVal=300.00
#          |        |        | (selected strategy)
#          |        |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#          |        |        |
#          |        |        | #8
#          |        |        | COST=400
#          |        |        | Prob=50.00
#          |        |        | PathProb=25.00
#          |        |        | ExpVal=100.00
#          |        |        | (selected strategy)
#          |        |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#          |        |        |
#          |        |        | #9
#          |        |        | COST=600
#          |        |        | Prob=25.00
#          |        |        | PathProb=12.50
#          |        |        | ExpVal=-100.00
#          |        |        | (selected strategy)
#          |        |        \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#          |        |
#          |        | #10
#          |        | COMPBID=800
#          |        | Prob=15.00
#          |        | ExpVal=100.00
#          |        | (selected strategy)
#          |        \-------[C]
#          |                 |
#          |                 | #11
#          |                 | COST=200
#          |                 | Prob=25.00
#          |                 | PathProb=3.75
#          |                 | ExpVal=300.00
#          |                 | (selected strategy)
#          |                 +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#          |                 |
#          |                 | #12
#          |                 | COST=400
#          |                 | Prob=50.00
#          |                 | PathProb=7.50
#          |                 | ExpVal=100.00
#          |                 | (selected strategy)
#          |                 +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#          |                 |
#          |                 | #13
#          |                 | COST=600
#          |                 | Prob=25.00
#          |                 | PathProb=3.75
#          |                 | ExpVal=-100.00
#          |                 | (selected strategy)
#          |                 \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#          |
#          | #14
#          | BID=700
#          | ExpVal=45.00
#          \-------[C]
#                   |
#                   | #15
#                   | COMPBID=400
#                   | Prob=35.00
#                   | ExpVal=0.00
#                   +-------[C]
#                   |        |
#                   |        | #16
#                   |        | COST=200
#                   |        | Prob=25.00
#                   |        | PathProb=0.00
#                   |        | ExpVal=0.00
#                   |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                   |        |
#                   |        | #17
#                   |        | COST=400
#                   |        | Prob=50.00
#                   |        | PathProb=0.00
#                   |        | ExpVal=0.00
#                   |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                   |        |
#                   |        | #18
#                   |        | COST=600
#                   |        | Prob=25.00
#                   |        | PathProb=0.00
#                   |        | ExpVal=0.00
#                   |        \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                   |
#                   | #19
#                   | COMPBID=600
#                   | Prob=50.00
#                   | ExpVal=0.00
#                   +-------[C]
#                   |        |
#                   |        | #20
#                   |        | COST=200
#                   |        | Prob=25.00
#                   |        | PathProb=0.00
#                   |        | ExpVal=0.00
#                   |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                   |        |
#                   |        | #21
#                   |        | COST=400
#                   |        | Prob=50.00
#                   |        | PathProb=0.00
#                   |        | ExpVal=0.00
#                   |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                   |        |
#                   |        | #22
#                   |        | COST=600
#                   |        | Prob=25.00
#                   |        | PathProb=0.00
#                   |        | ExpVal=0.00
#                   |        \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                   |
#                   | #23
#                   | COMPBID=800
#                   | Prob=15.00
#                   | ExpVal=300.00
#                   \-------[C]
#                            |
#                            | #24
#                            | COST=200
#                            | Prob=25.00
#                            | PathProb=0.00
#                            | ExpVal=500.00
#                            +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                            |
#                            | #25
#                            | COST=400
#                            | Prob=50.00
#                            | PathProb=0.00
#                            | ExpVal=300.00
#                            +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                            |
#                            | #26
#                            | COST=600
#                            | Prob=25.00
#                            | PathProb=0.00
#                            | ExpVal=100.00
#                            \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)


# >>> tree.display_tree(selected_strategy=True) # doctest: +NORMALIZE_WHITESPACE
# |
# | #0
# | ExpVal=65.00
# | (selected strategy)
# \-------[D]
#          |
#          | #1
#          | BID=500
#          | ExpVal=65.00
#          | (selected strategy)
#          \-------[C]
#                   |
#                   | #2
#                   | COMPBID=400
#                   | Prob=35.00
#                   | ExpVal=0.00
#                   | (selected strategy)
#                   +-------[C]
#                   |        |
#                   |        | #3
#                   |        | COST=200
#                   |        | Prob=25.00
#                   |        | PathProb=8.75
#                   |        | ExpVal=0.00
#                   |        | (selected strategy)
#                   |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                   |        |
#                   |        | #4
#                   |        | COST=400
#                   |        | Prob=50.00
#                   |        | PathProb=17.50
#                   |        | ExpVal=0.00
#                   |        | (selected strategy)
#                   |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                   |        |
#                   |        | #5
#                   |        | COST=600
#                   |        | Prob=25.00
#                   |        | PathProb=8.75
#                   |        | ExpVal=0.00
#                   |        | (selected strategy)
#                   |        \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                   |
#                   | #6
#                   | COMPBID=600
#                   | Prob=50.00
#                   | ExpVal=100.00
#                   | (selected strategy)
#                   +-------[C]
#                   |        |
#                   |        | #7
#                   |        | COST=200
#                   |        | Prob=25.00
#                   |        | PathProb=12.50
#                   |        | ExpVal=300.00
#                   |        | (selected strategy)
#                   |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                   |        |
#                   |        | #8
#                   |        | COST=400
#                   |        | Prob=50.00
#                   |        | PathProb=25.00
#                   |        | ExpVal=100.00
#                   |        | (selected strategy)
#                   |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                   |        |
#                   |        | #9
#                   |        | COST=600
#                   |        | Prob=25.00
#                   |        | PathProb=12.50
#                   |        | ExpVal=-100.00
#                   |        | (selected strategy)
#                   |        \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                   |
#                   | #10
#                   | COMPBID=800
#                   | Prob=15.00
#                   | ExpVal=100.00
#                   | (selected strategy)
#                   \-------[C]
#                            |
#                            | #11
#                            | COST=200
#                            | Prob=25.00
#                            | PathProb=3.75
#                            | ExpVal=300.00
#                            | (selected strategy)
#                            +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                            |
#                            | #12
#                            | COST=400
#                            | Prob=50.00
#                            | PathProb=7.50
#                            | ExpVal=100.00
#                            | (selected strategy)
#                            +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                            |
#                            | #13
#                            | COST=600
#                            | Prob=25.00
#                            | PathProb=3.75
#                            | ExpVal=-100.00
#                            | (selected strategy)
#                            \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)


# >>> tree.compute_risk_profile()

# >>> tree.display_tree() # doctest: +NORMALIZE_WHITESPACE
# |
# | #0
# | ExpVal=65.00
# | Risk Profile:
# |      Value  Prob
# |    -100.00 16.25
# |       0.00 35.00
# |     100.00 32.50
# |     300.00 16.25
# | (selected strategy)
# \-------[D]
#          |
#          | #1
#          | BID=500
#          | ExpVal=65.00
#          | Risk Profile:
#          |      Value  Prob
#          |    -100.00 16.25
#          |       0.00 35.00
#          |     100.00 32.50
#          |     300.00 16.25
#          | (selected strategy)
#          +-------[C]
#          |        |
#          |        | #2
#          |        | COMPBID=400
#          |        | Prob=35.00
#          |        | ExpVal=0.00
#          |        | Risk Profile:
#          |        |      Value  Prob
#          |        |       0.00 35.00
#          |        | (selected strategy)
#          |        +-------[C]
#          |        |        |
#          |        |        | #3
#          |        |        | COST=200
#          |        |        | Prob=25.00
#          |        |        | PathProb=8.75
#          |        |        | ExpVal=0.00
#          |        |        | (selected strategy)
#          |        |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#          |        |        |
#          |        |        | #4
#          |        |        | COST=400
#          |        |        | Prob=50.00
#          |        |        | PathProb=17.50
#          |        |        | ExpVal=0.00
#          |        |        | (selected strategy)
#          |        |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#          |        |        |
#          |        |        | #5
#          |        |        | COST=600
#          |        |        | Prob=25.00
#          |        |        | PathProb=8.75
#          |        |        | ExpVal=0.00
#          |        |        | (selected strategy)
#          |        |        \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#          |        |
#          |        | #6
#          |        | COMPBID=600
#          |        | Prob=50.00
#          |        | ExpVal=100.00
#          |        | Risk Profile:
#          |        |      Value  Prob
#          |        |    -100.00 12.50
#          |        |     100.00 25.00
#          |        |     300.00 12.50
#          |        | (selected strategy)
#          |        +-------[C]
#          |        |        |
#          |        |        | #7
#          |        |        | COST=200
#          |        |        | Prob=25.00
#          |        |        | PathProb=12.50
#          |        |        | ExpVal=300.00
#          |        |        | (selected strategy)
#          |        |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#          |        |        |
#          |        |        | #8
#          |        |        | COST=400
#          |        |        | Prob=50.00
#          |        |        | PathProb=25.00
#          |        |        | ExpVal=100.00
#          |        |        | (selected strategy)
#          |        |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#          |        |        |
#          |        |        | #9
#          |        |        | COST=600
#          |        |        | Prob=25.00
#          |        |        | PathProb=12.50
#          |        |        | ExpVal=-100.00
#          |        |        | (selected strategy)
#          |        |        \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#          |        |
#          |        | #10
#          |        | COMPBID=800
#          |        | Prob=15.00
#          |        | ExpVal=100.00
#          |        | Risk Profile:
#          |        |      Value  Prob
#          |        |    -100.00  3.75
#          |        |     100.00  7.50
#          |        |     300.00  3.75
#          |        | (selected strategy)
#          |        \-------[C]
#          |                 |
#          |                 | #11
#          |                 | COST=200
#          |                 | Prob=25.00
#          |                 | PathProb=3.75
#          |                 | ExpVal=300.00
#          |                 | (selected strategy)
#          |                 +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#          |                 |
#          |                 | #12
#          |                 | COST=400
#          |                 | Prob=50.00
#          |                 | PathProb=7.50
#          |                 | ExpVal=100.00
#          |                 | (selected strategy)
#          |                 +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#          |                 |
#          |                 | #13
#          |                 | COST=600
#          |                 | Prob=25.00
#          |                 | PathProb=3.75
#          |                 | ExpVal=-100.00
#          |                 | (selected strategy)
#          |                 \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#          |
#          | #14
#          | BID=700
#          | ExpVal=45.00
#          \-------[C]
#                   |
#                   | #15
#                   | COMPBID=400
#                   | Prob=35.00
#                   | ExpVal=0.00
#                   +-------[C]
#                   |        |
#                   |        | #16
#                   |        | COST=200
#                   |        | Prob=25.00
#                   |        | PathProb=0.00
#                   |        | ExpVal=0.00
#                   |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                   |        |
#                   |        | #17
#                   |        | COST=400
#                   |        | Prob=50.00
#                   |        | PathProb=0.00
#                   |        | ExpVal=0.00
#                   |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                   |        |
#                   |        | #18
#                   |        | COST=600
#                   |        | Prob=25.00
#                   |        | PathProb=0.00
#                   |        | ExpVal=0.00
#                   |        \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                   |
#                   | #19
#                   | COMPBID=600
#                   | Prob=50.00
#                   | ExpVal=0.00
#                   +-------[C]
#                   |        |
#                   |        | #20
#                   |        | COST=200
#                   |        | Prob=25.00
#                   |        | PathProb=0.00
#                   |        | ExpVal=0.00
#                   |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                   |        |
#                   |        | #21
#                   |        | COST=400
#                   |        | Prob=50.00
#                   |        | PathProb=0.00
#                   |        | ExpVal=0.00
#                   |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                   |        |
#                   |        | #22
#                   |        | COST=600
#                   |        | Prob=25.00
#                   |        | PathProb=0.00
#                   |        | ExpVal=0.00
#                   |        \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                   |
#                   | #23
#                   | COMPBID=800
#                   | Prob=15.00
#                   | ExpVal=300.00
#                   \-------[C]
#                            |
#                            | #24
#                            | COST=200
#                            | Prob=25.00
#                            | PathProb=0.00
#                            | ExpVal=500.00
#                            +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                            |
#                            | #25
#                            | COST=400
#                            | Prob=50.00
#                            | PathProb=0.00
#                            | ExpVal=300.00
#                            +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                            |
#                            | #26
#                            | COST=600
#                            | Prob=25.00
#                            | PathProb=0.00
#                            | ExpVal=100.00
#                            \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)


# Probabilistic senstitivity

# >>> b500 = []
# >>> b700 = []
# >>> for p in range(0, 101, 10):
# ...    tree.data[2]['branches'] = [(p,  200,  3), (0.0,  400,  3),  (100-p,  600,  3)]
# ...    tree.build_tree()
# ...    tree.evaluate()
# ...    b500.append(tree.tree[1]['ExpVal'])
# ...    b700.append(tree.tree[14]['ExpVal'])

# >>> tree.data[2]['branches'] = [(25,  200,  3), (50,  400,  3),  (25,  600,  3)]
# >>> tree.build_tree()
# >>> tree.evaluate()


# >>> b500
# [-65.0, -39.0, -13.0, 13.0, 39.0, 65.0, 91.0, 117.0, 143.0, 169.0, 195.0]

# >>> b700
# [15.0, 21.0, 27.0, 33.0, 39.0, 45.0, 51.0, 57.0, 63.0, 69.0, 75.0]

# >>> tree.use_utility_function(exponential=True, R=100)
# >>> tree.evaluate()
# >>> tree.display_tree() # doctest: +NORMALIZE_WHITESPACE
# |
# | #0
# | ExpVal=45.00
# | ExpUtl=0.13
# | CE=14.18
# | (selected strategy)
# \-------[D]
#          |
#          | #1
#          | BID=500
#          | ExpVal=65.00
#          | ExpUtl=0.08
#          | CE=8.41
#          +-------[C]
#          |        |
#          |        | #2
#          |        | COMPBID=400
#          |        | Prob=35.00
#          |        | ExpVal=0.00
#          |        | ExpUtl=0.00
#          |        | CE=-0.00
#          |        +-------[C]
#          |        |        |
#          |        |        | #3
#          |        |        | COST=200
#          |        |        | Prob=25.00
#          |        |        | PathProb=0.00
#          |        |        | ExpVal=0.00
#          |        |        | ExpUtl=0.00
#          |        |        | CE=0.00
#          |        |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#          |        |        |
#          |        |        | #4
#          |        |        | COST=400
#          |        |        | Prob=50.00
#          |        |        | PathProb=0.00
#          |        |        | ExpVal=0.00
#          |        |        | ExpUtl=0.00
#          |        |        | CE=0.00
#          |        |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#          |        |        |
#          |        |        | #5
#          |        |        | COST=600
#          |        |        | Prob=25.00
#          |        |        | PathProb=0.00
#          |        |        | ExpVal=0.00
#          |        |        | ExpUtl=0.00
#          |        |        | CE=0.00
#          |        |        \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#          |        |
#          |        | #6
#          |        | COMPBID=600
#          |        | Prob=50.00
#          |        | ExpVal=100.00
#          |        | ExpUtl=0.12
#          |        | CE=13.24
#          |        +-------[C]
#          |        |        |
#          |        |        | #7
#          |        |        | COST=200
#          |        |        | Prob=25.00
#          |        |        | PathProb=0.00
#          |        |        | ExpVal=300.00
#          |        |        | ExpUtl=0.95
#          |        |        | CE=300.00
#          |        |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#          |        |        |
#          |        |        | #8
#          |        |        | COST=400
#          |        |        | Prob=50.00
#          |        |        | PathProb=0.00
#          |        |        | ExpVal=100.00
#          |        |        | ExpUtl=0.63
#          |        |        | CE=100.00
#          |        |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#          |        |        |
#          |        |        | #9
#          |        |        | COST=600
#          |        |        | Prob=25.00
#          |        |        | PathProb=0.00
#          |        |        | ExpVal=-100.00
#          |        |        | ExpUtl=-1.72
#          |        |        | CE=-100.00
#          |        |        \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#          |        |
#          |        | #10
#          |        | COMPBID=800
#          |        | Prob=15.00
#          |        | ExpVal=100.00
#          |        | ExpUtl=0.12
#          |        | CE=13.24
#          |        \-------[C]
#          |                 |
#          |                 | #11
#          |                 | COST=200
#          |                 | Prob=25.00
#          |                 | PathProb=0.00
#          |                 | ExpVal=300.00
#          |                 | ExpUtl=0.95
#          |                 | CE=300.00
#          |                 +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#          |                 |
#          |                 | #12
#          |                 | COST=400
#          |                 | Prob=50.00
#          |                 | PathProb=0.00
#          |                 | ExpVal=100.00
#          |                 | ExpUtl=0.63
#          |                 | CE=100.00
#          |                 +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#          |                 |
#          |                 | #13
#          |                 | COST=600
#          |                 | Prob=25.00
#          |                 | PathProb=0.00
#          |                 | ExpVal=-100.00
#          |                 | ExpUtl=-1.72
#          |                 | CE=-100.00
#          |                 \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#          |
#          | #14
#          | BID=700
#          | ExpVal=45.00
#          | ExpUtl=0.13
#          | CE=14.18
#          | (selected strategy)
#          \-------[C]
#                   |
#                   | #15
#                   | COMPBID=400
#                   | Prob=35.00
#                   | ExpVal=0.00
#                   | ExpUtl=0.00
#                   | CE=-0.00
#                   | (selected strategy)
#                   +-------[C]
#                   |        |
#                   |        | #16
#                   |        | COST=200
#                   |        | Prob=25.00
#                   |        | PathProb=8.75
#                   |        | ExpVal=0.00
#                   |        | ExpUtl=0.00
#                   |        | CE=0.00
#                   |        | (selected strategy)
#                   |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                   |        |
#                   |        | #17
#                   |        | COST=400
#                   |        | Prob=50.00
#                   |        | PathProb=17.50
#                   |        | ExpVal=0.00
#                   |        | ExpUtl=0.00
#                   |        | CE=0.00
#                   |        | (selected strategy)
#                   |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                   |        |
#                   |        | #18
#                   |        | COST=600
#                   |        | Prob=25.00
#                   |        | PathProb=8.75
#                   |        | ExpVal=0.00
#                   |        | ExpUtl=0.00
#                   |        | CE=0.00
#                   |        | (selected strategy)
#                   |        \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                   |
#                   | #19
#                   | COMPBID=600
#                   | Prob=50.00
#                   | ExpVal=0.00
#                   | ExpUtl=0.00
#                   | CE=-0.00
#                   | (selected strategy)
#                   +-------[C]
#                   |        |
#                   |        | #20
#                   |        | COST=200
#                   |        | Prob=25.00
#                   |        | PathProb=12.50
#                   |        | ExpVal=0.00
#                   |        | ExpUtl=0.00
#                   |        | CE=0.00
#                   |        | (selected strategy)
#                   |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                   |        |
#                   |        | #21
#                   |        | COST=400
#                   |        | Prob=50.00
#                   |        | PathProb=25.00
#                   |        | ExpVal=0.00
#                   |        | ExpUtl=0.00
#                   |        | CE=0.00
#                   |        | (selected strategy)
#                   |        +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                   |        |
#                   |        | #22
#                   |        | COST=600
#                   |        | Prob=25.00
#                   |        | PathProb=12.50
#                   |        | ExpVal=0.00
#                   |        | ExpUtl=0.00
#                   |        | CE=0.00
#                   |        | (selected strategy)
#                   |        \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                   |
#                   | #23
#                   | COMPBID=800
#                   | Prob=15.00
#                   | ExpVal=300.00
#                   | ExpUtl=0.88
#                   | CE=213.24
#                   | (selected strategy)
#                   \-------[C]
#                            |
#                            | #24
#                            | COST=200
#                            | Prob=25.00
#                            | PathProb=3.75
#                            | ExpVal=500.00
#                            | ExpUtl=0.99
#                            | CE=500.00
#                            | (selected strategy)
#                            +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                            |
#                            | #25
#                            | COST=400
#                            | Prob=50.00
#                            | PathProb=7.50
#                            | ExpVal=300.00
#                            | ExpUtl=0.95
#                            | CE=300.00
#                            | (selected strategy)
#                            +-------[T] (BID-COST) * (1 if BID < COMPBID else 0)
#                            |
#                            | #26
#                            | COST=600
#                            | Prob=25.00
#                            | PathProb=3.75
#                            | ExpVal=100.00
#                            | ExpUtl=0.63
#                            | CE=100.00
#                            | (selected strategy)
#                            \-------[T] (BID-COST) * (1 if BID < COMPBID else 0)


# """


# if __name__ == "__main__":
#     import doctest

#     doctest.testmod()
