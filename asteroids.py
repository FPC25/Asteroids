import pygame
import random

from circleshape import CircleShape
from constants import *


class Asteroid(CircleShape):
    
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)
    
    def update(self, dt):
        self.position += self.velocity * dt
    
    def __creating_new_asteroid(self, velocity):
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        new_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid.velocity = velocity * 1.2
    
    def split(self):
        self.kill()
        if self.radius == ASTEROID_MIN_RADIUS:
            return 
        
        angle = random.uniform(20, 50)
        velocity1 = self.velocity.rotate(angle)
        velocity2 = self.velocity.rotate(-angle)
        
        self.__creating_new_asteroid(velocity1)
        self.__creating_new_asteroid(velocity2)