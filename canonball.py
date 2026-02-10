from circleshape import CircleShape
from constants import CANON_SHOT_RADIUS, LINE_WIDTH
import pygame

class Canonball(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.radius = CANON_SHOT_RADIUS
        self.color = "pink"

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius, LINE_WIDTH)
        
    def update(self, dt):
        self.position += (self.velocity * dt)