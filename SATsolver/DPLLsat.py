#!/usr/bin/python3
# CMPT310 A2
#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
"""
num_hours_i_spent_on_this_assignment = 25
"""
#
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
"""
course going great so far. No complaints or suggestions!


"""
#####################################################
#####################################################
import sys, getopt
import copy
import random
import time
import numpy as np
sys.setrecursionlimit(10000)

class SatInstance:
    def __init__(self):
        pass

    def from_file(self, inputfile):
        self.clauses = list()
        self.VARS = set()
        self.p = 0
        self.cnf = 0
        with open(inputfile, "r") as input_file:
            self.clauses.append(list())
            maxvar = 0
            for line in input_file:
                tokens = line.split()
                if len(tokens) != 0 and tokens[0] not in ("p", "c"):
                    for tok in tokens:
                        lit = int(tok)
                        maxvar = max(maxvar, abs(lit))
                        if lit == 0:
                            self.clauses.append(list())
                        else:
                            self.clauses[-1].append(lit)
                if tokens[0] == "p":
                    self.p = int(tokens[2])
                    self.cnf = int(tokens[3])
            assert len(self.clauses[-1]) == 0
            self.clauses.pop()
            if (maxvar > self.p):
                print("Non-standard CNF encoding!")
                sys.exit(5)
        # Variables are numbered from 1 to p
        for i in range(1, self.p + 1):
            self.VARS.add(i)

    def __str__(self):
        s = ""
        for clause in self.clauses:
            s += str(clause)
            s += "\n"
        return s


def main(argv):
    inputfile = ''
    verbosity = False
    inputflag = False
    try:
        opts, args = getopt.getopt(argv, "hi:v", ["ifile="])
    except getopt.GetoptError:
        print('DPLLsat.py -i <inputCNFfile> [-v] ')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('DPLLsat.py -i <inputCNFfile> [-v]')
            sys.exit()
        ##-v sets the verbosity of informational output
        ## (set to true for output veriable assignments, defaults to false)
        elif opt == '-v':
            verbosity = True
        elif opt in ("-i", "--ifile"):
            inputfile = arg
            inputflag = True
    if inputflag:
        instance = SatInstance()
        instance.from_file(inputfile)
        #start_time = time.time()
        solve_dpll(instance, verbosity)
        #print("--- %s seconds ---" % (time.time() - start_time))

    else:
        print("You must have an input file!")
        print('DPLLsat.py -i <inputCNFfile> [-v]')


