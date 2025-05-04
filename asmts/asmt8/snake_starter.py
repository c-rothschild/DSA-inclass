import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import numpy as np

import networkx as nx

import sys

from heapq import *
import heapq

from matplotlib import pyplot as plt
pygame.init()

if len(sys.argv) <= 1:
    num_obstacles = 0
    mode = 'human'
else:
    mode = sys.argv[1]
    num_obstacles = sys.argv[2]
    

# Defining the colors that the snake and food will use.  
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
 
# Width of the game board (in tiles). 
WIDTH  = 20
# Height of the game board (in tiles).
HEIGHT = 20

# Size of each tile (in pixels).
STEPSIZE = 20

# How fast the game runs. Higher values are faster. 
CLOCK_SPEED = 10
 
# Making a pygame display. 
dis = pygame.display.set_mode((WIDTH*STEPSIZE,HEIGHT*STEPSIZE))
pygame.display.set_caption('Snake!')

# Initial variables to store the starting x and y position,
# and whether the game has ended. 
game_over = False 
x1 = 5
y1 = 5
snake_list = [(x1,y1)]
snake_len = 1 
x1_change = old_x1_change = 0       
y1_change = old_y1_change = 0

# PyGame clock object.  
clock = pygame.time.Clock()

food_eaten = True

# Random obstacles, if desired. 
obstacles = [(np.random.randint(low=0, high=WIDTH),np.random.randint(low=0, high=HEIGHT)) for i in range(int(num_obstacles))]




# This method is a wrapper for the various AI methods. 
# right now it just moves the snake randomly regardless
# of the board state, because none of those methods are 
# filled in yet. 
# Bstate is a matrix representing the game board:
### Array cells with a 0 are empty locations. 
### Array cells with a -1 are the body of the snake.
### The cell marked with a -2 is the head of the snake.
### The cell marked with a 1 is the food.
def get_AI_moves(ai_mode, bstate):
    if ai_mode == 'rand':
        return random_AI(bstate)
    elif ai_mode == 'greedy':
        return greedy_AI(bstate)
    elif ai_mode == 'astar':
        return astar_AI(bstate)  
    elif ai_mode == 'dijkstra':
        return dijkstra_AI(bstate)  
    elif ai_mode == 'backt':
        return backt_AI(bstate)   
    else:
        raise NotImplementedError("Not a valid AI mode!\nValid modes are rand, greedy, astar, dijkstra, and backt.")    


# These are the methods you will fill in. 
# Each method takes in a game board (as described above), and
# should output a series of moves. Valid moves are: 
# (0,1),(0,-1),(1,0), and (-1,0). This means if you want to
# move in any more complicated way, you need to convert the move
# you want to make into a sequence like this one.
# For example, if I wanted my snake to move +5 in the x direction and +3
# in the y direction, I could return 
# [(0,1),(0,1),(0,1),(0,1),(0,1),(1,0),(1,0),(1,0)].

# Several of these methods demonstrate how to get the source
# and target locations, but currently do not use this information. 

def dist2target(source, target):
    x_steps = np.abs(target[0] - source[0])
    y_steps = np.abs(target[1] - source[1])

    if x_steps > 10:
        x_steps = 20 - x_steps
    
    if y_steps > 10:
        y_steps = 20 - y_steps
    
    return x_steps + y_steps


def getPath2Node(G, target):
    
    path = [target]
    curParent = G.nodes[target]['parent']
    while curParent != None:
        path.append(curParent)
        curParent = G.nodes[curParent]['parent']
    return path[::-1]

