import pygame
from constants import *
from player import Player
from asteroids import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def grouping():
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

def game_loop(screen: object, updatable, drawable, asteroids, shots, player: object, dt: float, fps: object) -> None:
    # while playing the game
    while True:
        
        # turning events on
        for event in pygame.event.get():
            # enabling the close button 
            if event.type == pygame.QUIT:
                return
        
        #for all objects on the updatable group, update it
        for spr in updatable:
            spr.update(dt)

        for asteroid in asteroids:
            if asteroid.collision(player):
                print("Game over!")
                exit()
            
            for bullet in shots:
                if asteroid.collision( bullet):
                    bullet.kill()
                    asteroid.split()
                
        # filling the screen with a back color  
        screen.fill("#000000")
        
        #for all object to be draw, do it
        for spr in drawable:
            spr.draw(screen)
    
        # making sure to refresh the screen
        pygame.display.flip()
        
        #limiting the fps to 60
        dt = fps.tick(60)/1000

def main():
    # initiating the game
    pygame.init()
    
    # creating the screen 
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # setting the variables to limit the fps
    fps = pygame.time.Clock()
    dt = 0
    
    updatable, drawable, asteroids, shots = grouping()
    
    # instantiating the player:
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    
    # initialization from asteroid field
    asteroid_field = AsteroidField()
    
    game_loop(screen, updatable, drawable, asteroids, shots, player, dt, fps)
    
        
    
if __name__ == "__main__":
    main()