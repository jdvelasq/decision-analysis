# precision-tree

# r"""
# >>> from hardDecisions.decisiontree import *

# >>> tree = DecisionTree()

# #0
# >>> tree.decision_node(name='TEST',
# ...                    branches=[(-55,  1),
# ...                              (  0, 14)],
# ...                    max=True)

# #1
# >>> tree.chance_node(name='STRUCT',
# ...                  branches=[(38.0,  0,  2),
# ...                            (39.0,  0,  6),
# ...                            (23.0,  0, 10)])

# #2
# >>> tree.decision_node(name='DRILL1',
# ...                    branches=[(-600,  3),
# ...                              (   0,  5)],
# ...                    max=True)

# #3
# >>> tree.chance_node(name='OILFOUND1',
# ...                  branches=[(78.95,    0,  4),
# ...                            (15.79, 1500,  4),
# ...                            ( 5.26, 3400,  4)])

# #4
# >>> tree.terminal_node(expr='TEST+DRILL1+OILFOUND1')

# #5
# >>> tree.terminal_node(expr='TEST+DRILL1')


# #6
# >>> tree.decision_node(name='DRILL2',
# ...                    branches=[(-600,   7),
# ...                              (   0,   9)],
# ...                    max=True)

# #7
# >>> tree.chance_node(name='OILFOUND2',
# ...                  branches=[(38.46,    0,  8),
# ...                            (46.15, 1500,  8),
# ...                            (15.38, 3400,  8)])

# #8
# >>> tree.terminal_node(expr='TEST+DRILL2+OILFOUND2')

# #9
# >>> tree.terminal_node(expr='TEST+DRILL2')


# #10
# >>> tree.decision_node(name='DRILL3',
# ...                    branches=[(-600,   11),
# ...                              (   0,   13)],
# ...                    max=True)

# #11
# >>> tree.chance_node(name='OILFOUND3',
# ...                  branches=[(21.74,    0,  12),
# ...                            (26.09, 1500,  12),
# ...                            (52.17, 3400,  12)])

# #12
# >>> tree.terminal_node(expr='TEST+DRILL3+OILFOUND3')

# #13
# >>> tree.terminal_node(expr='TEST+DRILL3')


# #14
# >>> tree.decision_node(name='DRILL4',
# ...                    branches=[(-600,   15),
# ...                              (   0,   17)],
# ...                    max=True)

# #15
# >>> tree.chance_node(name='OILFOUND4',
# ...                  branches=[(50.0,    0,  16),
# ...                            (30.0, 1500,  16),
# ...                            (20.0, 3400,  16)])

# #16
# >>> tree.terminal_node(expr='TEST+DRILL4+OILFOUND4')

# #17
# >>> tree.terminal_node(expr='TEST+DRILL4')


# >>> tree.display_nodes() # doctest: +NORMALIZE_WHITESPACE
# Node 0
#    Type: DECISION - Maximum Payoff
#    Name: TEST
#    Branches:
#                         Value  Next Node
#                       -55.000  1
#                         0.000  14
# <BLANKLINE>
# Node 1
#    Type: CHANCE
#    Name: STRUCT
#    Branches:
#          Chance          Value Next Node
#           38.00         0.000  2
#           39.00         0.000  6
#           23.00         0.000  10
# <BLANKLINE>
# Node 2
#    Type: DECISION - Maximum Payoff
#    Name: DRILL1
#    Branches:
#                         Value  Next Node
#                      -600.000  3
#                         0.000  5
# <BLANKLINE>
# Node 3
#    Type: CHANCE
#    Name: OILFOUND1
#    Branches:
#          Chance         Value  Next Node
#           78.95         0.000  4
#           15.79      1500.000  4
#            5.26      3400.000  4
# <BLANKLINE>
# Node 4
#    Type: TERMINAL
#    Expr: TEST+DRILL1+OILFOUND1
# <BLANKLINE>
# Node 5
#    Type: TERMINAL
#    Expr: TEST+DRILL1
# <BLANKLINE>
# Node 6
#    Type: DECISION - Maximum Payoff
#    Name: DRILL2
#    Branches:
#                         Value  Next Node
#                      -600.000  7
#                         0.000  9
# <BLANKLINE>
# Node 7
#    Type: CHANCE
#    Name: OILFOUND2
#    Branches:
#          Chance          Value Next Node
#           38.46         0.000  8
#           46.15      1500.000  8
#           15.38      3400.000  8
# <BLANKLINE>
# Node 8
#    Type: TERMINAL
#    Expr: TEST+DRILL2+OILFOUND2
# <BLANKLINE>
# Node 9
#    Type: TERMINAL
#    Expr: TEST+DRILL2
# <BLANKLINE>
# Node 10
#    Type: DECISION - Maximum Payoff
#    Name: DRILL3
#    Branches:
#                         Value  Next Node
#                      -600.000  11
#                         0.000  13
# <BLANKLINE>
# Node 11
#    Type: CHANCE
#    Name: OILFOUND3
#    Branches:
#          Chance         Value  Next Node
#           21.74         0.000  12
#           26.09      1500.000  12
#           52.17      3400.000  12
# <BLANKLINE>
# Node 12
#    Type: TERMINAL
#    Expr: TEST+DRILL3+OILFOUND3
# <BLANKLINE>
# Node 13
#    Type: TERMINAL
#    Expr: TEST+DRILL3
# <BLANKLINE>
# Node 14
#    Type: DECISION - Maximum Payoff
#    Name: DRILL4
#    Branches:
#                         Value  Next Node
#                      -600.000  15
#                         0.000  17
# <BLANKLINE>
# Node 15
#    Type: CHANCE
#    Name: OILFOUND4
#    Branches:
#          Chance         Value  Next Node
#           50.00         0.000  16
#           30.00      1500.000  16
#           20.00      3400.000  16
# <BLANKLINE>
# Node 16
#    Type: TERMINAL
#    Expr: TEST+DRILL4+OILFOUND4
# <BLANKLINE>
# Node 17
#    Type: TERMINAL
#    Expr: TEST+DRILL4
# <BLANKLINE>


