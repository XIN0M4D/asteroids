import pygame
import sys
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from logger import log_event
from circleshape import CircleShape
from shot import Shot
from shield_buff import ShieldBuff
from piercing_shots import PiercingShot
def show_start_menu(screen):
    font_title = pygame.font.SysFont(None, 72)
    font_info = pygame.font.SysFont(None, 36)

    clock = pygame.time.Clock()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    waiting = False

        screen.fill("black")

        title_surf = font_title.render("ASTEROIDS", True, (255, 255, 255))
        info_surf = font_info.render("Press SPACE to start", True, (200, 200, 200))

        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        info_rect = info_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))

        screen.blit(title_surf, title_rect)
        screen.blit(info_surf, info_rect)

        pygame.display.flip()
        clock.tick(60)

def run_game(screen):
    pygame.font.init()
    font = pygame.font.SysFont(None, 36)
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    ShieldBuffs = pygame.sprite.Group()
    PiercingShots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, drawable, updatable)
    ShieldBuff.containers = (ShieldBuffs,drawable, updatable)
    PiercingShot.containers = (PiercingShots, drawable, updatable)
    clock = pygame.time.Clock()
    dt = 0
    player = Player( SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    score = 0
    shield_state = False
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        updatable.update(dt)
        for shieldbuff in ShieldBuffs:
            if shieldbuff.collides_with(player):
                shieldbuff.kill()
                log_event("shield_gained")
                shield_state = True
                player.color = "blue"
        for piercingshot in PiercingShots:
            if piercingshot.collides_with(player):
                log_event("piercing_shots_gained")
                piercingshot.kill()
                player.piercing_shot_count += 25
        for object in asteroids:
            if object.collides_with(player) and shield_state == True:
                log_event("player_hit, shiled_lost")
                object.kill()
                shield_state = False
                player.color = "pink"
            elif object.collides_with(player) and shield_state == False:
                 log_event("player_hit")
                 score = 0
                 return
        for object in asteroids:
            for shot in shots:
                if object.collides_with(shot) and player.piercing_shot_count > 0:
                    log_event("asteroid_shot")
                    result = object.split()
                    if result == "split":
                        score += 1
                    elif result == "killed":
                        score += 5
                elif object.collides_with(shot):
                     log_event("asteroid_shot")
                     shot.kill()
                     result = object.split()
                     if result == "split":
                        score += 1
                     elif result == "killed":
                        score += 5
        for sprite in drawable:
            sprite.draw(screen)
        score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_surface, (10, 690))
        pygame.display.flip()
        dt = clock.tick(60) / 1000
        
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    while True:
        show_start_menu(screen)
        run_game(screen)

