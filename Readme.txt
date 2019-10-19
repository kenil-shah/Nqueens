Run the code using:- python NQueens.py FOR/MAC N CFile RFile

The variables selected for solving NQueens problem are the Queen number starting from 0 to n-1 where n is the number of Queens that are
supposed to be placed.
	eg, For N = 5 the variables would be {Q0,Q1,Q2,Q3,Q4}

The domains will be the positions in the horizontal axis of the board where a queen can be placed. Thus, the domain of every queen will be
in the range of 0 to n-1.
	eg, For N = 5 the domains for Q0 would be {0,1,2,3,4}

Constraints are displayed in the CFile.txt

The algorithm runs in the following manner:-
1]Initially the board size is passed in the QueenGraph object and using that the domains and variables are initialized, which are going to be used in the algorithm. Moreover, the values of
variable, domains and constraints are dumped in the CFile.
2]Function queens_arrange present in the QueenGraph class will start placing each queen one after another.The algorithm does not use any ordering heuristic and will place the queens one 
after another in normal order. Thus, Q0 will be placed first then Q1 and so on.
3]Whenever a queen is  placed the algorithm will iterate through the queens domain and if the MAC/FOR would return True for that particular value in the queens domain then a recursive
call to the function queens_arrange will be made but this time the queen_no would be increased by 1 and so it will try placing the second queen and so on. If MAC/FOR returns false then it
will iterate with the next value in the domain of first queen.(This goes on in the recursion)
4]Once every queen is placed then algorithm return False as we want multiple solutions rather than just one. It will return True value only when the number of solutions are equal to 2*n.

Forward Error Checking:-Forward error checking has been implemented by iterating through the domains of every queen. Suppose first queen is placed at position 0 and so the domain of first
queen will be reduced to 0 as we have assigned the value to it. The remaining queen q1,q2 qnd q3 will have [[0,1,2,3],[0,1,2,3],[0,1,2,3]] domains. After running the forward checking
algorithm the the domain values of other queens that are not consistent(Checked by using constraints from queen graph) with respect to first queen would be discarded. Thus, the domains of 
other queens would be reduced to [[2,3],[1,3],[1,2]]. The function will return true when the domains of other queen have atleast one possible value and will return false if the domain of 
any queen is empty(i.e. placement is not feasible). If a true value is returned then it will try placing queen 1 (queen 0 has been placed and so going in order)	

Maintaining arc consistency:- Maintaining arc consistency is a method using which we can reduce the domain values more quickly which would thus lead to a less number of backtracking steps.
When we place the first queen we will check the consistency of the domains of one queen with every other queen and remove the domain values which leads to an empty domain of other queen.
This algorithm has been implemented using three nested for loop in order to compare the domains of every pair of queens available.