import pygame
import sys
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, LINE_WIDTH
from logger import log_state
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from logger import log_event
from circleshape import CircleShape
from shot import Shot
from small_shot import SmallShot
from canonball import Canonball
from shield_buff import ShieldBuff
from piercing_shots import PiercingShot
from knockback_wave import Knockback_Wave

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
    canonballs = pygame.sprite.Group()
    small_shots = pygame.sprite.Group()
    ShieldBuffs = pygame.sprite.Group()
    PiercingShots = pygame.sprite.Group()
    knockback_waves = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, drawable, updatable)
    Canonball.containers = (canonballs, drawable, updatable)
    SmallShot.containers = (small_shots, drawable, updatable)
    ShieldBuff.containers = (ShieldBuffs,drawable, updatable)
    PiercingShot.containers = (PiercingShots, drawable, updatable)
    Knockback_Wave.containers = (knockback_waves, drawable, updatable)

    clock = pygame.time.Clock()

    dt = 0

    player = Player( SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    asteroid_field = AsteroidField()

    score = 0

    

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        screen.fill("black")

        updatable.update(dt)

        for wave in knockback_waves:
            for asteroid in asteroids:
                if wave.collides_with(asteroid):
                    offset = asteroid.position - wave.position
                    distance = offset.length()

                    if distance == 0:
                        direction = pygame.Vector2(1, 0)
                    else:
                        direction = offset / distance   # same as normalize()

            # assume your wave has a radius attribute
                        max_radius = wave.radius

            # factor goes from 1.0 at center -> 0.0 at edge
                        falloff = max(0, 1 - distance / max_radius)

                        base_strength = 600
                        knockback_strength = base_strength * falloff

                        asteroid.velocity += direction * knockback_strength


        for shieldbuff in ShieldBuffs:
            if shieldbuff.collides_with(player):
                shieldbuff.kill()
                log_event("shield_gained")
                player.shield_state = True
                player.color = "blue"

        for piercingshot in PiercingShots:
            if piercingshot.collides_with(player) and player.weapon != player.double_shot:
                log_event("piercing_shots_gained")
                piercingshot.kill()
                player.piercing_shot_count += 10
            if piercingshot.collides_with(player) and player.weapon == player.double_shot:
                log_event("piercing_shots_gained")
                piercingshot.kill()
                player.piercing_shot_count += 20

        for object in asteroids:
            if object.collides_with(player) and player.shield_state == True:
                log_event("player_hit, shiled_lost")
                object.kill()
                player.shield_state = False
                player.color = "pink"
            elif object.collides_with(player) and player.shield_state == False:
                 log_event("player_hit")
                 score = 0
                 return
            
        for object in asteroids:
            for shot in shots:
                if object.collides_with(shot) and player.piercing_shot_count > 0:
                    log_event("asteroid_shot")
                    result = object.split(player)
                    if result == "split":
                        score += 1
                    elif result == "killed":
                        score += 5
                        if player.knockback_charge < 100:
                            player.knockback_charge += 4
                elif object.collides_with(shot):
                    log_event("asteroid_shot")
                    shot.kill()
                    result = object.split(player)
                    if result == "split":
                        score += 1
                    elif result == "killed":
                        score += 5
                        if player.knockback_charge < 100:
                            player.knockback_charge += 4
            
            for canonball in canonballs:
                if object.collides_with(canonball) and player.piercing_shot_count > 0:
                    log_event("asteroid_canon_shot")
                    result = object.split(player)
                    if result == "split":
                        score += 1
                    elif result == "killed":
                        score += 5
                        if player.knockback_charge < 100:
                            player.knockback_charge += 10
                elif object.collides_with(canonball):
                    log_event("asteroid_canon_shot")
                    canonball.kill()
                    result = object.split(player)
                    if result == "split":
                        score += 1
                    elif result == "killed":
                        score += 5
                        if player.knockback_charge < 100:
                            player.knockback_charge += 10

            for smallshot in small_shots:
                if object.collides_with(smallshot) and player.piercing_shot_count > 0:
                    log_event("asteroid_small_shot")
                    result = object.split(player)
                    if result == "split":
                        score += 1
                    elif result == "killed":
                        score += 5
                        if player.knockback_charge < 100:
                            player.knockback_charge += 4
                elif object.collides_with(smallshot):
                    log_event("asteroid_small_shot")
                    smallshot.kill()
                    result = object.split(player)
                    if result == "split":
                        score += 1
                    elif result == "killed":
                        score += 5
                        if player.knockback_charge < 100:
                            player.knockback_charge += 4

        for sprite in drawable:
            sprite.draw(screen)

        if player.knockback_charge >= 100:  
            pygame.draw.circle( screen, "purple", (int(player.position.x), int(player.position.y)), player.radius + 10, LINE_WIDTH )

        shots_surface = font.render(f"piercing shots: {player.piercing_shot_count}", True, (255, 255, 255))
        screen.blit(shots_surface, (10, 690))

        score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_surface, (10, 650))

        pulse_wave_surface = font.render(f"pulse wave: {player.knockback_charge}%" ,True,(255, 255, 255))
        screen.blit(pulse_wave_surface, (10, 670))

        pygame.display.flip()

        dt = clock.tick(60) / 1000
        
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    while True:
        show_start_menu(screen)
        run_game(screen)