# >>> tree.build_tree()


# >>> tree.display_tree() # doctest: +NORMALIZE_WHITESPACE
# |
# | #0
# \-------[D]
#         |
#         | #1
#         | TEST=-55
#         +-------[C]
#         |        |
#         |        | #2
#         |        | STRUCT=0
#         |        | Prob=38.00
#         |        +-------[D]
#         |        |        |
#         |        |        | #3
#         |        |        | DRILL1=-600
#         |        |        +-------[C]
#         |        |        |        |
#         |        |        |        | #4
#         |        |        |        | OILFOUND1=0
#         |        |        |        | Prob=78.95
#         |        |        |        +-------[T] TEST+DRILL1+OILFOUND1
#         |        |        |        |
#         |        |        |        | #5
#         |        |        |        | OILFOUND1=1500
#         |        |        |        | Prob=15.79
#         |        |        |        +-------[T] TEST+DRILL1+OILFOUND1
#         |        |        |        |
#         |        |        |        | #6
#         |        |        |        | OILFOUND1=3400
#         |        |        |        | Prob=5.26
#         |        |        |        \-------[T] TEST+DRILL1+OILFOUND1
#         |        |        |
#         |        |        | #7
#         |        |        | DRILL1=0
#         |        |        \-------[T] TEST+DRILL1
#         |        |
#         |        | #8
#         |        | STRUCT=0
#         |        | Prob=39.00
#         |        +-------[D]
#         |        |        |
#         |        |        | #9
#         |        |        | DRILL2=-600
#         |        |        +-------[C]
#         |        |        |        |
#         |        |        |        | #10
#         |        |        |        | OILFOUND2=0
#         |        |        |        | Prob=38.46
#         |        |        |        +-------[T] TEST+DRILL2+OILFOUND2
#         |        |        |        |
#         |        |        |        | #11
#         |        |        |        | OILFOUND2=1500
#         |        |        |        | Prob=46.15
#         |        |        |        +-------[T] TEST+DRILL2+OILFOUND2
#         |        |        |        |
#         |        |        |        | #12
#         |        |        |        | OILFOUND2=3400
#         |        |        |        | Prob=15.38
#         |        |        |        \-------[T] TEST+DRILL2+OILFOUND2
#         |        |        |
#         |        |        | #13
#         |        |        | DRILL2=0
#         |        |        \-------[T] TEST+DRILL2
#         |        |
#         |        | #14
#         |        | STRUCT=0
#         |        | Prob=23.00
#         |        \-------[D]
#         |                 |
#         |                 | #15
#         |                 | DRILL3=-600
#         |                 +-------[C]
#         |                 |        |
#         |                 |        | #16
#         |                 |        | OILFOUND3=0
#         |                 |        | Prob=21.74
#         |                 |        +-------[T] TEST+DRILL3+OILFOUND3
#         |                 |        |
#         |                 |        | #17
#         |                 |        | OILFOUND3=1500
#         |                 |        | Prob=26.09
#         |                 |        +-------[T] TEST+DRILL3+OILFOUND3
#         |                 |        |
#         |                 |        | #18
#         |                 |        | OILFOUND3=3400
#         |                 |        | Prob=52.17
#         |                 |        \-------[T] TEST+DRILL3+OILFOUND3
#         |                 |
#         |                 | #19
#         |                 | DRILL3=0
#         |                 \-------[T] TEST+DRILL3
#         |
#         | #20
#         | TEST=0
#         \-------[D]
#                  |
#                  | #21
#                  | DRILL4=-600
#                  +-------[C]
#                  |        |
#                  |        | #22
#                  |        | OILFOUND4=0
#                  |        | Prob=50.00
#                  |        +-------[T] TEST+DRILL4+OILFOUND4
#                  |        |
#                  |        | #23
#                  |        | OILFOUND4=1500
#                  |        | Prob=30.00
#                  |        +-------[T] TEST+DRILL4+OILFOUND4
#                  |        |
#                  |        | #24
#                  |        | OILFOUND4=3400
#                  |        | Prob=20.00
#                  |        \-------[T] TEST+DRILL4+OILFOUND4
#                  |
#                  | #25
#                  | DRILL4=0
#                  \-------[T] TEST+DRILL4


