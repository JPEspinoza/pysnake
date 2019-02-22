import tkinter
import random

master = tkinter.Tk()

size = 800
divisions = 50
partition = size / divisions #size of squares

#simulation speed
tickTime = 200

#The snake, first item is head, last item is tail
snakeList = []

#Optimization for collision detection
board = []

direction = None
foodRectangle = None

canvas = tkinter.Canvas(master, width=size, height=size)
canvas.pack()

#control events
def left(event):
    global direction
    direction = (-1, 0)

def right(event):
    global direction
    direction = (1, 0)

def up(event):
    global direction
    direction = (0, -1)

def down(event):
    global direction
    direction = (0, 1)

master.bind('<Left>', left)
master.bind('<Right>', right)
master.bind('<Up>', up)
master.bind('<Down>', down)

#game process
def putFood(): #Chooses a random free spot and puts food
    x = random.randint(0, divisions)
    y = random.randint(0, divisions)
    if(board[x][y] != False):
        putFood()
    else:
        global foodRectangle
        canvas.delete(foodRectangle)
        board[x][y] = "food"
        foodRectangle = canvas.create_rectangle(x * partition, y * partition, (x+1)*partition, (y+1)*partition, fill="red")

def createSnake(x,y):
    snakeList.append((x,y))
    board[x][y] = canvas.create_rectangle(x * partition, y * partition, (x+1)*partition, (y+1)*partition, fill="black") #This puts the object into the board, super easy to handle

def delete(x,y):
    canvas.delete(board[x][y])
    board[x][y] = False
    snakeList.pop(0)

def loop():
    if(direction == None):
        pass 
    else:
        #check for collision in direction
        newX = snakeList[-1][0] + direction[0]
        newY = snakeList[-1][1] + direction[1]

        if(board[newX][newY] == "food"): #Food, dont delete and add more food
            board[newX][newY] = False
            putFood()
        elif(board[newX][newY] != False): #Collision
            restart()
        else: #Nothing, delete last piece
            delete(snakeList[0][0], snakeList[0][1])

        #create new piece of snake
        createSnake(snakeList[-1][0] + direction[0], snakeList[-1][1] + direction[1])

    #call itself to set speed
    master.after(tickTime, loop)

def restart():
    direction = None
    board = [[False for _ in range(divisions)] for _ in range(divisions)]
    for piece in snakeList:
        delete(piece[0], piece[1])
    snakeList[:]

    y = int(divisions / 2)
    for x in range(y-1, y+2):
        createSnake(x, y)

    putFood()

#start the game
restart()
loop()

master.mainloop()
