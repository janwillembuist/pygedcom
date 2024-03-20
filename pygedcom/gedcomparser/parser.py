from pygedcom.gedcomparser.elements import FamilyTree


class Parser:
    """Parses the raw gedcom file into a Pygedcom FamilyTree instance"""

    def __init__(self, file):
        with open(file, mode='r', encoding='utf-8-sig') as f:
            self.lines = f.readlines()
            i = 0
            self.separators = []
            for line in self.lines:
                if line[0] == '0':
                    self.separators.append([i, line])
                i += 1

    def build_tree(self):
        # Init tree
        tree = FamilyTree()

        # For each part of GEDCOM file, fill the tree
        for i, (line, title) in enumerate(self.separators):
            if 'INDI' in title:
                # Add inidividual to the tree with this part of the file
                tree.add_individual(self.lines[line:self.separators[i + 1][0]])
            elif 'FAM' in title:
                # Add family to the tree with this part of the file
                tree.add_family(self.lines[line:self.separators[i + 1][0]])

        # Serialize tree
        tree.serialize()

        return tree