# >>> tree.evaluate()
# >>> tree.display_tree() # doctest: +NORMALIZE_WHITESPACE
# |
# | #0
# | ExpVal=544.92
# | (selected strategy)
# \-------[D]
#          |
#          | #1
#          | TEST=-55
#          | ExpVal=544.92
#          | (selected strategy)
#          +-------[C]
#          |        |
#          |        | #2
#          |        | STRUCT=0
#          |        | Prob=38.00
#          |        | ExpVal=-55.00
#          |        | (selected strategy)
#          |        +-------[D]
#          |        |        |
#          |        |        | #3
#          |        |        | DRILL1=-600
#          |        |        | ExpVal=-239.31
#          |        |        +-------[C]
#          |        |        |        |
#          |        |        |        | #4
#          |        |        |        | OILFOUND1=0
#          |        |        |        | Prob=78.95
#          |        |        |        | PathProb=0.00
#          |        |        |        | ExpVal=-655.00
#          |        |        |        +-------[T] TEST+DRILL1+OILFOUND1
#          |        |        |        |
#          |        |        |        | #5
#          |        |        |        | OILFOUND1=1500
#          |        |        |        | Prob=15.79
#          |        |        |        | PathProb=0.00
#          |        |        |        | ExpVal=845.00
#          |        |        |        +-------[T] TEST+DRILL1+OILFOUND1
#          |        |        |        |
#          |        |        |        | #6
#          |        |        |        | OILFOUND1=3400
#          |        |        |        | Prob=5.26
#          |        |        |        | PathProb=0.00
#          |        |        |        | ExpVal=2745.00
#          |        |        |        \-------[T] TEST+DRILL1+OILFOUND1
#          |        |        |
#          |        |        | #7
#          |        |        | DRILL1=0
#          |        |        | PathProb=38.00
#          |        |        | ExpVal=-55.00
#          |        |        | (selected strategy)
#          |        |        \-------[T] TEST+DRILL1
#          |        |
#          |        | #8
#          |        | STRUCT=0
#          |        | Prob=39.00
#          |        | ExpVal=560.24
#          |        | (selected strategy)
#          |        +-------[D]
#          |        |        |
#          |        |        | #9
#          |        |        | DRILL2=-600
#          |        |        | ExpVal=560.24
#          |        |        | (selected strategy)
#          |        |        +-------[C]
#          |        |        |        |
#          |        |        |        | #10
#          |        |        |        | OILFOUND2=0
#          |        |        |        | Prob=38.46
#          |        |        |        | PathProb=15.00
#          |        |        |        | ExpVal=-655.00
#          |        |        |        | (selected strategy)
#          |        |        |        +-------[T] TEST+DRILL2+OILFOUND2
#          |        |        |        |
#          |        |        |        | #11
#          |        |        |        | OILFOUND2=1500
#          |        |        |        | Prob=46.15
#          |        |        |        | PathProb=18.00
#          |        |        |        | ExpVal=845.00
#          |        |        |        | (selected strategy)
#          |        |        |        +-------[T] TEST+DRILL2+OILFOUND2
#          |        |        |        |
#          |        |        |        | #12
#          |        |        |        | OILFOUND2=3400
#          |        |        |        | Prob=15.38
#          |        |        |        | PathProb=6.00
#          |        |        |        | ExpVal=2745.00
#          |        |        |        | (selected strategy)
#          |        |        |        \-------[T] TEST+DRILL2+OILFOUND2
#          |        |        |
#          |        |        | #13
#          |        |        | DRILL2=0
#          |        |        | PathProb=0.00
#          |        |        | ExpVal=-55.00
#          |        |        \-------[T] TEST+DRILL2
#          |        |
#          |        | #14
#          |        | STRUCT=0
#          |        | Prob=23.00
#          |        | ExpVal=1510.13
#          |        | (selected strategy)
#          |        \-------[D]
#          |                 |
#          |                 | #15
#          |                 | DRILL3=-600
#          |                 | ExpVal=1510.13
#          |                 | (selected strategy)
#          |                 +-------[C]
#          |                 |        |
#          |                 |        | #16
#          |                 |        | OILFOUND3=0
#          |                 |        | Prob=21.74
#          |                 |        | PathProb=5.00
#          |                 |        | ExpVal=-655.00
#          |                 |        | (selected strategy)
#          |                 |        +-------[T] TEST+DRILL3+OILFOUND3
#          |                 |        |
#          |                 |        | #17
#          |                 |        | OILFOUND3=1500
#          |                 |        | Prob=26.09
#          |                 |        | PathProb=6.00
#          |                 |        | ExpVal=845.00
#          |                 |        | (selected strategy)
#          |                 |        +-------[T] TEST+DRILL3+OILFOUND3
#          |                 |        |
#          |                 |        | #18
#          |                 |        | OILFOUND3=3400
#          |                 |        | Prob=52.17
#          |                 |        | PathProb=12.00
#          |                 |        | ExpVal=2745.00
#          |                 |        | (selected strategy)
#          |                 |        \-------[T] TEST+DRILL3+OILFOUND3
#          |                 |
#          |                 | #19
#          |                 | DRILL3=0
#          |                 | PathProb=0.00
#          |                 | ExpVal=-55.00
#          |                 \-------[T] TEST+DRILL3
#          |
#          | #20
#          | TEST=0
#          | ExpVal=530.00
#          \-------[D]
#                   |
#                   | #21
#                   | DRILL4=-600
#                   | ExpVal=530.00
#                   +-------[C]
#                   |        |
#                   |        | #22
#                   |        | OILFOUND4=0
#                   |        | Prob=50.00
#                   |        | PathProb=0.00
#                   |        | ExpVal=-600.00
#                   |        +-------[T] TEST+DRILL4+OILFOUND4
#                   |        |
#                   |        | #23
#                   |        | OILFOUND4=1500
#                   |        | Prob=30.00
#                   |        | PathProb=0.00
#                   |        | ExpVal=900.00
#                   |        +-------[T] TEST+DRILL4+OILFOUND4
#                   |        |
#                   |        | #24
#                   |        | OILFOUND4=3400
#                   |        | Prob=20.00
#                   |        | PathProb=0.00
#                   |        | ExpVal=2800.00
#                   |        \-------[T] TEST+DRILL4+OILFOUND4
#                   |
#                   | #25
#                   | DRILL4=0
#                   | PathProb=0.00
#                   | ExpVal=0.00
#                   \-------[T] TEST+DRILL4

