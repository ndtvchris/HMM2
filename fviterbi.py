class viterbi:

    def __init__(self, infile):
        self.stateEmission = {}  # holds emissions probs at each state
        self.stateTransmission = {}  # holds transmission probs at each state
        self.emissions = []  # emissions organized by index based on table read in
        self.transmissions = []  # transmissions by index
        self.endState = ''  # from where the end node got the best prob
        self.observables = ''
        self.prevProbs = {}
        self.bestParent = {}
        self.maxProb = 0
        self.parseFile(infile)

    def parseFile(self, infile):
        holdList = []
        with open(infile) as file:
            file.readline()
            file.readline()
            self.observables = file.readline().rstrip()
            for line in file:
                checker = line.split()
                try:
                    # if the first letter read is in observables and not yet in emissions, put them in
                    if self.observables.find(checker[0]) != -1 and checker[0] not in self.emissions:
                        [self.emissions.append(checker[i]) for i in range(len(checker))]
                    # letter followed by a decimal means transmission, so flag that
                    elif checker[0].isalpha() and checker[1].find('.') != -1 and len(self.stateTransmission) < len \
                                (self.transmissions):
                        [holdList.append(float(checker[i])) for i in range(1, len(checker))]
                        self.stateTransmission[checker[0]] = holdList

                        holdList = []
                    # letter followed by decimal and transmits full means that it's emissions
                    elif checker[0].isalpha() and checker[1].find('.') != -1 and len(self.stateEmission) < len \
                                (self.transmissions):
                        [holdList.append(float(checker[i])) for i in range(1, len(checker))]
                        self.stateEmission[checker[0]] = holdList
                        holdList = []

                    elif checker[0].isalpha() and checker[0] not in self.emissions \
                            and checker[0] not in self.transmissions:
                        [self.transmissions.append(checker[i]) for i in range(len(checker))]
                        self.transmissions = sorted(set(self.transmissions))

                except IndexError:
                    continue

            self.prevProbs = {k: 0.5 for k in self.transmissions}
            self.bestParent = {k: [] for k in self.transmissions}

    def pathTrace(self):
        maxProb = 0
        newProbs = {k: 0 for k in self.transmissions}
        for index in range(len(self.observables)):
            hold = 0

            if index == 0:
                for state in self.transmissions:
                    emitProb = self.stateEmission[state][self.emissions.index(self.observables[index])]
                    prevProb = self.prevProbs[state]
                    self.prevProbs[state] = emitProb * prevProb

            else:
                currentBest = ''
                for state in self.transmissions:
                    total = 0  # current total value
                    emitProb = self.stateEmission[state][self.emissions.index(self.observables[index])]
                    for key in self.stateTransmission:

                        prevProb = self.prevProbs[key]
                        transIndex = self.transmissions.index(state)
                        transProb = self.stateTransmission[key][transIndex]
                        hold = emitProb * prevProb * transProb
                        if hold > total:
                            total = hold
                            newProbs[state] = total
                            currentBest = key
                    self.bestParent[state].append(currentBest)
                for key in self.prevProbs:
                    self.prevProbs[key] = newProbs[key]
                newProbs = {k: 0 for k in self.transmissions}
                if index == len(self.observables) - 1:
                    for state in self.prevProbs:

                        if self.prevProbs[state] > maxProb:
                            maxProb = self.prevProbs[state]
                            self.endState = state
        self.prevProbs = {k: 0.5 for k in self.transmissions}
        return maxProb

    # returns path
    def backTrace(self):
        writeList = [self.endState]
        current = self.endState
        for x in range(len(self.bestParent[self.endState]) - 1, -1, -1):
            writeList.insert(0, self.bestParent[current][x])
            current = self.bestParent[current][x]
        self.bestParent = {k: [] for k in self.transmissions}
        return ''.join(writeList)

'''
v = viterbi('vittest.txt')
print(v.emissions)
print(v.transmissions)
print(v.stateEmission)
print(v.stateTransmission)

print(v.pathTrace())
v.backTrace()
'''


