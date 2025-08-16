import tkinter as tk
import random

class SnakeGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Snake Game")
        self.root.geometry("600x650")
        self.root.configure(bg='black')
        self.root.resizable(False, False)
        
        # Game variables
        self.GAME_WIDTH = 600
        self.GAME_HEIGHT = 600
        self.SPEED = 150
        self.SPACE_SIZE = 25
        self.BODY_PARTS = 3
        self.SNAKE_COLOR = "#00FF00"
        self.FOOD_COLOR = "#FF0000"
        self.BACKGROUND_COLOR = "#000000"
        
        self.score = 0
        self.direction = 'down'
        
        # UI Elements
        self.label = tk.Label(self.root, text=f"Score: {self.score}", 
                             font=('Arial', 20), fg='white', bg='black')
        self.label.pack()
        
        self.canvas = tk.Canvas(self.root, bg=self.BACKGROUND_COLOR,
                               height=self.GAME_HEIGHT, width=self.GAME_WIDTH)
        self.canvas.pack()
        
        # Initialize game
        self.snake = [[0, 0], [0, self.SPACE_SIZE], [0, self.SPACE_SIZE * 2]]
        self.food = self.create_food()
        
        # Key bindings
        self.root.bind('<Key>', self.change_direction)
        self.root.focus_set()
        
        self.next_turn()
        
    def create_food(self):
        x = random.randint(0, (self.GAME_WIDTH // self.SPACE_SIZE) - 1) * self.SPACE_SIZE
        y = random.randint(0, (self.GAME_HEIGHT // self.SPACE_SIZE) - 1) * self.SPACE_SIZE
        return [x, y]
    
    def next_turn(self):
        x, y = self.snake[0]
        
        if self.direction == "up":
            y -= self.SPACE_SIZE
        elif self.direction == "down":
            y += self.SPACE_SIZE
        elif self.direction == "left":
            x -= self.SPACE_SIZE
        elif self.direction == "right":
            x += self.SPACE_SIZE
            
        self.snake.insert(0, [x, y])
        
        if x == self.food[0] and y == self.food[1]:
            self.score += 1
            self.label.config(text=f"Score: {self.score}")
            self.food = self.create_food()
        else:
            self.snake.pop()
            
        if self.check_collisions():
            self.game_over()
        else:
            self.update_canvas()
            self.root.after(self.SPEED, self.next_turn)
    
    def change_direction(self, event):
        new_direction = event.keysym.lower()
        
        directions = ['up', 'down', 'left', 'right']
        if new_direction in directions:
            if new_direction == 'up' and self.direction != 'down':
                self.direction = new_direction
            elif new_direction == 'down' and self.direction != 'up':
                self.direction = new_direction
            elif new_direction == 'left' and self.direction != 'right':
                self.direction = new_direction
            elif new_direction == 'right' and self.direction != 'left':
                self.direction = new_direction
    
    def check_collisions(self):
        x, y = self.snake[0]
        
        # Check boundaries
        if x < 0 or x >= self.GAME_WIDTH or y < 0 or y >= self.GAME_HEIGHT:
            return True
            
        # Check self collision
        for body_part in self.snake[1:]:
            if x == body_part[0] and y == body_part[1]:
                return True
                
        return False
    
    def update_canvas(self):
        self.canvas.delete("all")
        
        # Draw food
        self.canvas.create_oval(self.food[0], self.food[1],
                               self.food[0] + self.SPACE_SIZE,
                               self.food[1] + self.SPACE_SIZE,
                               fill=self.FOOD_COLOR, tags="food")
        
        # Draw snake
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1],
                                       segment[0] + self.SPACE_SIZE,
                                       segment[1] + self.SPACE_SIZE,
                                       fill=self.SNAKE_COLOR, tags="snake")
    
    def game_over(self):
        self.canvas.delete("all")
        self.canvas.create_text(self.GAME_WIDTH // 2, self.GAME_HEIGHT // 2,
                               font=('Arial', 30), text="GAME OVER",
                               fill="red", tags="gameover")
        self.canvas.create_text(self.GAME_WIDTH // 2, self.GAME_HEIGHT // 2 + 50,
                               font=('Arial', 20), text=f"Final Score: {self.score}",
                               fill="white", tags="score")
        self.canvas.create_text(self.GAME_WIDTH // 2, self.GAME_HEIGHT // 2 + 100,
                               font=('Arial', 16), text="Press R to restart",
                               fill="yellow", tags="restart")
        self.root.bind('<Key>', self.restart_game)
    
    def restart_game(self, event):
        if event.keysym.lower() == 'r':
            self.root.destroy()
            new_game = SnakeGame()
            new_game.run()
    
    def run(self):
        self.root.mainloop()

# Jalankan game
if __name__ == "__main__":
    game = SnakeGame()
    game.run()