# Finds a satisfying assignment to a SAT instance,
# using the DPLL algorithm.
# Input: a SAT instance and verbosity flag
# Output: print "UNSAT" or
#    "SAT"
#    list of true literals (if verbosity == True)
#
#  You will need to define your own
#  DPLLsat(), DPLL(), pure-elim(), propagate-units(), and
#  any other auxiliary functions
def solve_dpll(instance, verbosity):
    # print(instance)
    # instance.VARS goes 1 to N in a dict
    # print(instance.VARS)
    # print(verbosity)
    ###########################################
    # Start your code
    ###########################################
    #instance: either .clauses or .VARS
    #verbosity either True or False (default)

    def DPLL(dpll_clauses,dpll_var,dpll_assignment,dpll_varMap):
        flag = try_assignment(dpll_clauses,dpll_assignment,dpll_varMap)
        ret = []
        if flag == 1:
            #assignment returns all true clauses
            return dpll_assignment
        elif flag == 0:
            #assignment does not create false clause
            find_pure(dpll_clauses,dpll_var,dpll_assignment,dpll_varMap)
            unit_prop(dpll_clauses,dpll_assignment,dpll_varMap)
            #choose new variable
            new_var = new_variable(dpll_assignment,dpll_varMap)
            #true branch
            if new_var != 0:
                variable_map = copy.deepcopy(dpll_varMap)
                ret = DPLL(dpll_clauses,dpll_var,dpll_assignment + [new_var],variable_map)
                if len(ret) == 0:
                    #true branch caused clause to fail, try false variable
                    variable_map = copy.deepcopy(dpll_varMap)
                    ret = DPLL(dpll_clauses,dpll_var,dpll_assignment + [-new_var],variable_map)
            else:
                variable_map = copy.deepcopy(dpll_varMap)
                ret = DPLL(dpll_clauses,dpll_var,dpll_assignment,variable_map)
        #return empty list on failure, otherwise we return assignment
        return ret

    def remove_false(dpll_assignment):
        assignment = []
        for val in dpll_assignment:
            if val > 0:
                assignment.append(val)
        return assignment

    def abs_val(val):
        if val < 0:
            val = -val
        return val

    def in_assignment(dpll_assignment,var):
        ret = False
        if var in dpll_assignment or -var in dpll_assignment:
            ret = True
        return ret
    
    def new_variable(dpll_assignment,dpll_varMap):
        #return variable that occurs the most
        max_var = 0
        max_varCount = 0
        for var in range(1,len(dpll_varMap),1):
            if not in_assignment(dpll_assignment,var):
                count = len(dpll_varMap[var])
                if count > max_varCount:
                    max_varCount = count
                    max_var = var
        return max_var

    def try_assignment(dpll_clauses,dpll_assignment,dpll_varMap):
        #test if assignment works, flag == 1 if all clauses true, flag == 0 for any number of clauses remaining, flag == -1 if a clause is violated
        flag = 0
        num_clauses = len(dpll_clauses)
        for assigned in dpll_assignment:
            varMap_index = abs_val(assigned)
            for clause_index in dpll_varMap[varMap_index]:
                clause = dpll_clauses[clause_index]
                if (dpll_varMap[0][clause_index] != 1):
                    #if clause is not already fulfilled
                    if (assigned in clause):
                        #symbol found in clause, mark clause fulfilled
                        dpll_varMap[0][clause_index] = 1
                        dpll_varMap[0][num_clauses] += 1
                    else:
                        #-symbol found in clause, count down to clause failure
                        dpll_varMap[0][clause_index] -= 1
                        if dpll_varMap[0][clause_index] == -len(dpll_clauses[clause_index]):
                            #if all literals in clause are false, exit dpll
                            flag = -1
                            return flag
            dpll_varMap[varMap_index].clear()
        if dpll_varMap[0][num_clauses] == num_clauses:
            flag = 1
        return flag
    
    def unit_prop(dpll_clauses,dpll_assignment,dpll_varMap):
        #adds literal to assignment and calls try assignment again
        assignment = []
        for clause_index in range(len(dpll_varMap[0])-1):
            clauseLive_target = len(dpll_clauses[clause_index]) - 1
            if dpll_varMap[0][clause_index] == -clauseLive_target:
                #only 1 literal remaining
                for literal in dpll_clauses[clause_index]:
                    if not in_assignment(dpll_assignment,literal):
                        dpll_assignment.append(literal)
                        assignment.append(literal)
                        break
        return assignment

    def find_pure(dpll_clauses,dpll_var,dpll_assignment,dpll_varMap):
        #look for variables that appear only in one sign throughout clauses
        assignment = []
        for var in range(1,len(dpll_var)+1,1):
            pos_count = 0
            neg_count = 0
            if not in_assignment(dpll_assignment,var):
                #consider variables not yet assigned only
                for clause_index in dpll_varMap[var]:
                    clause = dpll_clauses[clause_index]
                    if var in clause:
                        pos_count += 1
                    elif -var in clause:
                        neg_count += 1
                if pos_count == len(dpll_varMap[var]):
                    #variable all true value found
                    dpll_assignment.append(var)
                    assignment.append(var)
                if neg_count == len(dpll_varMap[var]):
                    #variable all false value found
                    dpll_assignment.append(-var)
                    assignment.append(-var)
        return assignment

    #clauses: list of lists class, variables: set class
    clauses = instance.clauses
    variables = instance.VARS
    #populate clause bitmap, indicates which clause (by indices) are still live. 0 = live, 1 = fulfilled, -x = x variables are assigned false
    #clauseLive_map[len(clauses)] = # fulfilled clauses count
    clauseLive_map = []
    for index in range(len(clauses)+1):
        clauseLive_map.append(0)
    #populate variable_map, variable_map[index] are the clause indices where variable(index) may be found. variable_map[0] = clauseLive_map
    variable_map = [clauseLive_map]
    for var in variables:
        variable_map.append([])
    clause_index = 0
    for clause in clauses:
        for literal in clause:
            variable_map[abs_val(literal)].append(clause_index)
            #print(variable_map[clause_index])
        clause_index += 1
    ret = remove_false(DPLL(clauses,variables,[],variable_map))
    if len(ret) > 0:
        #assignment found
        print("SAT")
        if verbosity:
            print(ret)
    else:
        #ret is empty, all assignments failed to find a SAT assignment
        print("UNSAT")

    ###########################################


if __name__ == "__main__":
    main(sys.argv[1:])
