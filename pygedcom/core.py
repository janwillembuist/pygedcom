
class Parser:
    def __init__(self, file):
        with open(file, mode='r', encoding='utf-8-sig') as f:
            lines = f.readlines()
            i = 0
            separators = []
            for line in lines:
                if line[0] == '0':
                    separators.append([i, line])
                i += 1
            print(separators)
class FamilyTree:
    pass