def astar_AI(bstate):
    
    source = np.array(np.where(bstate == -2))
    target = np.array(np.where(bstate == 1))
    sourceTup = (int(source[0,0]), int(source[1,0]))
    targetTup = (int(target[0,0]), int(target[1,0]))
    G = boardGraph()
    nx.set_node_attributes(G, np.inf, 'cost')
    nx.set_node_attributes(G, np.inf, 'distFrStart')
    nx.set_node_attributes(G, None, 'parent')

    G.nodes[sourceTup]['cost'] = dist2target(sourceTup, targetTup)
    G.nodes[sourceTup]['distFrStart'] = 0


    # let the openList equal empty priority Q of nodes (lower cost = higher priority)
    openList = []
    heapq.heapify(openList)
    # let the closedList equal empty collection of nodes (probably a dictionary for fastness)
    closedList = {}
    # put the startNode on the openList and the closedList (we didn’t start at the goal!)
    heapq.heappush(openList, (G.nodes[sourceTup]['cost'], sourceTup))
    closedList[sourceTup] = G.nodes[sourceTup]['cost']
    path = []
    # while the openList is not empty
    while len(openList) != 0:
        # Pop from the openlist and call that currentNode
        curNode = heapq.heappop(openList)[1]
            
        # if currentNode is the goal
        if curNode == targetTup:
            # Backtrack to get path and return (you remembered every node’s parent, right?!)
            path.extend(getPath2Node(G, targetTup))
            break
        # otherwise:
        # for each non-obstacle neighbor of currentNode:
        curNodeDist = G.nodes[curNode]['distFrStart']
        for neighbor in G.neighbors(curNode):
            # neighbor.cost = steps to get to currentNode + 1 + estimated distance from neighbor to goal
            tempNeighborCost = curNodeDist + 1 + dist2target(neighbor, targetTup)


            # if neighbor not in closedList or closedList[neighbor].cost > neighbor.cost
            if neighbor not in closedList or G.nodes[neighbor]['cost'] > tempNeighborCost:

                G.nodes[neighbor]['parent'] = curNode
                G.nodes[neighbor]['cost'] = tempNeighborCost
                G.nodes[neighbor]['distFrStart'] = curNodeDist + 1
                # Add neighbor and its cost to closedList
                closedList[neighbor] = 'balls'
                
                # Enqueue neighbor to openList
                heapq.heappush(openList, (tempNeighborCost, neighbor))
    


    path_list.clear()
    # print(sourceTup)
    # print(targetTup)
    
    path_list.extend(path[1:])
    if len(path_list) == 0:
        return random_dense_AI(bstate)
    


    return [((path[1][0] - sourceTup[0]),(path[1][1] - sourceTup[1]))]

def random_dense_AI(bstate):
    source = np.array(np.where(bstate == -2))
    sourceTup = (int(source[0,0]), int(source[1,0]))
    G = boardGraph()
    move = random_AI(bstate)
    for neighbor in G.neighbors(sourceTup):
        move = [((neighbor[0] - sourceTup[0]),(neighbor[1] - sourceTup[1]))]
        if len(list(G.neighbors(neighbor))) < 4:
            return move
    return move



    
def backt_AI(bstate):
    source = np.array(np.where(bstate == -2))
    target = np.array(np.where(bstate == 1))
    return random_AI(bstate)


#list of tuples in path to apple
path_list = []

def dijkstra_AI(bstate):
    source = np.array(np.where(bstate == -2))
    target = np.array(np.where(bstate == 1))
    sourceTup = (source[0,0],source[1,0])
    targetTup = (target[0,0], target[1,0])
    G = boardGraph()
    try:
        path = nx.dijkstra_path(G, sourceTup, targetTup)
    except:
        path_list.clear()
        return random_dense_AI(bstate)
    path_list.clear()
    path_list.extend(path[1:])
    return [((path[1][0] - sourceTup[0]),(path[1][1] - sourceTup[1]))]





def steps2zero(num, source):
    if num > 10:
        num -= 20
    elif num < -10:
        num += 20

    if num == 0:
        return []
    
    return list(reversed([(source + i) % 20 for i in range(num, 0, int(np.abs(num)/num * -1))]))

            
def greedy_AI(bstate):
    source = np.array(np.where(bstate == -2))
    target = np.array(np.where(bstate == 1))
    sourceTup = (source[0,0],source[1,0])
    targetTup = (target[0,0], target[1,0])
    G = boardGraph()
    path = [sourceTup]
    x_change = targetTup[0] - sourceTup[0]
    y_change = targetTup[1] - sourceTup[1]
    
    x_steps = steps2zero(x_change, sourceTup[0])
    path.extend(list(zip(x_steps, [int(source[1])] * len(x_steps))))



    y_steps = steps2zero(y_change, sourceTup[1])
    path.extend(list(zip([int(target[0])] * len(y_steps), y_steps)))
    path.append(targetTup)
    path_list.clear()
    path_list.extend(path[2:])

    return [((path[1][0] - sourceTup[0]),(path[1][1] - sourceTup[1]))]

    
def random_AI(bstate):
    return [[(0,1),(0,-1),(1,0),(-1,0)][np.random.randint(low=0,high=4)]]
    

AI_moves = []

