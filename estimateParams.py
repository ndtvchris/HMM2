import itertools


class estimateParams:

    def __init__(self, infile):
        '''
        Class constructor
        :param infile: file to parse from
        '''

        with open(infile) as file:
            self.observables = file.readline().rstrip()
            for line in file:

                # if they're all letters, must be the path string
                if line.rstrip().isalpha():
                    self.path = line.rstrip()
                # if the first letter is in observables, they're emissions
                elif self.observables.find(line.split()[0]) != -1:
                    self.emissions = line.split()
                # if it's not in observables but still a letter, they're states
                elif self.observables.find(line.split()[0]) == -1 and line.split()[0].isalpha():
                    self.states = line.split()
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
                    self.statesEmit[state][self.observables[index]] = 1
            holder.clear()

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
            for key in self.statesEmit[state]:
                self.statesEmit[state][key] = self.statesEmit[state][key] / eTotal
            for key in self.statesTransmit[state]:
                if self.statesTransmit[state][key] == 0:
                    self.statesTransmit[state][key] = 1 / len(self.states)
                else:
                    self.statesTransmit[state][key] = self.statesTransmit[state][key] / tTotal

    def writeFile(self):
        '''
        This function writes out all the data with nice formatting

        '''

        printer = []
        with open('p23.out.txt', 'w') as out:
            out.write('\t')
            # write transmissions first
            out.write('\t\t'.join(self.states) + '\n')
            # get transmission probs from each state
            for key in self.statesTransmit:
                printer.append(key)
                [printer.append(f'{i:<4.3}') for i in self.statesTransmit[key].values()]
                out.write('\t'.join(printer) + '\n')
                printer = []
            # now put the slashes in
            out.write('--------\n')
            out.write('\t')
            out.write('\t\t'.join(self.emissions) + '\n')
            for key in self.statesEmit:
                printer.append(key)
                for emit in self.emissions:
                    printer.append(f'{self.statesEmit[key][emit]:<4.3}')
                out.write('\t'.join(printer) + '\n')
                printer = []


ep = estimateParams('parame.txt')
ep.findEmissions()
ep.writeFile()
print(ep.emissions)
print(ep.states)
print(ep.statesEmit)
print(ep.statesTransmit)


