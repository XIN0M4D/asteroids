import pygame
from circleshape import CircleShape

class Knockback_Wave(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, 0)
        self.max_radius = 200
        self.growth_rate = 150      

    def update(self, dt):
        self.radius += self.growth_rate * dt
        if self.radius >= self.max_radius:
            self.kill()

    def draw(self, screen):
        pygame.draw.circle( screen, "purple", (int(self.position.x), int(self.position.y)), int(self.radius), 2 )