# >>> tree.compute_risk_profile()
# >>> tree.display_tree(selected_strategy=True) # doctest: +NORMALIZE_WHITESPACE
# |
# | #0
# | ExpVal=544.92
# | Risk Profile:
# |      Value  Prob
# |    -655.00 20.00
# |     -55.00 38.00
# |     845.00 24.00
# |    2745.00 18.00
# | (selected strategy)
# \-------[D]
#          |
#          | #1
#          | TEST=-55
#          | ExpVal=544.92
#          | Risk Profile:
#          |      Value  Prob
#          |    -655.00 20.00
#          |     -55.00 38.00
#          |     845.00 24.00
#          |    2745.00 18.00
#          | (selected strategy)
#          \-------[C]
#                   |
#                   | #2
#                   | STRUCT=0
#                   | Prob=38.00
#                   | ExpVal=-55.00
#                   | Risk Profile:
#                   |      Value  Prob
#                   |     -55.00 38.00
#                   | (selected strategy)
#                   +-------[D]
#                   |        |
#                   |        | #7
#                   |        | DRILL1=0
#                   |        | PathProb=38.00
#                   |        | ExpVal=-55.00
#                   |        | (selected strategy)
#                   |        \-------[T] TEST+DRILL1
#                   |
#                   | #8
#                   | STRUCT=0
#                   | Prob=39.00
#                   | ExpVal=560.24
#                   | Risk Profile:
#                   |      Value  Prob
#                   |    -655.00 15.00
#                   |     845.00 18.00
#                   |    2745.00  6.00
#                   | (selected strategy)
#                   +-------[D]
#                   |        |
#                   |        | #9
#                   |        | DRILL2=-600
#                   |        | ExpVal=560.24
#                   |        | Risk Profile:
#                   |        |      Value  Prob
#                   |        |    -655.00 15.00
#                   |        |     845.00 18.00
#                   |        |    2745.00  6.00
#                   |        | (selected strategy)
#                   |        \-------[C]
#                   |                 |
#                   |                 | #10
#                   |                 | OILFOUND2=0
#                   |                 | Prob=38.46
#                   |                 | PathProb=15.00
#                   |                 | ExpVal=-655.00
#                   |                 | (selected strategy)
#                   |                 +-------[T] TEST+DRILL2+OILFOUND2
#                   |                 |
#                   |                 | #11
#                   |                 | OILFOUND2=1500
#                   |                 | Prob=46.15
#                   |                 | PathProb=18.00
#                   |                 | ExpVal=845.00
#                   |                 | (selected strategy)
#                   |                 +-------[T] TEST+DRILL2+OILFOUND2
#                   |                 |
#                   |                 | #12
#                   |                 | OILFOUND2=3400
#                   |                 | Prob=15.38
#                   |                 | PathProb=6.00
#                   |                 | ExpVal=2745.00
#                   |                 | (selected strategy)
#                   |                 \-------[T] TEST+DRILL2+OILFOUND2
#                   |
#                   | #14
#                   | STRUCT=0
#                   | Prob=23.00
#                   | ExpVal=1510.13
#                   | Risk Profile:
#                   |      Value  Prob
#                   |    -655.00  5.00
#                   |     845.00  6.00
#                   |    2745.00 12.00
#                   | (selected strategy)
#                   \-------[D]
#                            |
#                            | #15
#                            | DRILL3=-600
#                            | ExpVal=1510.13
#                            | Risk Profile:
#                            |      Value  Prob
#                            |    -655.00  5.00
#                            |     845.00  6.00
#                            |    2745.00 12.00
#                            | (selected strategy)
#                            \-------[C]
#                                     |
#                                     | #16
#                                     | OILFOUND3=0
#                                     | Prob=21.74
#                                     | PathProb=5.00
#                                     | ExpVal=-655.00
#                                     | (selected strategy)
#                                     +-------[T] TEST+DRILL3+OILFOUND3
#                                     |
#                                     | #17
#                                     | OILFOUND3=1500
#                                     | Prob=26.09
#                                     | PathProb=6.00
#                                     | ExpVal=845.00
#                                     | (selected strategy)
#                                     +-------[T] TEST+DRILL3+OILFOUND3
#                                     |
#                                     | #18
#                                     | OILFOUND3=3400
#                                     | Prob=52.17
#                                     | PathProb=12.00
#                                     | ExpVal=2745.00
#                                     | (selected strategy)
#                                     \-------[T] TEST+DRILL3+OILFOUND3


# >>> tree = DecisionTree()

# #0
# >>> tree.decision_node(name='TEST',
# ...                    branches=[(-55, 1),
# ...                              (  0, 9)],
# ...                    max=True)

# #1
# >>> tree.chance_node(name='STRUCT',
# ...                  branches=[(38.0,  0, 2),
# ...                            (39.0,  0, 5),
# ...                            (23.0,  0, 7)])

# #2
# >>> tree.decision_node(name='DRILL',
# ...                    branches=[(-600,  3),
# ...                              (   0,  4)],
# ...                    max=True)

# #3
# >>> tree.chance_node(name='OILFOUND',
# ...                  branches=[(78.95,    0,  4),
# ...                            (15.79, 1500,  4),
# ...                            (05.26, 3400,  4)])

# #4
# >>> tree.terminal_node()

