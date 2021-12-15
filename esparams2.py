import itertools


class estimateParams:

    def __init__(self, path: str, obser: str, states: list , emissions: list):
        '''
        Class constructor

        '''
        self.observables = obser
        self.path = path
        self.emissions = emissions
        self.states = states
        # initialize dictionaries
        self.statesEmit = {k: {} for k in self.states}
        self.statesTransmit = {k: {} for k in self.states}

    def finder(self, pattern):
        '''
        This function finds a certain pattern in a string
        :param pattern: pattern to search for
        :return: generator with indices of pattern
        '''
        i = self.path.find(pattern)
        while i != -1:
            yield i
            i = self.path.find(pattern, i + 1)

    def findEmissions(self):
        '''
        This function finds the emissions at each state

        '''


        holder = []
        holder2 = []
        # creates 2mers representing transmissions
        combos = [''.join(w) for w in (itertools.product(self.states, repeat=2))]

        # first gets emissions by state
        for state in self.states:
            # find indices in state string
            [holder.append(i) for i in self.finder(state)]
            # at each index found, check what's being emitted

            for index in holder:
                if self.observables[index] in self.statesEmit[state]:
                    self.statesEmit[state][self.observables[index]] += 1
                else:
                    self.statesEmit[state][self.observables[index]] = 1.0
            holder.clear()
            # here i have to make all the other emissions that don't get seen
            for emit in self.emissions:
                if emit in self.statesEmit[state]:
                    continue
                else:
                    self.statesEmit[state][emit] = 0.0

            # then, set dictionary for transmissions
            for combo in combos:
                [holder2.append(i) for i in self.finder(combo)]
                if combo.startswith(state):
                    self.statesTransmit[state][combo] = len(holder2)
                    holder2 = []
                else:
                    holder2 = []
                    continue

            # after we have all the data, do math
            # need to account for not states that aren't present
            eTotal = sum(self.statesEmit[state].values())
            tTotal = sum(self.statesTransmit[state].values())
            if tTotal == 0:
                for key in self.statesTransmit[state]:
                    self.statesTransmit[state][key] = 1.0 / len(self.states)

            else:
                for key in self.statesEmit[state]:
                    self.statesEmit[state][key] = self.statesEmit[state][key] / eTotal
                for key in self.statesTransmit[state]:
                    if sum(self.statesTransmit[state].values()) == 0:
                        self.statesTransmit[state][key] = 1 / len(self.states)
                    else:
                        self.statesTransmit[state][key] = self.statesTransmit[state][key] / tTotal

    def writeFile(self):
        '''
        This function writes out all the data with nice formatting

        '''

        printer = []
        with open('/Users/christophernguyen/Desktop/vitlearnop.txt', 'w') as out:
            #out.write('\t')
            # write transmissions first
            out.write('\t'.join(self.states) + '\t\n')
            # get transmission probs from each state
            for key in self.statesTransmit:
                printer.append(key)
                [printer.append(str(i)) for i in self.statesTransmit[key].values()]
                out.write('\t'.join(printer) + '\n')
                printer = []
            # now put the slashes in
            out.write('--------\n')
            out.write('\t')
            out.write('\t'.join(self.emissions) + '\t\n')
            for key in self.statesEmit:
                printer.append(key)
                for emit in self.emissions:
                    printer.append(str(self.statesEmit[key][emit]))
                if key == self.states[len(self.states) - 1]:
                    out.write('\t'.join(printer))
                else:
                    out.write('\t'.join(printer) + '\n')
                printer = []




