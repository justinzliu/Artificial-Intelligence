#!/usr/bin/python3
import sys
import os
import random
import math

import numpy as np
import operator

#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
num_hours_i_spent_on_this_assignment = 35
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
# Until the TA's and other students posted explanations, outputs, and formulas on piazza, I had no way of completing this assignment. Posterior in particular was impossible  to implement given lecture notes.
#####################################################
#####################################################



# Outputs a random integer, according to a multinomial
# distribution specified by probs.
def rand_multinomial(probs):
    # Make sure probs sum to 1
    assert(abs(sum(probs) - 1.0) < 1e-5)
    rand = random.random()
    for index, prob in enumerate(probs):
        if rand < prob:
            return index
        else:
            rand -= prob
    return 0

# Outputs a random key, according to a (key,prob)
# iterator. For a probability dictionary
# d = {"A": 0.9, "C": 0.1}
# call using rand_multinomial_iter(d.items())
def rand_multinomial_iter(iterator):
    rand = random.random()
    for key, prob in iterator:
        if rand < prob:
            return key
        else:
            rand -= prob
    return 0


class HMM():

    def __init__(self):
        self.num_states = 2
        self.prior      = np.array([0.5, 0.5])
        self.transition = np.array([[0.999, 0.001], [0.01, 0.99]])
        self.emission   = np.array([{"A": 0.291, "T": 0.291, "C": 0.209, "G": 0.209},
                                    {"A": 0.169, "T": 0.169, "C": 0.331, "G": 0.331}])

    # Generates a sequence of states and characters from
    # the HMM model.
    # - length: Length of output sequence
    def sample(self, length):
        sequence = []
        states = []
        rand = random.random()
        cur_state = rand_multinomial(self.prior)
        for i in range(length):
            states.append(cur_state)
            char = rand_multinomial_iter(self.emission[cur_state].items())
            sequence.append(char)
            cur_state = rand_multinomial(self.transition[cur_state])
        return sequence, states

    # Generates a emission sequence given a sequence of states
    def generate_sequence(self, states):
        sequence = []
        for state in states:
            char = rand_multinomial_iter(self.emission[state].items())
            sequence.append(char)
        return sequence

    # Outputs the most likely sequence of states given an emission sequence
    # - sequence: String with characters [A,C,T,G]
    # return: list of state indices, e.g. [0,0,0,1,1,0,0,...]
    def viterbi(self, sequence):
        ###########################################
        # Start your code

        def max_wState(l):
        	#finds max values in list l and returns [value,index]
        	l_len = len(l)
        	maxVal = float("-inf")
        	maxIndex = 0
        	if l_len > 0:
        		for x in range(l_len):
        			if l[x] > maxVal:
        				maxIndex = x
        				maxVal = l[x]
        	else:
        		print("max_wState: empty list evaluated")
        	return [maxVal,maxIndex]

        ### viterbi function ###
        seq_len = len(sequence)
        v_dist = np.zeros((seq_len,self.num_states),dtype=float)
        v_prev = np.zeros((seq_len,self.num_states),dtype=int)
        #store probability p as 10 base log of x. 10^x = p
        for st in range(self.num_states):
        	v_dist[0][st] = math.log(self.prior[st]) + math.log(self.emission[st][sequence[0]])
        for emi in range(1,seq_len):
        	for curr_st in range(self.num_states):
        		prob = []
        		for prev_st in range(self.num_states):
        			#previous state probability * probability of state (curr_st) given emission (emi) * transition probability from prev state to current
        			prob.append(v_dist[emi-1][prev_st] + math.log(self.emission[curr_st][sequence[emi]]) + math.log(self.transition[prev_st][curr_st]))
        		maxVal = max_wState(prob)
        		v_dist[emi][curr_st] = maxVal[0]
        		v_prev[emi][curr_st] = maxVal[1]
        prob = []
        for st in range(self.num_states):
        	prob.append(v_dist[seq_len-1][st])
        maxVal = max_wState(prob)
       	path = [maxVal[1]]
       	for seq in range(seq_len-2,-1,-1):
       		path.insert(0,v_prev[seq+1][path[0]])
       	return path
        # End your code
        ###########################################

    def log_sum(self, factors):
        if abs(min(factors)) > abs(max(factors)):
            a = min(factors)
        else:
            a = max(factors)

        total = 0
        for x in factors:
            total += math.exp(x - a)
        return a + math.log(total)

    # - sequence: String with characters [A,C,T,G]
    # return: posterior distribution. shape should be (len(sequence), 2)
    # Please use log_sum() in posterior computations.
    def posterior(self, sequence):
        ###########################################
        # Start your code
        #return array

        #forward
        seq_len = len(sequence)
        fwd = np.zeros((seq_len,self.num_states),dtype=float)
        prev_st = [] 
        for st in range(self.num_states):
            fwd[0][st] = math.log(self.prior[st]) + math.log(self.emission[st][sequence[0]])
            prev_st.append(fwd[0][st])
        for emi in range(1,seq_len):
            curr_st = []
            for st in range(self.num_states):
                prev_toSum = []
                for pst in range(self.num_states):
                    prev_toSum.append(prev_st[pst] + math.log(self.transition[pst][st]))
                prev_sum = self.log_sum(prev_toSum)
                curr_st.append(math.log(self.emission[st][sequence[emi]]) + prev_sum)
            for st in range(self.num_states):
                fwd[emi][st] = curr_st[st]
            prev_st = curr_st

        #backward
        bwd = np.zeros((seq_len,self.num_states),dtype=float)
        prev_st = []
        for st in range(self.num_states):
            bwd[seq_len-1][st] = math.log(1)
            prev_st.append(bwd[seq_len-1][st])
        for emi in range(seq_len-2,-1,-1):
            curr_st = []
            for st in range(self.num_states):
                prev_toSum = []
                for pst in range(self.num_states):
                    prev_toSum.append(prev_st[pst] + math.log(self.transition[st][pst]) + math.log(self.emission[pst][sequence[emi+1]]))
                curr_st.append(self.log_sum(prev_toSum))
            for st in range(self.num_states):
                bwd[emi][st] = curr_st[st]
            prev_st = curr_st

        #combine forward and backward
        fwdbwd = np.zeros((seq_len,self.num_states),dtype=float)
        alpha = 1/self.log_sum(fwd[:][seq_len-1])
        for emi in range(seq_len):
            for st in range(self.num_states):
                fwdbwd[emi][st] = fwd[emi][st] * bwd[emi][st] * alpha

        return fwdbwd
        # End your code
        ###########################################


    # Output the most likely state for each symbol in an emmision sequence
    # - sequence: posterior probabilities received from posterior()
    # return: list of state indices, e.g. [0,0,0,1,1,0,0,...]
    def posterior_decode(self, sequence):
        nSamples  = len(sequence)
        post = self.posterior(sequence)
        best_path = np.zeros(nSamples)
        for t in range(nSamples):
            best_path[t], _ = max(enumerate(post[t]), key=operator.itemgetter(1))
        return list(best_path.astype(int))


