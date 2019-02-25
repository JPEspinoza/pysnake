"""A simple snake game made in python, main objective is simplicity, consistency and performance"""
import tkinter
import random

MASTER = tkinter.Tk()

#constants
SIZE = 900 #size (in pixels?)
DIVISIONS = 60 #number of tiles
PARTITION = SIZE / DIVISIONS #size of squares

TICKTIME = 200 #simulation speed

#classes
class Point:
    """ a simple coordinates class to simplify coord passing"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, i):
        """Point * int/float"""
        x = self.x * i
        y = self.y * i

        return Point(x, y)

    def __str__(self):
        """debugging"""
        return "X: " + str(self.x) + " - Y: " + str(self.y)

    def __eq__(self, other):
        """point == point"""
        if(
                self.x == other.x and
                self.y == other.y):
            return True
        return False

class Board:
    """ Handles drawing and efficient positioning"""
    def __init__(self):
        CANVAS.delete("all")

        #stores canvas element for later deletion
        self.visual = [[None for _ in range(DIVISIONS)] for _ in range(DIVISIONS)]

        #stores color so the program can use it to identify things
        self.info = [["white" for _ in range(DIVISIONS)] for _ in range(DIVISIONS)]

    def __call__(self, pos):
        """to check positions"""
        try:
            return self.info[pos.x][pos.y]
        except AttributeError: #if pos isnt a point, initial state of game
            return None
        except IndexError: #if outside of bounds
            return "black"

    def add(self, pos, color):
        """add and draw item"""
        coords = pos * PARTITION
        self.visual[pos.x][pos.y] = CANVAS.create_rectangle(coords.x, coords.y, coords.x+PARTITION, coords.y+PARTITION, fill=color)
        self.info[pos.x][pos.y] = color

    def remove(self, pos):
        """deletes item in the board (including visual)"""
        CANVAS.delete(self.visual[pos.x][pos.y])
        self.visual[pos.x][pos.y] = None
        self.info[pos.x][pos.y] = "white"

class Snake:
    """keeps track of the snake itself"""
    def __init__(self):
        self.snake_list = [] #array of points
        self.direction = Point(None, None) #store potential movements
        self.last_direction = Point(1, 0) #store direction of last movement

    def set_direction(self, point):
        inverse_direction = self.last_direction * -1
        if point != inverse_direction:
            self.direction = point

    def next(self):
        """return next position and removes"""
        try:
            next_x = self.snake_list[-1].x + self.direction.x
            next_y = self.snake_list[-1].y + self.direction.y

            return Point(next_x, next_y)

        except TypeError:
            return None

    def add(self, pos):
        """add piece of snake at the end of the list"""
        self.snake_list.append(pos)

    def remove(self, i=0):
        """remove last piece of snakelist"""
        return self.snake_list.pop(i)

#control events
def left(__):
    """left"""
    SNAKE.set_direction(Point(-1, 0))

def right(__):
    """right"""
    SNAKE.set_direction(Point(1, 0))

def up(__):
    """up"""
    SNAKE.set_direction(Point(0, -1))

def down(__):
    """down"""
    SNAKE.set_direction(Point(0, 1))

#control functions
def add_food():
    """delete old piece of food and put new one"""
    new_x = random.randint(1, DIVISIONS - 1)
    new_y = random.randint(1, DIVISIONS - 1)

    point = Point(new_x, new_y)

    if BOARD(point) == "white": #if empty
        global FOOD #use global food item
        BOARD.remove(FOOD) #delete old food
        BOARD.add(point, "red") #add new food
        FOOD = point #store new food

    else:
        add_food()

def add_snake(pos):
    """add piece of snake directly"""
    SNAKE.add(pos)
    BOARD.add(pos, "black")

def remove_snake():
    """remove last piece of the snake"""
    BOARD.remove(SNAKE.remove())

def reset_game():
    """reset all objects"""
    #restart each object
    BOARD.__init__()
    SNAKE.__init__()

    #restart food item
    global FOOD
    FOOD = Point(0, 0)

    #add new snake
    row = int(DIVISIONS / 2)
    for column in range(row - 1, row + 2):
        add_snake(Point(column, row))

    #add new food
    add_food()

def loop():
    """main loop"""
    next_pos = SNAKE.next()
    next_item = BOARD(next_pos)

    if next_item == "white":
        add_snake(next_pos)
        remove_snake()
        SNAKE.last_direction = SNAKE.direction

    elif next_item == "red":
        add_food()
        add_snake(next_pos)
        SNAKE.last_direction = SNAKE.direction

    elif next_item == "black":
        reset_game()

    MASTER.after(TICKTIME, loop) #call itself to set speed

#setup window
CANVAS = tkinter.Canvas(MASTER, width=SIZE, height=SIZE)
CANVAS.pack()

#setup objects
BOARD = Board()
SNAKE = Snake()
FOOD = Point(0, 0) #keep the position of the old food

#setup keys
MASTER.bind('<Left>', left)
MASTER.bind('<Right>', right)
MASTER.bind('<Up>', up)
MASTER.bind('<Down>', down)

#start the game
reset_game()
loop()
MASTER.mainloop()
