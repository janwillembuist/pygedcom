import re

class Individual:
    def __init__(self, gedcomlines):
        # TODO: more info!
        self.fullname = 'None'
        self.firstname = 'None'
        self.lastname = 'None'
        self.sex = 'None'
        self.birthdate = 'None'
        self.deathdate = 'None'
        self.upperfam = None
        self.lowerfam = None

        # Fill info
        self._scan_input(gedcomlines)

    def __str__(self):
        return '{}, {}'.format(self.fullname, self.sex)

    def _scan_input(self, gedcomlines):
        # Analyze input to fill Individual's attributes line by line
        in_birt = False
        in_deat = False

        for line in gedcomlines:
            # Cut of newlines and spaces
            line = line.strip()
            if in_birt:
                if line.startswith('2 DATE'):
                    self.birthdate = line[7:]
                elif line.startswith('1'):
                    in_birt = False

            if in_deat:
                if line.startswith('2 DATE'):
                    self.deathdate = line[7:]
                elif line.startswith('1'):
                    in_deat = False

            # Save stuff into class
            if line.startswith('1 NAME'):
                self.fullname = line[7:].replace('/', '')
            elif line.startswith('1 SEX'):
                self.sex = line[6]
            elif line.startswith('1 FAMS'):
                self.lowerfam = line.split('@')[1]
            elif line.startswith('1 FAMC'):
                self.upperfam = line.split('@')[1]
            elif line.startswith('1 BIRT'):
                in_birt = True
            elif line.startswith('1 DEAT'):
                in_deat = True
            elif line.startswith('2 SURN'):
                self.lastname = line[7:]
            elif line.startswith('2 GIVN'):
                self.firstname = line[7:]

    def serialize_individual(self, families):
        if self.upperfam is not None:
            self.upperfam = families[self.upperfam]
        if self.lowerfam is not None:
            self.lowerfam = families[self.lowerfam]


class Family:
    def __init__(self, gedcomlines):
        self.husband = None
        self.wife = None
        self.children = []

        # Get attributes
        self._scan_input(gedcomlines)

    def __str__(self):
        return '{} & {}'.format(self.husband, self.wife)

    def _scan_input(self, gedcomlines):
        for line in gedcomlines:
            if line.startswith('1 HUSB'):
                self.husband = line.split('@')[1]
            elif line.startswith('1 WIFE'):
                self.wife = line.split('@')[1]
            elif line.startswith('1 CHIL'):
                self.children.append(line.split('@')[1])

    def serialize_family(self, individuals):
        if self.husband is not None:
            self.husband = individuals[self.husband]
        if self.wife is not None:
            self.wife = individuals[self.wife]
        if len(self.children) > 0:
            newkids = []
            for child in self.children:
                newkids.append(individuals[child])
            self.children = newkids

class FamilyTree:
    """Pygedcom's representation of a family tree."""
    def __init__(self):
        # key: ID, value: Individual/Family
        self.individuals = {}
        self.families = {}

        # key: Individual.fullname, value: ID
        self.individuals_lookup = {}

        # The selected person
        self._selected_individual = None

        self.individual_amount = 0
        self.family_amount = 0

    @property
    def selected_individual(self):
        return self._selected_individual

    @selected_individual.setter
    def selected_individual(self, value):
        if isinstance(value, Individual):
            self._selected_individual = value
        else:
            raise AssertionError('Not a valid Individual')

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

    def find_ancestors(self, tree_list=None, depth=2):
        if tree_list is None:
            level = 1
            tree_list = [[[level, self.selected_individual.firstname + '\n' + self.selected_individual.lastname]]]
            fams = [[None, self.selected_individual.upperfam]]
        else:
            fams = tree_list[0]
            level = fams[0][0]

        level *= 2
        generation = []
        for fam in fams:
            fam = fam[1]
            if isinstance(fam, Family):
                if isinstance(fam.husband, Individual):
                    father = fam.husband.firstname + '\n' + fam.husband.lastname
                else:
                    father = None
                if isinstance(fam.wife, Individual):
                    mother = fam.wife.firstname + '\n' + fam.wife.lastname
                else:
                    mother = None
                generation.append([level, father])
                generation.append([level + 1, mother])
            else:
                tree_list.append([[level, None], [level + 1, None]])

            level += 2
        tree_list.append(generation)

        return tree_list

    def serialize(self):
        for fam_id, family in self.families.items():
            self.families[fam_id].serialize_family(self.individuals)

        for ind_id, individual in self.individuals.items():
            self.individuals[ind_id].serialize_individual(self.families)

