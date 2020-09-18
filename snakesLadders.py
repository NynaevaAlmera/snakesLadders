import random
import math
import argparse
import numpy as np
import pprint

def quickestWayUp(ladders, snakes, goal):
    adj = dict()

    ladderMap = dict()

    for i in range(len(ladders)):
        ladderMap[ladders[i][0]] = ladders[i][1]

    for i in range(len(snakes)):
        ladderMap[snakes[i][0]] = snakes[i][1]

    for i in range(1, goal + 1):
        adj[i] = list()

    for i in range(1, goal - 5):
        for j in range(1, 7):
            if (i+j) in ladderMap:
                adj.get(i).append(ladderMap.get(i+j))
            else:
                adj.get(i).append(i+j)
    for i in range(goal - 5, goal):
        for j in range(i+1, goal + 1):
            if (i+j) in ladderMap:
                adj.get(i).append(ladderMap.get(j))
            else:
                adj.get(i).append(j)

    result = 0

    frontier = list()
    frontier.append(1)
    visited = list()
    visited.append(1)
    while not (goal in frontier):
        result = result + 1
        newFrontier = list()
        for node in frontier:
            for neighbour in adj.get(node):
                if not (neighbour in visited):
                    visited.append(neighbour)
                    newFrontier.append(neighbour)
        if not newFrontier:
            return -1
        frontier = newFrontier.copy()
    return result


def generateSnakesAndLadders(numOfLadders, numOfSnakes, goal):
    ladders = list()
    snakes = list()
    occupiedSet = set()
    if numOfLadders + numOfSnakes >= goal // 2 - 2:
        raise Exception('too many snakes and ladders')
    for i in range(numOfLadders):
        start = random.randint(2,goal-1)
        end = random.randint(3,goal)
        while start in occupiedSet or end in occupiedSet or end <= start:
            start = random.randint(2,goal-1)
            end = random.randint(3,goal)
        newEntry = list()
        newEntry.append(start)
        newEntry.append(end)
        ladders.append(newEntry)

        occupiedSet.add(start)
        occupiedSet.add(end)

    for i in range(numOfSnakes):
        start = random.randint(2,goal-1)
        end = random.randint(1,goal-2)
        while start in occupiedSet or end in occupiedSet or end >= start:
            start = random.randint(2,goal-1)
            end = random.randint(1,goal-2)
        newEntry = list()
        newEntry.append(start)
        newEntry.append(end)
        snakes.append(newEntry)

        occupiedSet.add(start)
        occupiedSet.add(end)
    
    return ladders,snakes

def betterAverageFinder(ladders,snakes,goal):
    if quickestWayUp(ladders, snakes, goal) == -1:
        return -1

    ladderMap = dict()

    for i in range(len(ladders)):
        ladderMap[ladders[i][0]] = ladders[i][1]

    for i in range(len(snakes)):
        ladderMap[snakes[i][0]] = snakes[i][1]
    
    equations = [[0]*(goal) for _ in range(goal)]
    rightHandSide = [0] * (goal)

    for i in range(0, goal):
        #print(i)
        #print(equations[i], '\n')
        equations[i][i] = 1
        #print(equations[i], '\n')

    for i in range(goal - 1, goal - 7, -1):
        if (i) not in ladderMap:
            rightHandSide[i-1] = 6/(goal-i)
            for j in range(i+1, goal):
                equations[i-1][j-1] = -1/(goal-i)
        else:
            equations[i-1][ladderMap[i]-1] = -1
        
    for i in range(goal - 7, 0, -1):
        if (i) not in ladderMap:
            rightHandSide[i-1] = 1
            for j in range(i+1, i+7):
                equations[i-1][j-1] = -1/6
        else:
            equations[i-1][ladderMap[i]-1] = -1


    A = np.array(equations)
    b = np.array(rightHandSide)

    solutions = np.linalg.solve(A, b)
    
    return solutions[0]
    

def luckPath(ladders,snakes,goal):
    if quickestWayUp(ladders, snakes, goal) == -1:
        return -1

    ladderMap = dict()

    for i in range(len(ladders)):
        ladderMap[ladders[i][0]] = ladders[i][1]

    for i in range(len(snakes)):
        ladderMap[snakes[i][0]] = snakes[i][1]
        
    currentField = 1
    numOfSteps = 0
    while currentField != goal:
        #print(numOfSteps,'\n')
        numOfSteps = numOfSteps + 1
        advance = random.randint(1,6)
        if (currentField + advance) <= goal:
            if (currentField + advance) in ladderMap:
                currentField = ladderMap[currentField + advance]
            else:
                currentField = currentField + advance

            
    return numOfSteps

def averageSteps(ladders,snakes,goal,numOfIterations):
    total = 0
    if quickestWayUp(ladders, snakes, goal) == -1:
        return -1
    else:
        for i in range(numOfIterations):
            steps = luckPath(ladders, snakes, goal)
            total = total + steps
            #print(steps, '\n')
        return total/numOfIterations

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--snakes", type=int,
            help="number of snakes, default value 5", default=40)
    ap.add_argument("-l", "--ladders", type=int, default=0,
            help="number of ladders, default value 17")
    ap.add_argument("-g","--goal", type=int, default=100,
            help="goal field, distance from start to goal")
    args = vars(ap.parse_args())


    goal = args["goal"]
    if goal < 2:
        print("goal must be 2 or greater")
        exit()
    ladders, snakes = generateSnakesAndLadders(args["ladders"], args["snakes"], goal)

    while quickestWayUp(ladders, snakes, goal) != -1:
        ladders, snakes = generateSnakesAndLadders(args["ladders"], args["snakes"], goal)
    
    luckyAverage = averageSteps(ladders,snakes,goal,1000000)
    betterAverage = betterAverageFinder(ladders,snakes,goal)
    result = quickestWayUp(ladders, snakes, 100)
    

     
    print('The ladders: \n')
    print(ladders, '\n')
    print('The snakes: \n')
    print(snakes, '\n')
    print('Quickest path to the goal is ' + str(result) + ' steps\n')
    print('Average path to the goal is ' + str(luckyAverage) + ' steps\n')
    print('BETTER average finder says path to the goal is ' + str(betterAverage) + ' steps\n')
    