# Don't modify any code below this point!
# This code is not meant to be readable or understandable to you - it's the game
# engine and the particulars of moving the snake according to your AI.
# The particulars of the code below shouldn't matter to your AI code above.
# If you have questions, or if your AI code needs to be able to use any of the below,
# talk to Blake.  


def show_grid(graph):
    plt.figure(figsize=(6,6))
    pos = {(x,y):(y,-x) for x,y in graph.nodes()}
    nx.draw(graph, pos=pos, 
            node_color='lightgreen', 
            with_labels=True,
            node_size=600)
    plt.show()

def generateEmptyBoard(remove_obstacles=True):
    G = nx.grid_graph(dim=(WIDTH, HEIGHT))

    #creating top to bottom edges
    for i in range(WIDTH):
        G.add_edge((0, i),(WIDTH-1, i))


    #creating left to right edges
    for i in range(HEIGHT):
        G.add_edge((i, HEIGHT - 1),(i, 0))

    if remove_obstacles:
        G.remove_nodes_from(obstacles)
    
    return G



gameBoard = generateEmptyBoard()

def boardGraph():
    G = gameBoard.copy()
    G.remove_nodes_from(snake_list[:-1])
    return G







while not game_over:
    


    if food_eaten:   
        fx = np.random.randint(low=0,high=WIDTH)
        fy = np.random.randint(low=0,high=HEIGHT)
        while (fx,fy) in snake_list or (fx,fy) in obstacles:
            fx = np.random.randint(low=0,high=WIDTH)
            fy = np.random.randint(low=0,high=HEIGHT)
        food_eaten = False
        
    dis.fill(white)
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if mode == 'human':    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -1
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = 1
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -1
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = 1
                    x1_change = 0
    if mode != 'human':
        if len(AI_moves) == 0:
            bstate = np.zeros((WIDTH,HEIGHT))
            for xx,yy in snake_list:
                bstate[xx,yy] = -1
            for xx,yy in obstacles:
                bstate[xx,yy] = -1
            bstate[snake_list[-1][0], snake_list[-1][1]] = -2
            bstate[fx,fy] = 1    
            AI_moves = get_AI_moves(mode, bstate)     
        x1_change, y1_change = AI_moves.pop(0) 

    if not snake_list:
        print("You lose! Score: %d" % snake_len)
        break

    if len(snake_list) > 1 :
        if ((snake_list[-1][0] + x1_change) % WIDTH) == snake_list[-2][0] and ((snake_list[-1][1] + y1_change)% HEIGHT) == snake_list[-2][1]:
            x1_change = old_x1_change
            y1_change = old_y1_change
    x1 += x1_change
    y1 += y1_change          
    
    x1 = x1 % WIDTH
    y1 = y1 % HEIGHT
    
    if x1 == fx and y1 == fy:
        snake_len += 1
        food_eaten = True
    
    snake_list.append((x1,y1))
    snake_list = snake_list[-snake_len:]
    
    if len(list(set(snake_list))) < len(snake_list) or len(set(snake_list).intersection(set(obstacles))) > 0:
        print("You lose! Score: %d" % snake_len)
        game_over = True
    else:


        #drawing path
        for xx, yy in path_list:
            pygame.draw.rect(dis, (128, 0, 0), [xx*STEPSIZE, yy*STEPSIZE, STEPSIZE, STEPSIZE])

        sncols = np.linspace(.5,1.0, len(snake_list))
        for jj, (xx, yy) in enumerate(snake_list):
            pygame.draw.rect(dis, (0, 255*sncols[jj], 32*sncols[jj]), [xx*STEPSIZE, yy*STEPSIZE, STEPSIZE, STEPSIZE])
            
        
        
        for (xx, yy) in np.cumsum(np.array([[.5,.5],snake_list[-1]] + AI_moves), axis=0)[2:]:
            pygame.draw.circle(dis, red, (xx*STEPSIZE,yy*STEPSIZE), STEPSIZE/4)            
        
        if not food_eaten:
            pygame.draw.rect(dis, red, [fx*STEPSIZE, fy*STEPSIZE, STEPSIZE, STEPSIZE])
        
        for xx, yy in obstacles:
            pygame.draw.rect(dis, blue, [xx*STEPSIZE, yy*STEPSIZE, STEPSIZE, STEPSIZE])
        pygame.display.update()
     
        clock.tick(CLOCK_SPEED)
        
        old_x1_change = x1_change
        old_y1_change = y1_change
 
pygame.quit()
quit()
