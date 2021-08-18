# DjangoSudoku
Sudoku Solver Web App in Django.

The solver uses solution space reduction on the input after filling all the empty cells with all possible values.
After the reduction, depth-first search is used recursively for backtracking using constraint satisfaction.
The solution is coded in "vanilla" Python without using any library.

Run the web server with: $cd Sudoku; python manage.py runserver.

## Home
![image info](./img/home.PNG)

## Solve
![image info](./img/solve.PNG)

## Scores
Scores are saved in the database and can be updated/deleted/created.

![image info](./img/scores.PNG)