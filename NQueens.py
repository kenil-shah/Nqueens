import copy
import time
import sys

backtracking_steps = 0
count = 0

'''
Command Line Arguments
'''
method_used = sys.argv[1]
Nqueens = int(sys.argv[2])
cfile = sys.argv[3]
rfile = sys.argv[4]


class QueenGraph:
    r_file = open(rfile+".txt", "w+")
    c_file = open(cfile+".txt", "w+")

    def __init__(self):
        """
        def __init__(self, n_queens)
        This is the init function and will run whenever an Object is created for Class QueenGraph.
        FUNCTIONS:
            Stores the values of domain, variables and constraints which are used in the entire code
        RETURNS:
            None
        """
        self.variables = []
        self.domains = []
        self.constraints = {}

    def initialize_domain_variables(self, n_queens):
        count = 0
        while count < n_queens:
            self.variables.append("Q_" + str(count))
            self.domains.append([])
            count1 = 0
            while count1 < n_queens:
                self.domains[count].append(count1)
                count1 += 1
            count += 1

    def write_values_to_cfile(self, variables, domains):
        """
        def write_values_to_cfile(self, variables, domains)
        This function is called only once at the beginning of the code.
        INPUT:
            variables :- The queen ID's are used are variables
            domains :- Possible locations where a queen can be safely placed.(Possible values :- 0 to n-1)
        FUNCTIONS:
            1]Dumps the variables, domains and constraints in the CFile.txt
            2]Constraints of QueenGraph are updated here
        RETURNS:
            None
        """
        self.c_file.write("Variables\n")
        self.c_file.write(str(variables)+"\n"+"\n")
        self.c_file.write("Domains")
        for a in variables:
            self.c_file.write("\n")
            self.c_file.write(a + " --- " + str(domains[0]))
        self.c_file.write("\n"+"\n")
        self.c_file.write("Constraints\n")
        total_queens = len(variables)
        for i in range(total_queens):
            for j in range(i+1, total_queens):
                self.constraints[str(i)+"_"+str(j)] = ([0, j-i, -(j-i)])
                self.c_file.write("V("+variables[i]+") - V("+variables[j]+") != 0,"+str(j-i)+"," + str(-(j-i))+"\n")

    def write_soln_to_rfile(self, solution):
        """
        def write_soln_to_rfile(self, solution)
        This function is called whenever the number of queens placed is equal to total number of queens.
        INPUT:
            solution :- The location where every queen is placed.
                For instance if N=4, one of the solution would be {1,3,0,2}
        FUNCTIONS:
            1]Dumps the solution into RFile.txt with the following human readable format,
                For solution = {1,3,0,2}
                0 1 0 0
                0 0 0 1
                1 0 0 0
                0 0 1 0
        Returns :- None
        """
        for x in solution:
            c = 0
            while c < len(solution):
                if c == x[0]:
                    self.r_file.write(str(1) + " ")
                else:
                    self.r_file.write(str(0) + " ")
                c += 1
            self.r_file.write("\n")
        self.r_file.write("-----------------")
        self.r_file.write("\n")

    def forward_check(self, q_position, queen_no, domains, total_queens, constraints):
        """
        def forward_check(self, q_position, queen_no, domains, total_queens):
        This function is called whenever a queen is placed in order to check whether the queen that has been placed
        would lead to an empty domain for any other queen.(If domain for any queen is empty solution cannot be found).
        No ordering heuristic is used and the queens would be placed starting from first to the last.
        INPUT:
            q_position :- The position at which the current queen has been placed.                          [Integer]
            queen_no :- The queen which has been placed.                                                    [Integer]
            domains :- Current values present in the domain of every queen                                  [2D List]
            total_queens:- The total number of queens that we supposed to place.                            [Integer]
            constraints:-Instance variable of an object of QueenGraph containing constraints of queen pairs.[Dictionary]
        FUNCTIONS:
            Discards the values in a domains after checking those values with the constraints of that specific queen
            pair.
        RETURNS:
            True/False:- The function returns True value when the domain of every queen is non-empty and returns False
            when the the domain of any queen is empty.
        """
        for q in range(queen_no+1, total_queens):
            # Use self.constraints to check the domain values which are not possible
            constraint_check = constraints[str(queen_no)+"_"+str(q)]
            constraint_check = [x + q_position for x in constraint_check]
            domains[q] = [elem for elem in domains[q] if elem not in constraint_check]
        for check in domains:
            if len(check) == 0:
                return False
        return True

    def arc_consistency(self, domains, total_queens, constraints):
        """
        def arc_consistency(self, domains, total_queens):
         This function is called whenever a queen is placed in order to check the consistency of the domain for each
         queen. No ordering heuristic is used and the queens would be placed starting from first to the last.
         In this implementation we will start checking arc consistency from the domains of first queen. The next loop
         would be used in order to evaluate whether the x value of the domain of queen 1 has a consistent value with the
         domain of every other queen. We will discard the value from the domain of Queen1 whenever a value is found that
         reduces the domain of any other queen to zero. After that a recursive call is used that would check the arc
         consistency from iteration 0. The function will return false when we cannot find a consistent arc.
        INPUT:
            domains :- Current values present in the domain of every queen                                  [2D List]
            total_queens:- The total number of queens that we supposed to place.                            [Integer]
            constraints:-Instance variable of an object of QueenGraph containing constraints of queen pairs.[Dictionary]
        FUNCTIONS:
            If an arc is found inconsistent then that value in the domain is discarded in order to make it consistent.
        RETURNS:
            True/False:- The function returns True value when the domain of every queen is non-empty and returns False
            when the the domain of any queen is empty.
        """
        for q1 in range(total_queens):
            for q_position in domains[q1]:
                domains2 = copy.deepcopy(domains)
                for q2 in range(total_queens):
                    queen1 = q1
                    queen2 = q2
                    if q1 == q2:
                        continue
                    if q1 > q2:
                        queen1, queen2 = q2, q1
                    # Use constraints to check the domain values which are not possible
                    constraint_check = constraints[str(queen1) + "_" + str(queen2)]
                    constraint_check = [x + q_position for x in constraint_check]
                    domains2[q2] = [val for val in domains2[q2] if val not in constraint_check]
                    if len(domains2[q2]) == 0:
                        domains[q1].remove(q_position)
                        if self.arc_consistency(domains, total_queens, constraints):
                            return True
                    if len(domains[q1]) == 0:
                        return False
        return True

    def queens_arrange(self, queen_no, total_queens, domains, constraints):
        """
        def queens_arrange(self, queen_no, total_queens, domains):
            This is the main function that uses recursion in order to find every possible solutions for a given board
            size. Arc consistency/ Forward checking is performed in this function
        INPUT:
            queen_no :- The queen which has been placed.                                                    [Integer]
            domains :- Instance variable of an object of QueenGraph containing domain of every queen.       [2D List]
            total_queens:- The total number of queens that we supposed to place.                            [Integer]
            constraints:-Instance variable of an object of QueenGraph containing constraints of queen pairs.[Dictionary]
        FUNCTIONS:
            It dumps up to 2n solutions in the RFile.txt
        RETURNS:
            True/False:- The function returns True value when a queen is placed or upto 2n solutions have been found.
            It returns false value when a queen cannot be placed or every queen has been placed.(We return false after
            placing every queen as we want to find all possible solutions and not a single solution)
        """
        global backtracking_steps
        global count
        if queen_no >= total_queens:
            count += 1
            self.r_file.write("Solution Number :-"+str(count))
            self.r_file.write("\n")
            self.write_soln_to_rfile(domains)
            if count == 2*total_queens:
                print("Total Solutions found:-", count)
                return True
            return False
        for i in domains[queen_no]:
            q_position = i
            domains2 = copy.deepcopy(domains)
            domains[queen_no] = []
            domains[queen_no].append(q_position)
            if method_used == "MAC":
                if self.arc_consistency(domains, total_queens, constraints):
                    ''' 
                    The domains passed in recursion will be the domains that are reduced by arc_consistency function
                    as the domains variable is an instance of the object QueenGraph.
                    '''
                    if self.queens_arrange(queen_no + 1, total_queens, domains, constraints):
                        return True
            elif method_used == "FOR":
                if self.forward_check(q_position, queen_no, domains, total_queens, constraints):
                    ''' 
                    The domains passed in recursion will be the domains that are reduced by forward_check function
                    as the domains variable is an instance of the object QueenGraph.
                    '''
                    if self.queens_arrange(queen_no+1, total_queens, domains, constraints):
                        return True
            else:
                print("Please enter Valid Input")
                return True
            domains = domains2
            backtracking_steps = backtracking_steps + 1
        return False


start = time.time()
Q = QueenGraph()
Q.initialize_domain_variables(Nqueens)
Q.write_values_to_cfile(Q.variables, Q.domains)
Q.queens_arrange(0, Nqueens, Q.domains, Q.constraints)
end = time.time()
print("Total time elapsed", end-start)
print("Number of backtracking steps are :-", backtracking_steps)
print("2N Solutions are stored in RFile ")