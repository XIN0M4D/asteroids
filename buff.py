from constants import LINE_WIDTH, BUFF_RADIUS
from circleshape import CircleShape
import pygame

class Buff(CircleShape):
     def __init__(self, x, y):
        super().__init__(x, y, BUFF_RADIUS )
        