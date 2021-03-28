
class Individual:
    def __init__(self, gedcomlines):
        self.fullname = None
        self.sex = None
        self.upperfam = None
        self.lowerfam = None

        for line in gedcomlines:
            if line.startswith('1 NAME'):
                # Delete '1 NAME ' and '\n'
                self.fullname = line[7:-2]
            elif line.startswith('1 SEX'):
                # Delete '1 SEX ' and '\n', only keep M/F
                self.sex = line[6]
            elif line.startswith('1 FAMS'):
                self.lowerfam = line.split('@')[1]
            elif line.startswith('1 FAMC'):
                self.upperfam = line.split('@')[1]

class Family:
    def __init__(self, gedcomlines):
        pass
