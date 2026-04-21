from circleshape import CircleShape
import pygame
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event
import random

class Asteroid(CircleShape):

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
         pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH) # type: ignore

    def update(self, dt):
        self.position += self.velocity * dt
    
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        angle = random.uniform(20, 50)
        vel_1 = self.velocity.rotate(angle)
        vel_2 = self.velocity.rotate(-angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        child_1 = Asteroid(self.position.x, self.position.y, new_radius) # type: ignore
        child_2 = Asteroid(self.position.x, self.position.y, new_radius) # type: ignore
        child_1.velocity = vel_1 * 1.2
        child_2.velocity = vel_2 * 1.2