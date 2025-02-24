import pygame

from enum import Enum


class GameState(Enum):
    
    MENU = 1
    PLAYING = 2
    SCOREBOARD = 3
    PAUSED = 4
    END_GAME = 5
 
   
class GameScreens:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.background = pygame.image.load("./background.jpeg")
        self.selected_option = 0
        self.menu_options = ["Start Game", "Score Board", "Exit"]
    
    def draw_menu(self, fps, rate):
        
        while True:
            dt = fps.tick(rate)/1000
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                        print(f"Selected: {self.menu_options[self.selected_option]}")  # Debug print
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                        print(f"Selected: {self.menu_options[self.selected_option]}")  # Debug print
                    elif event.key == pygame.K_RETURN:
                        return self.handle_menu_selection()
                    
            self.screen.blit(self.background, (0, 0))
            self.draw_menu_options()
            pygame.display.flip()
            
    def draw_menu_options(self):
        
        # Title setup
        title_font = pygame.font.Font(None, 128)  # Bigger font for title
        title_text = "ASTEROIDS"
        title_color = (255, 165, 0)  # Orange color (you can adjust this)
        title_y = 150  # Position from top
        
        # Render title with a cool effect (optional glow/shadow)
        title_shadow = title_font.render(title_text, True, (139, 69, 19))  # Darker orange shadow
        title = title_font.render(title_text, True, title_color)
        
        # Position title
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, title_y))
        title_shadow_rect = title_shadow.get_rect(center=(self.screen.get_width() // 2 + 4, title_y + 4))
        
        # Draw title
        self.screen.blit(title_shadow, title_shadow_rect)  # Draw shadow first
        self.screen.blit(title, title_rect)  # Draw main title
        
        
        font = pygame.font.Font(None, 64)  # None uses default font, 64 is text size
        menu_y = 300  # Starting y position for first option
        spacing = 80  # Vertical space between options


        # Button dimensions
        button_width = 300
        button_height = 60
        button_alpha = 128  # Transparency (0 is fully transparent, 255 is solid)
    
        for i, option in enumerate(self.menu_options):
            
            button_surface = pygame.Surface((button_width, button_height))
            button_surface.fill((0, 0, 0))  # Fill with black
            button_surface.set_alpha(button_alpha)  # Set transparency
            
            # Position for the button
            button_rect = button_surface.get_rect(
                center=(self.screen.get_width() // 2, menu_y + i * spacing)
            )
            
            # Text color (white for selected, gray for unselected)
            color = (255, 255, 255) if i == self.selected_option else (128, 128, 128)

            # Render text
            text = font.render(option, True, color)
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, menu_y + i * spacing))
            
            # Draw button and text
            self.screen.blit(button_surface, button_rect)
            self.screen.blit(text, text_rect)
    
    def handle_menu_selection(self):
        if self.selected_option == 0:
            return GameState.PLAYING
        elif self.selected_option == 1:
            return GameState.SCOREBOARD
        elif self.selected_option == 2:
            return None

    def draw_scoreboard(self):
        # Implementation for scoreboard screen
        pass