# #5
# >>> tree.decision_node(name='DRILL',
# ...                    branches=[(-600,   6),
# ...                              (   0,   4)],
# ...                    max=True)

# #6
# >>> tree.chance_node(name='OILFOUND',
# ...                  branches=[(38.46,    0,  4),
# ...                            (46.15, 1500,  4),
# ...                            (15.38, 3400,  4)])

# #7
# >>> tree.decision_node(name='DRILL',
# ...                    branches=[(-600,  8),
# ...                              (   0,  4)],
# ...                    max=True)

# #8
# >>> tree.chance_node(name='OILFOUND',
# ...                  branches=[(21.74,    0,  4),
# ...                            (26.09, 1500,  4),
# ...                            (52.17, 3400,  4)])

# #9
# >>> tree.decision_node(name='DRILL',
# ...                    branches=[(-600, 10),
# ...                              (   0,  4)],
# ...                    max=True)

# #10
# >>> tree.chance_node(name='OILFOUND',
# ...                  branches=[(50.0,    0,  4),
# ...                            (30.0, 1500,  4),
# ...                            (20.0, 3400,  4)])


# >>> tree.display_nodes() # doctest: +NORMALIZE_WHITESPACE
# Node 0
#    Type: DECISION - Maximum Payoff
#    Name: TEST
#    Branches:
#                         Value  Next Node
#                       -55.000  1
#                         0.000  9
# <BLANKLINE>
# Node 1
#    Type: CHANCE
#    Name: STRUCT
#    Branches:
#          Chance         Value  Next Node
#           38.00         0.000  2
#           39.00         0.000  5
#           23.00         0.000  7
# <BLANKLINE>
# Node 2
#    Type: DECISION - Maximum Payoff
#    Name: DRILL
#    Branches:
#                         Value  Next Node
#                      -600.000  3
#                         0.000  4
# <BLANKLINE>
# Node 3
#    Type: CHANCE
#    Name: OILFOUND
#    Branches:
#          Chance         Value  Next Node
#           78.95         0.000  4
#           15.79      1500.000  4
#            5.26      3400.000  4
# <BLANKLINE>
# Node 4
#    Type: TERMINAL
#    Expr: (cumulative)
# <BLANKLINE>
# Node 5
#    Type: DECISION - Maximum Payoff
#    Name: DRILL
#    Branches:
#                         Value  Next Node
#                      -600.000  6
#                         0.000  4
# <BLANKLINE>
# Node 6
#    Type: CHANCE
#    Name: OILFOUND
#    Branches:
#          Chance         Value  Next Node
#           38.46         0.000  4
#           46.15      1500.000  4
#           15.38      3400.000  4
# <BLANKLINE>
# Node 7
#    Type: DECISION - Maximum Payoff
#    Name: DRILL
#    Branches:
#                         Value  Next Node
#                      -600.000  8
#                         0.000  4
# <BLANKLINE>
# Node 8
#    Type: CHANCE
#    Name: OILFOUND
#    Branches:
#          Chance         Value  Next Node
#           21.74         0.000  4
#           26.09      1500.000  4
#           52.17      3400.000  4
# <BLANKLINE>
# Node 9
#    Type: DECISION - Maximum Payoff
#    Name: DRILL
#    Branches:
#                         Value  Next Node
#                      -600.000  10
#                         0.000  4
# <BLANKLINE>
# Node 10
#    Type: CHANCE
#    Name: OILFOUND
#    Branches:
#          Chance         Value  Next Node
#           50.00         0.000  4
#           30.00      1500.000  4
#           20.00      3400.000  4
# <BLANKLINE>


# >>> tree.build_tree()


