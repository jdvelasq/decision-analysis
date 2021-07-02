#
# SuperTree user guide simple bid example
#

# def test_tree_repr():


# >>> from dmak.examples import stguide_bid
# >>> from dmak.decisiontree import DecisionTree
# >>> nodes = stguide_bid()
# >>> tree = DecisionTree(
# ...     variables=nodes,
# ...     initial_variable="bid"
# ... )
# >>> tree
# STRUCTURE    NAMES    OUTCOMES     PROBABILIES
# <BLANKLINE>
# 0D1 14       bid      500 700
# 1C2 6 10     compbid  400 600 800  .350 .500 .150
# 2C3 4 5      cost     200 400 600  .250 .500 .250
# 3T           profit
# 4T           profit
# 5T           profit
# 6C7 8 9      cost     200 400 600  .250 .500 .250
# 7T           profit
# 8T           profit
# 9T           profit
# 10C11 12 13  cost     200 400 600  .250 .500 .250
# 11T          profit
# 12T          profit
# 13T          profit
# 14C15 19 23  compbid  400 600 800  .350 .500 .150
# 15C16 17 18  cost     200 400 600  .250 .500 .250
# 16T          profit
# 17T          profit
# 18T          profit
# 19C20 21 22  cost     200 400 600  .250 .500 .250
# 20T          profit
# 21T          profit
# 22T          profit
# 23C24 25 26  cost     200 400 600  .250 .500 .250
# 24T          profit
# 25T          profit
# 26T          profit
