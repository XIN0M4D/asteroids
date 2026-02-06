from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOT_SPEED, SHOT_RADIUS, PLAYER_SHOOT_COOLDOWN_SECONDS
from circleshape import CircleShape
from shot import Shot
from knockback_wave import Knockback_Wave
import pygame

class Player(CircleShape):

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown_timer = 0
        self.color = "pink"
        self.piercing_shot_count = 0
        self.knockback_charge = 0
        self.shield_state = False
    
    
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.triangle(), LINE_WIDTH)

    def rotate(self, dt):
        self.rotation += (PLAYER_TURN_SPEED * dt)

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector
        
    def strafe_right(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation + 90)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def strafe_left(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation - 90)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        if self.shot_cooldown_timer > 0:
            return
        
        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOT_SPEED

        if self.piercing_shot_count > 0:
            shot.color = "red"  
            self.piercing_shot_count -= 1
        else:
            shot.color = "pink"  
    
        self.shot_cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
        if self.piercing_shot_count > 0:
            self.piercing_shot_count -= 1

    def knockback(self):
        if self.knockback_charge >= 100:
            Knockback_Wave(self.position.x, self.position.y)
            self.knockback_charge -= 100

        

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if self.shot_cooldown_timer > 0:
            self.shot_cooldown_timer -= dt

        if keys[pygame.K_a]:
            self.rotate(-1 * dt)
        if keys[pygame.K_q]:
            self.strafe_left(dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_e]:
            self.strafe_right(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-1 * dt)
        if keys[pygame.K_SPACE]:
                self.shoot()
        if keys[pygame.K_r]:
            self.knockback()
