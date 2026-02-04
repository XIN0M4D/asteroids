from constants import LINE_WIDTH, BUFF_RADIUS
from buff import Buff
import pygame

class ShieldBuff(Buff):
    def __init__(self, x, y):
        super().__init__(x, y)
    
    def draw(self, screen):
        pygame.draw.circle(screen, "blue", self.position, self.radius, LINE_WIDTH)
        