import pygame
import math

pygame.init()

FPS = 60
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
BACKGROUND_COLOR = (217, 217, 217)
DISTANCE = 300
ICON_SIZE = 125
ANIMATION_TIME = 4

# Set up the display window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Endless Scroll Diagonal")

# Load the icon image
icon = pygame.image.load("icon.png").convert_alpha()

class ScrollingBackground:
    def __init__(self, image, distance):
        self.image = image
        self.distance = distance
        self.scroll_x = 0
        self.scroll_y = 0
        # Calculate the number of tiles needed to cover the screen
        self.tiles_x = math.ceil(SCREEN_WIDTH / distance) + 1
        self.tiles_y = math.ceil(SCREEN_HEIGHT / distance) + 1

    def update(self):
        # Update the scroll position to create the scrolling effect
        self.scroll_x += 2  # Horizontal scroll speed
        self.scroll_y += 1  # Vertical scroll speed
        # Wrap the scroll position to create endless scrolling
        if self.scroll_x > self.distance:
            self.scroll_x -= self.distance
        if self.scroll_y > self.distance:
            self.scroll_y -= self.distance

    def draw(self, surface, scale_factor, rotation_angle, move_offset):
        for x in range(self.tiles_x):
            for y in range(self.tiles_y):
                pos_x = x * self.distance - self.scroll_x
                pos_y = y * self.distance - self.scroll_y
                # Only draw tiles that are within the screen bounds
                if pos_x + ICON_SIZE > 0 and pos_y + ICON_SIZE > 0 and pos_x < SCREEN_WIDTH and pos_y < SCREEN_HEIGHT:
                    # Scale the icon based on the scale factor
                    scaled_icon = pygame.transform.scale(self.image, (int(ICON_SIZE * scale_factor), int(ICON_SIZE * scale_factor)))
                    # Rotate the scaled icon based on the rotation angle
                    rotated_icon = pygame.transform.rotate(scaled_icon, rotation_angle)
                    # Position the icon and apply the movement offset
                    rect = rotated_icon.get_rect(center=(pos_x + ICON_SIZE // 2 + move_offset, pos_y + ICON_SIZE // 2 + move_offset))
                    surface.blit(rotated_icon, rect.topleft)

def main():
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    background = ScrollingBackground(icon, DISTANCE)
    
    run = True
    while run:
        delta_time = clock.tick(FPS) / 1000.0
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Fill the screen with the background color
        screen.fill(BACKGROUND_COLOR)

        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000.0
        phase = (elapsed_time % ANIMATION_TIME) / ANIMATION_TIME

        # Calculate the dynamic scale factor
        scale_factor = 1.0 + 0.05 * math.sin(phase * 2 * math.pi)
        # Calculate the smooth rotation angle
        rotation_angle = 5 * math.sin(phase * 2 * math.pi)
        # Calculate the diagonal movement offset
        move_offset = 3 * math.sin(phase * 2 * math.pi)

        # Update and draw the background with the calculated parameters
        background.update()
        background.draw(screen, scale_factor, rotation_angle, move_offset)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
