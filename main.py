import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
BIRD_SIZE = 80
PIPE_WIDTH = 200  # Adjusted for new pipe image size
PIPE_GAP = 250
GRAVITY = 0.5
FLAP_STRENGTH = -8
SPEED = 5

# Load Assets
background_img = pygame.image.load("img/background.png")
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
bird_img = pygame.image.load("img/bird.png")  # Ensure you have a bird image
bird_img = pygame.transform.scale(bird_img, (80, 80))
pipe_img = pygame.image.load("img/stone.png")  # Updated to new pipe image
pipe_img = pygame.transform.scale(pipe_img, (PIPE_WIDTH, SCREEN_HEIGHT // 2))

# Setup Display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Flappy Bird Left to Right")

# Bird Class
class Bird:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.alive = True
    
    def flap(self):
        self.velocity = FLAP_STRENGTH
    
    def move(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        
        # Collision with top or bottom
        if self.y <= 0 or self.y >= SCREEN_HEIGHT - BIRD_SIZE:
            self.alive = False
    
    def draw(self):
        screen.blit(bird_img, (self.x, self.y))

# Pipe Class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        self.passed = False
    
    def move(self):
        self.x -= SPEED
    
    def draw(self):
        screen.blit(pipe_img, (self.x, self.height - pipe_img.get_height()))
        screen.blit(pygame.transform.flip(pipe_img, False, True), (self.x, self.height + PIPE_GAP))
    
    def collide(self, bird):
        if bird.x + BIRD_SIZE > self.x and bird.x < self.x + PIPE_WIDTH:
            if bird.y < self.height or bird.y + BIRD_SIZE > self.height + PIPE_GAP:
                return True
        return False

# Main Game Function
def main():
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH + i * 300) for i in range(5)]
    score = 0
    running = True

    while running:
        clock.tick(30)
        screen.blit(background_img, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        if bird.alive:
            bird.move()
            for pipe in pipes:
                pipe.move()
                if pipe.collide(bird):
                    bird.alive = False
                if not pipe.passed and pipe.x + PIPE_WIDTH < bird.x:
                    score += 1
                    pipe.passed = True
                
            if pipes[0].x < -PIPE_WIDTH:
                pipes.pop(0)
                pipes.append(Pipe(pipes[-1].x + 300))
        
        bird.draw()
        for pipe in pipes:
            pipe.draw()
        
        # Draw Score
        font = pygame.font.Font(None, 50)
        score_text = font.render(f"Score: {score}", True, (255, 0, 0))
        screen.blit(score_text, (50, 50))
        
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
