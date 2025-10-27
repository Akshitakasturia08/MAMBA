
# MAMBA
# total pixels = 625px*625px , total rows/ columns = 25tiles , each tile = 25px*25px

import tkinter 
import random

ROWS = 25
COLUMNS = 25
TILE_SIZE = 30

WINDOW_WIDTH = TILE_SIZE * ROWS
WINDOW_HEIGHT = TILE_SIZE * COLUMNS

class Tile:
    def __init__(self, x,y):
        self.x = x
        self.y = y


#Game Window

window = tkinter.Tk()
window.title("MAMBA")
window.resizable(False, False)


canvas = tkinter.Canvas(window , bg="black" , height=WINDOW_HEIGHT , width=WINDOW_WIDTH , borderwidth=0 , highlightthickness=0 )
canvas.pack()
window.update()

#initialize game 
snake = Tile(5*TILE_SIZE,5*TILE_SIZE) #snake head
food = Tile(10*TILE_SIZE , 10*TILE_SIZE)
snake_body =[] # multiply the snake tiles
velocityX = 0
velocityY = 0

game_over = False


def restart_game():
    global snake, snake_body, food, velocityX, velocityY, game_over

    snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE)
    snake_body = []
    food = Tile(random.randint(0, COLUMNS - 1) * TILE_SIZE,
                random.randint(0, ROWS - 1) * TILE_SIZE)
    velocityX = 0
    velocityY = 0
    game_over = False

    draw()  # restart the game loop


# def change_direction(e): #e = event 
#     global velocityX , velocityY , game_over

#     if (game_over):
#         return
def change_direction(e): #e = event
    global velocityX, velocityY, game_over

    if game_over:
        if e.keysym == "Return":
            restart_game()
        return


    if e.keysym == "Up" and velocityY != 1:
        velocityX = 0
        velocityY = -1
    elif e.keysym == "Down" and velocityY != -1:
        velocityX = 0
        velocityY = 1
    elif e.keysym == "Left" and velocityX != 1:
        velocityX = -1
        velocityY = 0
    elif e.keysym == "Right" and velocityX != -1:
        velocityX = 1
        velocityY = 0

def move():
    global snake , game_over , snake_body , food
    if (game_over):
        return
    
       # Move body
    if snake_body:
        snake_body = [Tile(snake.x, snake.y)] + snake_body[:-1]

     #move head
    snake.x += velocityX*TILE_SIZE
    snake.y += velocityY*TILE_SIZE

    #wall collisoon
    if (snake.x <0 or snake.x >= WINDOW_WIDTH or snake.y <0 or snake.y >=WINDOW_HEIGHT):
        game_over = True
        return
    #self collision
    for tile in snake_body:
        if(snake.x == tile.x and snake.y ==tile.y):
            game_over= True
            return


    
# Food collision
    if (snake.x == food.x and snake.y == food.y):
        # Add new tile at the end (copy last tile's position)
        if snake_body:
            last_tile = snake_body[-1]
            snake_body.append(Tile(last_tile.x, last_tile.y))
        else:
            snake_body.append(Tile(snake.x, snake.y))
        # Move food
        food.x = random.randint(0, COLUMNS - 1) * TILE_SIZE
        food.y = random.randint(0, ROWS - 1) * TILE_SIZE

    
def draw():
    global snake
    move() #moves 10times ... loop
    canvas.delete("all") #cleans the frame

    #draw food
    canvas.create_rectangle(food.x , food.y , food.x+TILE_SIZE , food.y + TILE_SIZE , fill="green")

    # Draw snake head as a circle
    canvas.create_oval(
        snake.x, snake.y,
        snake.x + TILE_SIZE, snake.y + TILE_SIZE,
        fill="red"
    )
    # Draw snake body as rectangles
    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill="red")


    # #draw snake
    # canvas.create_rectangle(snake.x , snake.y , snake.x + TILE_SIZE , snake.y + TILE_SIZE , fill="black")
    
    # for tile in snake_body:
    #     canvas.create_rectangle(tile.x , tile.y , tile.x + TILE_SIZE , tile.y + TILE_SIZE , fill = "black")



    # Show Game Over message
    if game_over:
        canvas.create_text(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2,
            text="GAME OVER",
            fill="red",
            font=("Arial", 32, )
        )
    else:
        window.after(150, draw)

draw()
window.bind("<KeyRelease>" , change_direction)
window.mainloop()