import re
from pygedcom.elements import Individual, Family

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
                tree.add_individual(self.lines[line:self.separators[i+1][0]])
            elif 'FAM' in title:
                # Add family to the tree with this part of the file
                tree.add_family(self.lines[line:self.separators[i+1][0]])
        return tree

class FamilyTree:
    """Pygedcom's representation of a family tree."""
    def __init__(self):
        # key: ID, value: Individual/Family
        self.individuals = {}
        self.families = {}

        # key: Individual.fullname, value: ID
        self.individuals_lookup = {}

        self.individual_amount = 0
        self.family_amount = 0

    def add_individual(self, gedcomlines):
        # Save person ID in dict and pass data to Individual class, save fullname to lookup table
        person_id = gedcomlines[0].split('@')[1]
        self.individuals[person_id] = Individual(gedcomlines)
        self.individuals_lookup[self.individuals[person_id].fullname] = person_id
        self.individual_amount += 1

    def add_family(self, gedcomlines):
        # Save family ID in dict and pass data to Family class
        self.families[gedcomlines[0].split('@')[1]] = Family(gedcomlines)
        self.family_amount += 1

    def find(self, entrystr):
        """Returns a list of individuals for a given Search query.

        Currently searches the individuals_lookup dictionary, which containts fullnames of the Individuals inside the
        FamilyTree.

        Speed could be optimized here by implementing a trie for example.
        :param str entrystr: Search query
        :return: List of individuals
        :rtype: list
        """
        return [self.select_person(key)
                for key in self.individuals_lookup.keys() if re.search(entrystr, key, re.IGNORECASE)]

    def select_person(self, fullname):
        """ Selects person from fullname

        :param str fullname: Fullname of person
        :return: Individual class
        :rtype: Individual
        """
        return self.individuals[self.individuals_lookup[fullname]]
