import pygame

from shot import Shot
from constants import *
from circleshape import CircleShape
from gamestates import GameState, GameScreens


class Player(CircleShape):
    
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0
        self.lives = PLAYER_NUM_LIVES
        
    # in the player class
    def triangle(self) -> list:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c] 
    
    def draw(self, screen: object):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)
        
    def rotate(self, dt: float) -> None:
        self.rotation += PLAYER_ROTATION_SPEED * dt
    
    def move(self, dt: float) -> None:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
        
    def update(self, dt):
        keys = pygame.key.get_pressed()
        
        if self.timer > 0:
            self.timer -= dt
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotate(-dt)
            
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotate(dt)
            
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move(dt)
        
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(-dt)
            
        if keys[pygame.K_SPACE]:
            if self.timer <= 0:
                self.shoot()
                
        if keys[pygame.K_ESCAPE]:
            #pause
            pass
                
        self.wrap_position()
    
    def wrap_position(self):
        if self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        if self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = SCREEN_HEIGHT    
            
    def shoot(self):
        bullet = Shot(self.position.x, self.position.y)
        bullet.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        self.timer = PLAYER_SHOOT_COOLDOWN

        
        
            
            
    