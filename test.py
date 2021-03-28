from pygedcom.core import Parser

file = 'data/555SAMPLE.GED'
tree = Parser(file).build_tree()
print(tree.individuals_lookup)