def read_sequences(filename):
    inputs = []
    with open(filename, "r") as f:
        for line in f:
            inputs.append(line.strip())
    return inputs

def write_sequence(filename, sequence):
    with open(filename, "w") as f:
        f.write("".join(sequence))

def write_output(filename, viterbi, posterior):
    vit_file_name = filename[:-4]+'_viterbi_output.txt' 
    with open(vit_file_name, "a") as f:
        for state in range(2):
            f.write(str(viterbi.count(state)))
            f.write("\n")
        f.write(" ".join(map(str, viterbi)))
        f.write("\n")

    pos_file_name = filename[:-4]+'_posteri_output.txt' 
    with open(pos_file_name, "a") as f:
        for state in range(2):
            f.write(str(posterior.count(state)))
            f.write("\n")
        f.write(" ".join(map(str, posterior)))
        f.write("\n")


def truncate_files(filename):
    vit_file_name = file[:-4]+'_viterbi_output.txt'
    pos_file_name = file[:-4]+'_posteri_output.txt' 
    if os.path.isfile(vit_file_name):
        open(vit_file_name, 'w')
    if os.path.isfile(pos_file_name):
        open(pos_file_name, 'w')


if __name__ == '__main__':

    hmm = HMM()

    file = sys.argv[1]
    truncate_files(file)
    
    sequences  = read_sequences(file)
    for sequence in sequences:
        viterbi   = hmm.viterbi(sequence)
        posterior = hmm.posterior_decode(sequence)
        write_output(file, viterbi, posterior)


