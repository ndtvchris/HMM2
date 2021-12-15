# will have to hard-code in the estimateParams stuff...
import fviterbi as fvi
import esparams2 as es2


class franken:
    '''
    This class does Viterbi, estimates new params from that, and then repeats.
    '''

    # init should set up and run first iteration of vit and params
    def __init__(self, infile, iter=1):
        self.vit = fvi.viterbi(infile)  # prepares for viterbi. viterbi has data
        self.maxProb = self.vit.pathTrace()  # holds max prob for comparisons
        # vit.backtrace now returns a path
        self.es = es2.estimateParams(self.vit.backTrace(), self.vit.observables, self.vit.transmissions,
                                     self.vit.emissions)
        self.es.findEmissions()
        self.iter = iter

    # repeats vit and param until maxProb can't improve anymore
    def process(self):
        currentProb = 0
        for x in range(self.iter):
            # convert es info into vit format
            self.vit.stateEmission, self.vit.stateTransmission = self.convertForVit()
            # then do vit
            currentProb = self.vit.pathTrace()
            # if current prob is better, update
            if currentProb > self.maxProb:
                self.maxProb = currentProb
            # after, estimate params again
            newPath = self.vit.backTrace()
            self.es.path = newPath
            self.es.findEmissions()

    # this converts data structures into format that vit can use
    def convertForVit(self):
        emitForVit = {k: [] for k in self.es.states}
        transmitForVit = {k: [] for k in self.es.states}
        holder = []
        # do for transmits first
        for state in self.es.statesTransmit:
            [holder.append(i) for i in self.es.statesTransmit[state].values()]
            transmitForVit[state] = holder
            holder = []
        # now the emits
        for state in self.es.statesEmit:
            for key in self.es.emissions:
                holder.append(self.es.statesEmit[state][key])
            emitForVit[state] = holder
            holder = []
        return emitForVit, transmitForVit

    def printout(self):

        self.es.writeFile()





fr = franken('vitlearn.txt', 100)
fr.process()
fr.printout()
'''

'''