class decodingMeSoftly:

    def __init__(self, infile):
        self.stateEmission = {}  # holds emissions probs at each state
        self.stateTransmission = {}  # holds transmission probs at each state
        self.emissions = []  # emissions organized by index based on table read in
        self.states = []  # states by index
        self.observables = ''
        self.forwardDict = {}
        self.backwardDict = {}
        self.prevProbs = {}  # for forward
        self.afterProbs = {}  # for backward
        self.finalProb = 0  # probability of sequence
        self.parseFile(infile)

    def parseFile(self, infile):
        '''
        This function parses in the file
        :param infile: file to parse from

        '''
        holdList = []
        with open(infile) as file:
            self.observables = file.readline().rstrip()
            for line in file:
                checker = line.split()
                try:
                    # if the first letter read is in observables and not yet in emissions, put them in
                    if self.observables.find(checker[0]) != -1 and checker[0] not in self.emissions:
                        [self.emissions.append(checker[i]) for i in range(len(checker))]
                    # letter followed by a decimal means transmission
                    elif checker[0].isalpha() and checker[1].find('.') != -1 and len(self.stateTransmission) < len(
                            self.states):
                        [holdList.append(float(checker[i])) for i in range(1, len(checker))]
                        self.stateTransmission[checker[0]] = holdList
                        holdList = []
                    # letter followed by decimal and transmits full means that it's emissions
                    elif checker[0].isalpha() and checker[1].find('.') != -1 and len(self.stateEmission) < len(
                            self.states):
                        [holdList.append(float(checker[i])) for i in range(1, len(checker))]
                        self.stateEmission[checker[0]] = holdList
                        holdList = []
                    # otherwise they're states
                    elif checker[0].isalpha() and checker[0] not in self.emissions and checker[
                        0] not in self.states:
                        [self.states.append(checker[i]) for i in range(len(checker))]
                        self.states = sorted(set(self.states))
                except IndexError:
                    continue
            # initialize dictionaries to use later
            self.prevProbs = {k: 0.5 for k in self.states}
            self.afterProbs = {k: 1.0 for k in self.states}
            self.forwardDict = {k: [] for k in self.states}
            self.backwardDict = {k: [] for k in self.states}

    def forward(self):
        '''
        This function performs the forward algorithm

        '''

        newProbs = {k: 0 for k in self.states}
        # for each observable, get the sum of probabilities at each state
        for index in range(len(self.observables)):

            # first index means a different calculation
            if index == 0:
                for state in self.states:
                    emitProb = self.stateEmission[state][self.emissions.index(self.observables[index])]
                    prevProb = self.prevProbs[state]
                    self.forwardDict[state].append(emitProb * prevProb)
                    self.prevProbs[state] = emitProb * prevProb

            # otherwise it's all the same
            else:
                # for each state, calculate probabilities of transmission, emission and sum them up
                for state in self.states:
                    total = 0
                    emitProb = self.stateEmission[state][self.emissions.index(self.observables[index])]
                    for key in self.stateTransmission:
                        prevProb = self.prevProbs[key]
                        transIndex = self.states.index(state)
                        transProb = self.stateTransmission[key][transIndex]
                        hold = emitProb * prevProb * transProb
                        total += hold
                    # stores values to use in subsequent operations
                    newProbs[state] = total
                    self.forwardDict[state].append(total)
                # updates previous probabilities
                for probKey in self.prevProbs:
                    self.prevProbs[probKey] = newProbs[probKey]
                # if at the end, store final probability for final soft decode
                if index == len(self.observables) - 1:
                    for state in self.prevProbs:
                        self.finalProb += self.prevProbs[state]

    def backward(self):
        '''
        This function does the backward algorithm

        '''
        newProbs = {k: 0 for k in self.states}
        # goes backward but does the same summing of probabilities
        for index in range(len(self.observables) - 1, -1, -1):
            # first index is a special case
            if index == len(self.observables) - 1:

                for state in self.states:
                    self.backwardDict[state].append(1.0)

            # otherwise calculate the same way
            else:
                for state in self.states:
                    total = 0
                    for key in self.stateTransmission:
                        emitProb = self.stateEmission[key][self.emissions.index(self.observables[index + 1])]
                        nextProb = self.afterProbs[key]
                        transProb = self.stateTransmission[state][self.states.index(key)]
                        hold = emitProb * nextProb * transProb
                        total += hold
                    # stores values for later
                    newProbs[state] = total
                    self.backwardDict[state].insert(0, total)
                # updates probabilities
                for probKey in self.afterProbs:
                    self.afterProbs[probKey] = newProbs[probKey]

    def mather(self):
        '''
        This function does the math
        :return: probsDict - dictionary of probabilities
        '''
        probsDict = {}
        holdList = []
        # goes through dictionaries and calculates conditional probabilities
        for state in self.states:
            for index in range(len(self.observables)):
                timeProb = self.forwardDict[state][index] * self.backwardDict[state][index] / self.finalProb
                holdList.append(timeProb)
            probsDict[state] = holdList
            holdList = []
        return probsDict


    def writeIt(self):
        '''
        This function writes out the data nicely

        '''
        printer = []
        probsDict = self.mather()
        with open('p24out.txt', 'w') as out:
            out.write('\t\t'.join(self.states) + '\n')
            for x in range(len(self.observables)):
                for state in self.states:
                    printer.append(f'{probsDict[state][x]:<6.4f}')
                out.write('\t'.join(printer) + '\n')
                printer = []


dms = decodingMeSoftly('tester.txt')
dms.forward()
dms.backward()


dms.writeIt()


