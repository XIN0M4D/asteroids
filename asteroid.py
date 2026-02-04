from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
import pygame
import random
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)
        
    def update(self, dt):
        self.position += (self.velocity * dt)

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return "killed"
        log_event("asteroid_split")
        random_angle = random.uniform(20, 50)
        new_vector_1 = self.velocity.rotate(+random_angle)
        new_vector_2 = self.velocity.rotate(-random_angle)
        new_asteroid_radius = self.radius - ASTEROID_MIN_RADIUS
        new_roid_1 = Asteroid(self.position, self.position, new_asteroid_radius)
        new_roid_2 = Asteroid(self.position, self.position , new_asteroid_radius)
        new_roid_1.velocity = new_vector_1 * 1.2
        new_roid_2.velocity = new_vector_2 * 1.2
        return "split"