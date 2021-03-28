
class Individual:
    def __init__(self, gedcomlines):
        self.fullname = None
        self.sex = None
        self.upperfam = None
        self.lowerfam = None

        for line in gedcomlines:
            # Save stuff into class
            if line.startswith('1 NAME'):
                self.fullname = line[7:-2]
            elif line.startswith('1 SEX'):
                self.sex = line[6]
            elif line.startswith('1 FAMS'):
                self.lowerfam = line.split('@')[1]
            elif line.startswith('1 FAMC'):
                self.upperfam = line.split('@')[1]

    def __str__(self):
        return '{}, {}'.format(self.fullname, self.sex)

class Family:
    def __init__(self, gedcomlines):
        self.husband = None
        self.wife = None
        self.children = []

        for line in gedcomlines:
            if line.startswith('1 HUSB'):
                self.husband = line.split('@')[1]
            elif line.startswith('1 WIFE'):
                self.wife = line.split('@')[1]
            elif line.startswith('1 CHIL'):
                self.children.append(line.split('@')[1])

    def __str__(self):
        return '{} & {}'.format(self.husband, self.wife)
