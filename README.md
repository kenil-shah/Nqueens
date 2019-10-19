# Nqueens

Determining upto 2*n solutions of NQueens using Forward checking and arc consistency.

![Alt Text](https://github.com/kenil-shah/Nqueens/blob/master/readme-images/Nqueens.gif)

## Installation

1) Clone this repository.
```
git clone https://github.com/kenil-shah/Nqueens.git
```

### Usage
```
python NQueens.py ALG N CFile RFile

ALG : FOR/MAC
N : Board Size
CFile : Generates a text file named CFile.txt which stores representation of the variables, constraints and domains.
RFile : Generates a text file named RFile.txt which stores upto 2*N solutions.
```

### Algorithm
```
1)Initially the board size is passed in the QueenGraph object and using that the domains and variables are initialized, 
which are going to be used in the algorithm. Moreover, the values of variable, domains and constraints are dumped in the CFile.

2)Function queens_arrange present in the QueenGraph class will start placing each queen one after another.The algorithm 
does not use any ordering heuristic and will place the queens one after another in normal order. Thus, Q0 will be placed
first then Q1 and so on.

3)Whenever a queen is  placed the algorithm will iterate through the queens domain and if the MAC/FOR would return True 
for that particular value in the queens domain then a recursive call to the function queens_arrange will be made but this
time the queen_no would be increased by 1 and so it will try placing the second queen and so on. If MAC/FOR returns false then it
will iterate with the next value in the domain of first queen.(This goes on in the recursion)

4)Once every queen is placed then algorithm return False as we want multiple solutions rather than just one. It will return
True value only when the number of solutions are equal to 2*n.

```
