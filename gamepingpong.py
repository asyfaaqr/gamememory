import pygame
import sys
import random

class PongGame:
    def __init__(self):
        pygame.init()
        
        # Constants
        self.WIDTH = 800
        self.HEIGHT = 600
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 100, 255)
        self.RED = (255, 100, 0)
        
        # Screen setup
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pong Game")
        self.clock = pygame.time.Clock()
        
        # Game objects
        self.ball = {
            'x': self.WIDTH // 2,
            'y': self.HEIGHT // 2,
            'dx': random.choice([-5, 5]),
            'dy': random.choice([-3, 3]),
            'size': 15
        }
        
        self.player1 = {
            'x': 50,
            'y': self.HEIGHT // 2 - 50,
            'width': 15,
            'height': 100,
            'speed': 6
        }
        
        self.player2 = {
            'x': self.WIDTH - 65,
            'y': self.HEIGHT // 2 - 50,
            'width': 15,
            'height': 100,
            'speed': 6
        }
        
        self.score1 = 0
        self.score2 = 0
        self.font = pygame.font.Font(None, 74)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
    
    def update(self):
        keys = pygame.key.get_pressed()
        
        # Player 1 controls (W/S)
        if keys[pygame.K_w] and self.player1['y'] > 0:
            self.player1['y'] -= self.player1['speed']
        if keys[pygame.K_s] and self.player1['y'] < self.HEIGHT - self.player1['height']:
            self.player1['y'] += self.player1['speed']
            
        # Player 2 controls (UP/DOWN arrows)
        if keys[pygame.K_UP] and self.player2['y'] > 0:
            self.player2['y'] -= self.player2['speed']
        if keys[pygame.K_DOWN] and self.player2['y'] < self.HEIGHT - self.player2['height']:
            self.player2['y'] += self.player2['speed']
        
        # Ball movement
        self.ball['x'] += self.ball['dx']
        self.ball['y'] += self.ball['dy']
        
        # Ball collision with top/bottom walls
        if self.ball['y'] <= 0 or self.ball['y'] >= self.HEIGHT - self.ball['size']:
            self.ball['dy'] = -self.ball['dy']
        
        # Ball collision with paddles
        ball_rect = pygame.Rect(self.ball['x'], self.ball['y'], self.ball['size'], self.ball['size'])
        player1_rect = pygame.Rect(self.player1['x'], self.player1['y'], 
                                  self.player1['width'], self.player1['height'])
        player2_rect = pygame.Rect(self.player2['x'], self.player2['y'],
                                  self.player2['width'], self.player2['height'])
        
        if ball_rect.colliderect(player1_rect) and self.ball['dx'] < 0:
            self.ball['dx'] = -self.ball['dx']
            self.ball['dy'] += random.randint(-2, 2)
            
        if ball_rect.colliderect(player2_rect) and self.ball['dx'] > 0:
            self.ball['dx'] = -self.ball['dx']
            self.ball['dy'] += random.randint(-2, 2)
        
        # Scoring
        if self.ball['x'] < 0:
            self.score2 += 1
            self.reset_ball()
        elif self.ball['x'] > self.WIDTH:
            self.score1 += 1
            self.reset_ball()
    
    def reset_ball(self):
        self.ball['x'] = self.WIDTH // 2
        self.ball['y'] = self.HEIGHT // 2
        self.ball['dx'] = random.choice([-5, 5])
        self.ball['dy'] = random.choice([-3, 3])
    
    def draw(self):
        self.screen.fill(self.BLACK)
        
        # Draw center line
        for i in range(0, self.HEIGHT, 20):
            pygame.draw.rect(self.screen, self.WHITE, (self.WIDTH // 2 - 2, i, 4, 10))
        
        # Draw paddles
        pygame.draw.rect(self.screen, self.BLUE, 
                        (self.player1['x'], self.player1['y'], 
                         self.player1['width'], self.player1['height']))
        pygame.draw.rect(self.screen, self.RED,
                        (self.player2['x'], self.player2['y'],
                         self.player2['width'], self.player2['height']))
        
        # Draw ball
        pygame.draw.ellipse(self.screen, self.WHITE,
                           (self.ball['x'], self.ball['y'], 
                            self.ball['size'], self.ball['size']))
        
        # Draw scores
        score_text = self.font.render(f"{self.score1}  {self.score2}", True, self.WHITE)
        text_rect = score_text.get_rect(center=(self.WIDTH // 2, 50))
        self.screen.blit(score_text, text_rect)
        
        # Draw controls
        controls_font = pygame.font.Font(None, 36)
        control_text1 = controls_font.render("Player 1: W/S", True, self.BLUE)
        control_text2 = controls_font.render("Player 2: UP/DOWN", True, self.RED)
        self.screen.blit(control_text1, (20, 20))
        self.screen.blit(control_text2, (self.WIDTH - 200, 20))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

# Jalankan game
if __name__ == "__main__":
    game = PongGame()
    game.run()
