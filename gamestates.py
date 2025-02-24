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
    
    def check_quit_event() -> bool:
        """Checks if the quit event (X button) has been triggered.
        
        Returns:
            bool: True if game should quit, False if game should continue
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False
    
    
    def draw_menu(self, fps, rate):
        
        while True:
            dt = fps.tick(rate)/1000
            
            if self.check_quit_event():
                return None
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                    elif event.key == pygame.K_RETURN:
                        return self.handle_menu_selection()
                    
            self.screen.blit(self.background, (0, 0))
            self.draw_menu_options()
            self.display.flip()
            
    def draw_menu_options(self):
        pass
    
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