import tkinter as tk
from tkinter import messagebox
import random
import time

class MemoryGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Memory Card Game")
        self.root.geometry("600x700")
        self.root.configure(bg='navy')
        
        # Game variables
        self.grid_size = 4
        self.cards = []
        self.revealed = []
        self.matched = []
        self.first_card = None
        self.second_card = None
        self.moves = 0
        self.start_time = time.time()
        
        # Create symbols for cards
        symbols = ['🎮', '🎯', '🎲', '🎪', '🎨', '🎭', '🎪', '🎺'] * 2
        random.shuffle(symbols)
        self.card_values = symbols
        
        # UI Setup
        self.setup_ui()
        self.create_board()
        
    def setup_ui(self):
        # Title
        title_label = tk.Label(self.root, text="MEMORY GAME", 
                              font=('Arial', 24, 'bold'), 
                              fg='white', bg='navy')
        title_label.pack(pady=10)
        
        # Score frame
        score_frame = tk.Frame(self.root, bg='navy')
        score_frame.pack(pady=10)
        
        self.moves_label = tk.Label(score_frame, text="Moves: 0", 
                                   font=('Arial', 16), fg='white', bg='navy')
        self.moves_label.pack(side=tk.LEFT, padx=20)
        
        self.time_label = tk.Label(score_frame, text="Time: 0s", 
                                  font=('Arial', 16), fg='white', bg='navy')
        self.time_label.pack(side=tk.LEFT, padx=20)
        
        # Game board frame
        self.board_frame = tk.Frame(self.root, bg='navy')
        self.board_frame.pack(pady=20)
        
        # Restart button
        restart_btn = tk.Button(self.root, text="Restart Game", 
                               font=('Arial', 14), command=self.restart_game,
                               bg='orange', fg='white', relief='raised')
        restart_btn.pack(pady=10)
        
        # Update timer
        self.update_timer()
    
    def create_board(self):
        self.buttons = []
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                btn = tk.Button(self.board_frame, 
                               text="?", 
                               font=('Arial', 20, 'bold'),
                               width=4, height=2,
                               bg='lightblue', 
                               fg='darkblue',
                               relief='raised',
                               command=lambda r=i, c=j: self.card_clicked(r, c))
                btn.grid(row=i, column=j, padx=5, pady=5)
                row.append(btn)
            self.buttons.append(row)
    
    def card_clicked(self, row, col):
        if (row, col) in self.revealed or (row, col) in self.matched:
            return
            
        if self.first_card is None:
            self.first_card = (row, col)
            self.reveal_card(row, col)
        elif self.second_card is None and (row, col) != self.first_card:
            self.second_card = (row, col)
            self.reveal_card(row, col)
            self.moves += 1
            self.moves_label.config(text=f"Moves: {self.moves}")
            self.root.after(1000, self.check_match)
    
    def reveal_card(self, row, col):
        index = row * self.grid_size + col
        symbol = self.card_values[index]
        self.buttons[row][col].config(text=symbol, bg='white')
        self.revealed.append((row, col))
    
    def hide_card(self, row, col):
        self.buttons[row][col].config(text="?", bg='lightblue')
        if (row, col) in self.revealed:
            self.revealed.remove((row, col))
    
    def check_match(self):
        if self.first_card and self.second_card:
            r1, c1 = self.first_card
            r2, c2 = self.second_card
            
            index1 = r1 * self.grid_size + c1
            index2 = r2 * self.grid_size + c2
            
            if self.card_values[index1] == self.card_values[index2]:
                # Match found
                self.matched.extend([self.first_card, self.second_card])
                self.buttons[r1][c1].config(bg='lightgreen')
                self.buttons[r2][c2].config(bg='lightgreen')
                
                if len(self.matched) == self.grid_size * self.grid_size:
                    self.game_won()
            else:
                # No match
                self.hide_card(r1, c1)
                self.hide_card(r2, c2)
            
            self.first_card = None
            self.second_card = None
    
    def update_timer(self):
        if len(self.matched) < self.grid_size * self.grid_size:
            elapsed = int(time.time() - self.start_time)
            self.time_label.config(text=f"Time: {elapsed}s")
            self.root.after(1000, self.update_timer)
    
    def game_won(self):
        elapsed = int(time.time() - self.start_time)
        messagebox.showinfo("Congratulations!", 
                           f"You won!\nMoves: {self.moves}\nTime: {elapsed} seconds")
    
    def restart_game(self):
        # Reset game variables
        self.revealed = []
        self.matched = []
        self.first_card = None
        self.second_card = None
        self.moves = 0
        self.start_time = time.time()
        
        # Shuffle cards
        random.shuffle(self.card_values)
        
        # Reset buttons
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.buttons[i][j].config(text="?", bg='lightblue')
        
        # Reset labels
        self.moves_label.config(text="Moves: 0")
        self.time_label.config(text="Time: 0s")
        
        # Restart timer
        self.update_timer()
    
    def run(self):
        self.root.mainloop()

# Jalankan game
if __name__ == "__main__":
    game = MemoryGame()
    game.run()
