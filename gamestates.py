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

    def _draw_menu_screen(self, title: str, options: list, fps, rate) -> GameState:
        self.selected_option = 0
        
        while True:
            dt = fps.tick(rate)/1000
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                        #print(f"Selected: {self.menu_options[self.selected_option]}")  # Debug print
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                        #print(f"Selected: {self.menu_options[self.selected_option]}")  # Debug print
                    elif event.key == pygame.K_RETURN:
                        return self._handle_menu_selection(options)
                    
                    elif event.key == pygame.K_ESCAPE and title == "PAUSED":
                        return GameState.PLAYING
                    
            self.screen.blit(self.background, (0, 0))
            self._draw_options(title, options)
            pygame.display.flip()
   
    def _draw_title(self, title: str):
        # Title setup
        title_font = pygame.font.Font(None, 128)  # Bigger font for title
        title_text = title.upper()
        title_color = (255, 165, 0)  # Orange color
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
   
    def _draw_options(self, title: str, options: list):
        
        self._draw_title(title)
        
        font = pygame.font.Font(None, 64)  # None uses default font, 64 is text size
        menu_y = 300  # Starting y position for first option
        spacing = 80  # Vertical space between options

        # Button dimensions
        button_width = 300
        button_height = 60
        button_alpha = 128  # Transparency (0 is fully transparent, 255 is solid)
    
        for i, option in enumerate(options):
            
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
   
    def _handle_menu_selection(self, options: list) -> GameState:
        
        if "Continue" in options: #Pause Menu
            if self.selected_option == 0:
                return GameState.PLAYING
            elif self.selected_option == 1:
                return GameState.MENU
            elif self.selected_option == 2:
                return None
            
        else: 
            if self.selected_option == 0:
                return GameState.PLAYING
            elif self.selected_option == 1:
                return GameState.SCOREBOARD
            elif self.selected_option == 2:
                return None
   
   
    def draw_menu(self, fps, rate):
        return self._draw_menu_screen("ASTEROIDS", ["Start Game", "Score Board", "Exit"], fps, rate)

    def draw_scoreboard(self):
        # Implementation for scoreboard screen
        pass
    
    def draw_pause_menu(self, fps, rate):
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0,0))
        
        return self._draw_menu_screen("PAUSED", ["Continue", "Return to Menu", "Exit"], fps, rate)