# >>> tree.display_tree() # doctest: +NORMALIZE_WHITESPACE
# |
# | #0
# \-------[D]
#          |
#          | #1
#          | TEST=-55
#          +-------[C]
#          |        |
#          |        | #2
#          |        | STRUCT=0
#          |        | Prob=38.00
#          |        +-------[D]
#          |        |        |
#          |        |        | #3
#          |        |        | DRILL=-600
#          |        |        +-------[C]
#          |        |        |        |
#          |        |        |        | #4
#          |        |        |        | OILFOUND=0
#          |        |        |        | Prob=78.95
#          |        |        |        +-------[T] TEST+STRUCT+DRILL+OILFOUND
#          |        |        |        |
#          |        |        |        | #5
#          |        |        |        | OILFOUND=1500
#          |        |        |        | Prob=15.79
#          |        |        |        +-------[T] TEST+STRUCT+DRILL+OILFOUND
#          |        |        |        |
#          |        |        |        | #6
#          |        |        |        | OILFOUND=3400
#          |        |        |        | Prob=5.26
#          |        |        |        \-------[T] TEST+STRUCT+DRILL+OILFOUND
#          |        |        |
#          |        |        | #7
#          |        |        | DRILL=0
#          |        |        \-------[T] TEST+STRUCT+DRILL
#          |        |
#          |        | #8
#          |        | STRUCT=0
#          |        | Prob=39.00
#          |        +-------[D]
#          |        |        |
#          |        |        | #9
#          |        |        | DRILL=-600
#          |        |        +-------[C]
#          |        |        |        |
#          |        |        |        | #10
#          |        |        |        | OILFOUND=0
#          |        |        |        | Prob=38.46
#          |        |        |        +-------[T] TEST+STRUCT+DRILL+OILFOUND
#          |        |        |        |
#          |        |        |        | #11
#          |        |        |        | OILFOUND=1500
#          |        |        |        | Prob=46.15
#          |        |        |        +-------[T] TEST+STRUCT+DRILL+OILFOUND
#          |        |        |        |
#          |        |        |        | #12
#          |        |        |        | OILFOUND=3400
#          |        |        |        | Prob=15.38
#          |        |        |        \-------[T] TEST+STRUCT+DRILL+OILFOUND
#          |        |        |
#          |        |        | #13
#          |        |        | DRILL=0
#          |        |        \-------[T] TEST+STRUCT+DRILL
#          |        |
#          |        | #14
#          |        | STRUCT=0
#          |        | Prob=23.00
#          |        \-------[D]
#          |                 |
#          |                 | #15
#          |                 | DRILL=-600
#          |                 +-------[C]
#          |                 |        |
#          |                 |        | #16
#          |                 |        | OILFOUND=0
#          |                 |        | Prob=21.74
#          |                 |        +-------[T] TEST+STRUCT+DRILL+OILFOUND
#          |                 |        |
#          |                 |        | #17
#          |                 |        | OILFOUND=1500
#          |                 |        | Prob=26.09
#          |                 |        +-------[T] TEST+STRUCT+DRILL+OILFOUND
#          |                 |        |
#          |                 |        | #18
#          |                 |        | OILFOUND=3400
#          |                 |        | Prob=52.17
#          |                 |        \-------[T] TEST+STRUCT+DRILL+OILFOUND
#          |                 |
#          |                 | #19
#          |                 | DRILL=0
#          |                 \-------[T] TEST+STRUCT+DRILL
#          |
#          | #20
#          | TEST=0
#          \-------[D]
#                   |
#                   | #21
#                   | DRILL=-600
#                   +-------[C]
#                   |        |
#                   |        | #22
#                   |        | OILFOUND=0
#                   |        | Prob=50.00
#                   |        +-------[T] TEST+DRILL+OILFOUND
#                   |        |
#                   |        | #23
#                   |        | OILFOUND=1500
#                   |        | Prob=30.00
#                   |        +-------[T] TEST+DRILL+OILFOUND
#                   |        |
#                   |        | #24
#                   |        | OILFOUND=3400
#                   |        | Prob=20.00
#                   |        \-------[T] TEST+DRILL+OILFOUND
#                   |
#                   | #25
#                   | DRILL=0
#                   \-------[T] TEST+DRILL


# >>> tree.evaluate()
# >>> tree.display_tree() # doctest: +NORMALIZE_WHITESPACE
# |
# | #0
# | ExpVal=544.92
# | (selected strategy)
# \-------[D]
#          |
#          | #1
#          | TEST=-55
#          | ExpVal=544.92
#          | (selected strategy)
#          +-------[C]
#          |        |
#          |        | #2
#          |        | STRUCT=0
#          |        | Prob=38.00
#          |        | ExpVal=-55.00
#          |        | (selected strategy)
#          |        +-------[D]
#          |        |        |
#          |        |        | #3
#          |        |        | DRILL=-600
#          |        |        | ExpVal=-239.31
#          |        |        +-------[C]
#          |        |        |        |
#          |        |        |        | #4
#          |        |        |        | OILFOUND=0
#          |        |        |        | Prob=78.95
#          |        |        |        | PathProb=0.00
#          |        |        |        | ExpVal=-655.00
#          |        |        |        +-------[T] TEST+STRUCT+DRILL+OILFOUND
#          |        |        |        |
#          |        |        |        | #5
#          |        |        |        | OILFOUND=1500
#          |        |        |        | Prob=15.79
#          |        |        |        | PathProb=0.00
#          |        |        |        | ExpVal=845.00
#          |        |        |        +-------[T] TEST+STRUCT+DRILL+OILFOUND
#          |        |        |        |
#          |        |        |        | #6
#          |        |        |        | OILFOUND=3400
#          |        |        |        | Prob=5.26
#          |        |        |        | PathProb=0.00
#          |        |        |        | ExpVal=2745.00
#          |        |        |        \-------[T] TEST+STRUCT+DRILL+OILFOUND
#          |        |        |
#          |        |        | #7
#          |        |        | DRILL=0
#          |        |        | PathProb=38.00
#          |        |        | ExpVal=-55.00
#          |        |        | (selected strategy)
#          |        |        \-------[T] TEST+STRUCT+DRILL
#          |        |
#          |        | #8
#          |        | STRUCT=0
#          |        | Prob=39.00
#          |        | ExpVal=560.24
#          |        | (selected strategy)
#          |        +-------[D]
#          |        |        |
#          |        |        | #9
#          |        |        | DRILL=-600
#          |        |        | ExpVal=560.24
#          |        |        | (selected strategy)
#          |        |        +-------[C]
#          |        |        |        |
#          |        |        |        | #10
#          |        |        |        | OILFOUND=0
#          |        |        |        | Prob=38.46
#          |        |        |        | PathProb=15.00
#          |        |        |        | ExpVal=-655.00
#          |        |        |        | (selected strategy)
#          |        |        |        +-------[T] TEST+STRUCT+DRILL+OILFOUND
#          |        |        |        |
#          |        |        |        | #11
#          |        |        |        | OILFOUND=1500
#          |        |        |        | Prob=46.15
#          |        |        |        | PathProb=18.00
#          |        |        |        | ExpVal=845.00
#          |        |        |        | (selected strategy)
#          |        |        |        +-------[T] TEST+STRUCT+DRILL+OILFOUND
#          |        |        |        |
#          |        |        |        | #12
#          |        |        |        | OILFOUND=3400
#          |        |        |        | Prob=15.38
#          |        |        |        | PathProb=6.00
#          |        |        |        | ExpVal=2745.00
#          |        |        |        | (selected strategy)
#          |        |        |        \-------[T] TEST+STRUCT+DRILL+OILFOUND
#          |        |        |
#          |        |        | #13
#          |        |        | DRILL=0
#          |        |        | PathProb=0.00
#          |        |        | ExpVal=-55.00
#          |        |        \-------[T] TEST+STRUCT+DRILL
#          |        |
#          |        | #14
#          |        | STRUCT=0
#          |        | Prob=23.00
#          |        | ExpVal=1510.13
#          |        | (selected strategy)
#          |        \-------[D]
#          |                 |
#          |                 | #15
#          |                 | DRILL=-600
#          |                 | ExpVal=1510.13
#          |                 | (selected strategy)
#          |                 +-------[C]
#          |                 |        |
#          |                 |        | #16
#          |                 |        | OILFOUND=0
#          |                 |        | Prob=21.74
#          |                 |        | PathProb=5.00
#          |                 |        | ExpVal=-655.00
#          |                 |        | (selected strategy)
#          |                 |        +-------[T] TEST+STRUCT+DRILL+OILFOUND
#          |                 |        |
#          |                 |        | #17
#          |                 |        | OILFOUND=1500
#          |                 |        | Prob=26.09
#          |                 |        | PathProb=6.00
#          |                 |        | ExpVal=845.00
#          |                 |        | (selected strategy)
#          |                 |        +-------[T] TEST+STRUCT+DRILL+OILFOUND
#          |                 |        |
#          |                 |        | #18
#          |                 |        | OILFOUND=3400
#          |                 |        | Prob=52.17
#          |                 |        | PathProb=12.00
#          |                 |        | ExpVal=2745.00
#          |                 |        | (selected strategy)
#          |                 |        \-------[T] TEST+STRUCT+DRILL+OILFOUND
#          |                 |
#          |                 | #19
#          |                 | DRILL=0
#          |                 | PathProb=0.00
#          |                 | ExpVal=-55.00
#          |                 \-------[T] TEST+STRUCT+DRILL
#          |
#          | #20
#          | TEST=0
#          | ExpVal=530.00
#          \-------[D]
#                   |
#                   | #21
#                   | DRILL=-600
#                   | ExpVal=530.00
#                   +-------[C]
#                   |        |
#                   |        | #22
#                   |        | OILFOUND=0
#                   |        | Prob=50.00
#                   |        | PathProb=0.00
#                   |        | ExpVal=-600.00
#                   |        +-------[T] TEST+DRILL+OILFOUND
#                   |        |
#                   |        | #23
#                   |        | OILFOUND=1500
#                   |        | Prob=30.00
#                   |        | PathProb=0.00
#                   |        | ExpVal=900.00
#                   |        +-------[T] TEST+DRILL+OILFOUND
#                   |        |
#                   |        | #24
#                   |        | OILFOUND=3400
#                   |        | Prob=20.00
#                   |        | PathProb=0.00
#                   |        | ExpVal=2800.00
#                   |        \-------[T] TEST+DRILL+OILFOUND
#                   |
#                   | #25
#                   | DRILL=0
#                   | PathProb=0.00
#                   | ExpVal=0.00
#                   \-------[T] TEST+DRILL


