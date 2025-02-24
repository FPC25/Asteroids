import pygame

from shot import Shot
from circleshape import CircleShape
from constants import *


class Player(CircleShape):
    
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0
        
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
            
            
    def shoot(self):
        bullet = Shot(self.position.x, self.position.y)
        bullet.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        self.timer = PLAYER_SHOOT_COLDDOWN

        
        
            
            
    