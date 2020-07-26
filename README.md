## Snakes and ladders

This is a simple program for determining the shortest possible path in a game of 'Snakes and ladders', as well as the average path length when the dierolls are random. Boards are generated randomly based on user specifications. 

The main program is called from the command line, using the following command line arguments:

-s, or --snakes, integer representing the number of snakes
-l, or --ladders, integer representing the number of ladders
-g, or --goal, integer representing the number of the goal field, which is also the length of the entire board

### Input restrictions:

Goal must not be on field 1 (the starting field)
Total number of snakes and ladders must not exceed half the length of the board, as each snake and/or ladder takes up 2 spots on the board. 