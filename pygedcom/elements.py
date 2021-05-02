
class Individual:
    def __init__(self, gedcomlines):
        self.fullname = None
        self.sex = None
        self.birthdate = None
        self.deathdate = None
        self.upperfam = None
        self.lowerfam = None

        in_birt = False
        in_deat = False

        for line in gedcomlines:
            if in_birt:
                print('inbirt')
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
                self.fullname = line[7:-2].replace('/', '')
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