# >>> tree = DecisionTree()

# #0
# >>> tree.decision_node(name='TEST',
# ...                    branches=[(-55, 1),
# ...                              (  0, 2)],
# ...                    max=True)

# #1
# >>> tree.chance_node(name='STRUCT',
# ...                  branches=[(38.0,  0, 2),
# ...                            (39.0,  0, 2),
# ...                            (23.0,  0, 2)])

# #2
# >>> tree.decision_node(name='DRILL',
# ...                    branches=[(-600,  3),
# ...                            (   0,  4)],
# ...                    max=True)

# #3
# >>> prob_branch_1 = (0, [(1, [78.95, 38.46, 21.74]), 50.00])
# >>> prob_branch_2 = (0, [(1, [15.79, 46.15, 26.09]), 30.00])
# >>> prob_branch_3 = (0, [(1, [05.26, 15.38, 52.17]), 20.00])
# >>> tree.chance_node(name='OILFOUND',
# ...                  branches=[(prob_branch_1,    0,  4),
# ...                            (prob_branch_2, 1500,  4),
# ...                            (prob_branch_3, 3400,  4)])

# #4
# >>> tree.terminal_node()

# >>> tree.build_tree()
# >>> tree.evaluate()
# >>> tree.display_tree() # doctest: +NORMALIZE_WHITESPACE
# |
# | #0
# | ExpVal=544.92
# | (selected strategy)
# \-------[D]
#          |
#          | #1
#          | TEST=-55
#          | ExpVal=544.92
#          | (selected strategy)
#          +-------[C]
#          |        |
#          |        | #2
#          |        | STRUCT=0
#          |        | Prob=38.00
#          |        | ExpVal=-55.00
#          |        | (selected strategy)
#          |        +-------[D]
#          |        |        |
#          |        |        | #3
#          |        |        | DRILL=-600
#          |        |        | ExpVal=-239.31
#          |        |        +-------[C]
#          |        |        |        |
#          |        |        |        | #4
#          |        |        |        | OILFOUND=0
#          |        |        |        | Prob=78.95
#          |        |        |        | PathProb=0.00
#          |        |        |        | ExpVal=-655.00
#          |        |        |        +-------[T] TEST+STRUCT+DRILL+OILFOUND
#          |        |        |        |
#          |        |        |        | #5
#          |        |        |        | OILFOUND=1500
#          |        |        |        | Prob=15.79
#          |        |        |        | PathProb=0.00
#          |        |        |        | ExpVal=845.00
#          |        |        |        +-------[T] TEST+STRUCT+DRILL+OILFOUND
#          |        |        |        |
#          |        |        |        | #6
#          |        |        |        | OILFOUND=3400
#          |        |        |        | Prob=5.26
#          |        |        |        | PathProb=0.00
#          |        |        |        | ExpVal=2745.00
#          |        |        |        \-------[T] TEST+STRUCT+DRILL+OILFOUND
#          |        |        |
#          |        |        | #7
#          |        |        | DRILL=0
#          |        |        | PathProb=38.00
#          |        |        | ExpVal=-55.00
#          |        |        | (selected strategy)
#          |        |        \-------[T] TEST+STRUCT+DRILL
#          |        |
#          |        | #8
#          |        | STRUCT=0
#          |        | Prob=39.00
#          |        | ExpVal=560.24
#          |        | (selected strategy)
#          |        +-------[D]
#          |        |        |
#          |        |        | #9
#          |        |        | DRILL=-600
#          |        |        | ExpVal=560.24
#          |        |        | (selected strategy)
#          |        |        +-------[C]
#          |        |        |        |
#          |        |        |        | #10
#          |        |        |        | OILFOUND=0
#          |        |        |        | Prob=38.46
#          |        |        |        | PathProb=15.00
#          |        |        |        | ExpVal=-655.00
#          |        |        |        | (selected strategy)
#          |        |        |        +-------[T] TEST+STRUCT+DRILL+OILFOUND
#          |        |        |        |
#          |        |        |        | #11
#          |        |        |        | OILFOUND=1500
#          |        |        |        | Prob=46.15
#          |        |        |        | PathProb=18.00
#          |        |        |        | ExpVal=845.00
#          |        |        |        | (selected strategy)
#          |        |        |        +-------[T] TEST+STRUCT+DRILL+OILFOUND
#          |        |        |        |
#          |        |        |        | #12
#          |        |        |        | OILFOUND=3400
#          |        |        |        | Prob=15.38
#          |        |        |        | PathProb=6.00
#          |        |        |        | ExpVal=2745.00
#          |        |        |        | (selected strategy)
#          |        |        |        \-------[T] TEST+STRUCT+DRILL+OILFOUND
#          |        |        |
#          |        |        | #13
#          |        |        | DRILL=0
#          |        |        | PathProb=0.00
#          |        |        | ExpVal=-55.00
#          |        |        \-------[T] TEST+STRUCT+DRILL
#          |        |
#          |        | #14
#          |        | STRUCT=0
#          |        | Prob=23.00
#          |        | ExpVal=1510.13
#          |        | (selected strategy)
#          |        \-------[D]
#          |                 |
#          |                 | #15
#          |                 | DRILL=-600
#          |                 | ExpVal=1510.13
#          |                 | (selected strategy)
#          |                 +-------[C]
#          |                 |        |
#          |                 |        | #16
#          |                 |        | OILFOUND=0
#          |                 |        | Prob=21.74
#          |                 |        | PathProb=5.00
#          |                 |        | ExpVal=-655.00
#          |                 |        | (selected strategy)
#          |                 |        +-------[T] TEST+STRUCT+DRILL+OILFOUND
#          |                 |        |
#          |                 |        | #17
#          |                 |        | OILFOUND=1500
#          |                 |        | Prob=26.09
#          |                 |        | PathProb=6.00
#          |                 |        | ExpVal=845.00
#          |                 |        | (selected strategy)
#          |                 |        +-------[T] TEST+STRUCT+DRILL+OILFOUND
#          |                 |        |
#          |                 |        | #18
#          |                 |        | OILFOUND=3400
#          |                 |        | Prob=52.17
#          |                 |        | PathProb=12.00
#          |                 |        | ExpVal=2745.00
#          |                 |        | (selected strategy)
#          |                 |        \-------[T] TEST+STRUCT+DRILL+OILFOUND
#          |                 |
#          |                 | #19
#          |                 | DRILL=0
#          |                 | PathProb=0.00
#          |                 | ExpVal=-55.00
#          |                 \-------[T] TEST+STRUCT+DRILL
#          |
#          | #20
#          | TEST=0
#          | ExpVal=530.00
#          \-------[D]
#                   |
#                   | #21
#                   | DRILL=-600
#                   | ExpVal=530.00
#                   +-------[C]
#                   |        |
#                   |        | #22
#                   |        | OILFOUND=0
#                   |        | Prob=50.00
#                   |        | PathProb=0.00
#                   |        | ExpVal=-600.00
#                   |        +-------[T] TEST+DRILL+OILFOUND
#                   |        |
#                   |        | #23
#                   |        | OILFOUND=1500
#                   |        | Prob=30.00
#                   |        | PathProb=0.00
#                   |        | ExpVal=900.00
#                   |        +-------[T] TEST+DRILL+OILFOUND
#                   |        |
#                   |        | #24
#                   |        | OILFOUND=3400
#                   |        | Prob=20.00
#                   |        | PathProb=0.00
#                   |        | ExpVal=2800.00
#                   |        \-------[T] TEST+DRILL+OILFOUND
#                   |
#                   | #25
#                   | DRILL=0
#                   | PathProb=0.00
#                   | ExpVal=0.00
#                   \-------[T] TEST+DRILL


# """


# if __name__ == "__main__":
#     import doctest

#     doctest.testmod()
