import pygame

from shot import Shot
from constants import *
from player import Player
from asteroids import Asteroid
from pygame.sprite import Group
from asteroidfield import AsteroidField
from gamestates import GameScreens, GameState


def check_quit_event() -> bool:
    """Checks if the quit event (X button) has been triggered.
    
    Returns:
        bool: True if game should quit, False if game should continue
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    return False

def grouping() -> tuple[Group, Group, Group, Group]:
    """Creates and configures sprite groups for game objects.
    
    Creates separate groups for:
        - updatable: Objects that need position/state updates
        - drawable: Objects that need to be drawn
        - asteroids: All asteroid objects for collision detection
        - shots: All projectiles for collision detection
    
    Also assigns container relationships for:
        - Player: Updates and draws
        - Asteroid: Updates, draws, and asteroid-specific handling
        - AsteroidField: Updates only
        - Shot: Updates, draws, and shot-specific handling
    
    Returns:
        tuple: Contains the following sprite groups in order:
            - updatable: Group for updating object states
            - drawable: Group for drawing objects
            - asteroids: Group for asteroid management
            - shots: Group for projectile management
    """
    
    
    # initiating the groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    #adding objects to the groups
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    
    return updatable, drawable, asteroids, shots


def menu_screen():
    pass

def updating_group(group_name: str, group: Group, *args) -> None:
    """Updates or draws all sprites in a sprite group.
    
    Handles two types of sprite group operations:
        - "updatable": Updates each sprite's position/state using dt (1/fps)
        - "drawable": Draws each sprite to the screen surface
    
    Args:
        group_name: Type of operation ("updatable" or "drawable")
        group: Pygame sprite group containing game objects
        *args: Single argument required:
            - dt (float): Delta time for updates
            - screen (Surface): Pygame surface for drawing
    
    Raises:
        ValueError: If more than one argument is passed
        ValueError: If no argument is passed
        ValueError: If group_name is not "updatable" or "drawable"
    """
    
    if len(args) > 1:
        raise ValueError("Too many arguments passed.")
    
    if len(args) == 0:
        raise ValueError("Must receive an argument related to the group. If updatable, the 1/fps; If drawable the screen object.")
    
    for spr in group:
        if group_name == "updatable":
            spr.update(args[0])
            
        elif group_name == "drawable":
            spr.draw(args[0])
            
        else:
            raise ValueError(f"{group_name} groups is not supported.")
            
def asteroid_collisions(asteroid_group: Group, shots_group: Group, player: Player) -> None:
    """
    Checks for:
        - Player collision with any asteroid (game over)
        - Shot collisions with asteroids (destroys both, splits asteroid)
    
    Args:
        asteroid_group: Group containing all asteroid objects
        shots_group: Group containing all projectiles
        player: The player's ship object
    
    Returns:
        bool: True if player collided (game over), False if game continues
    """
    
    for asteroid in asteroid_group:
        if asteroid.collision(player):
            return True
        
        for bullet in shots_group:
            if asteroid.collision(bullet):
                bullet.kill()
                asteroid.split()
        
    return False


def game_loop(
    screen: pygame.Surface, 
    updatable: Group, 
    drawable: Group, 
    asteroids: Group, 
    shots: Group, 
    player: Player, 
    dt: float, 
    fps: pygame.time.Clock
    ) -> int:
    
    """Runs the main game loop.
    
    Handles:
        - Event checking (quit)
        - Object updates
        - Collision detection
        - Screen drawing/rendering
        - FPS limiting
    
    Args:
        screen: Game display surface
        updatable: Group of objects requiring updates
        drawable: Group of objects to be drawn
        asteroids: Group of asteroid objects
        shots: Group of projectiles
        player: Player ship instance
        dt: Delta time for frame rate independence (it converts milliseconds to seconds)
        fps: Clock for controlling frame rate
        
    Returns:
        int: Game end status
            0: Normal exit (player closed window)
            1: Game over (player crashed into asteroid)
    """
    
    # while playing the game
    while True:
        
        if check_quit_event():
            return 0
            
        #for all objects on the updatable group, update it
        updating_group("updatable", updatable, dt)

        #checking for collisions with asteroids
        if asteroid_collisions(asteroids, shots, player):
            return 1
               
        # filling the screen with a back color  
        screen.fill("#000000")
        
        #for all object to be draw, do it
        updating_group("drawable", drawable, screen)
    
        # making sure to refresh the screen
        pygame.display.flip()
        
        #limiting the fps to 60
        dt = fps.tick(60)/1000

def main():
    """Initializes and starts the game.
    
    Sets up:
        - Pygame initialization
        - Screen display
        - FPS control
        - Sprite groups
        - Player instance
        - Asteroid field
        
    Then passes control to the game loop
    
    Raises:
        pygame.error: If pygame fails to initialize
        SystemError: If screen cannot be created
    """

    try:
        # initiating the game
        pygame.init()
        if pygame.get_error():
            raise SystemError("Pygame failed to initialize properly")
        
        # creating the screen 
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        if not screen:
            raise SystemError("Could not create game screen")
        
        # setting the variables to limit the fps
        fps = pygame.time.Clock()
        dt = 0
        
        game_screens = GameScreens(screen)
        current_state = GameState.MENU
        
        while current_state is not None:
            if current_state == GameState.MENU:
                current_state = game_screens.draw_menu(fps, 60)
            
            elif current_state == GameState.PLAYING:
                updatable, drawable, asteroids, shots = grouping()
                
                # instantiating the player:
                player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                
                # initialization from asteroid field
                asteroid_field = AsteroidField()
                end_status = game_loop(screen, updatable, drawable, asteroids, shots, player, dt, fps)
                if end_status == 1:
                    print("Game Over!")
                    current_state = GameState.MENU
            
            elif current_state == GameState.SCOREBOARD:
                current_state = game_screens.draw_scoreboard()
                
            elif current_state == GameState.PAUSED: 
                pass
            
            elif current_state == GameState.END_GAME:
                current_state = GameState.MENU
        
    except (pygame.error, SystemError) as e:
        print(f"Failed to start game: {e}")

    finally:
        pygame.quit()
    
        
    
if __name__ == "__main__":
    main()