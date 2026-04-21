import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable) # type: ignore
    Asteroid.containers = (asteroids, updatable, drawable) # type: ignore
    AsteroidField.containers = (updatable) # type: ignore
    Shot.containers = (shots, updatable, drawable) # type: ignore

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    clock = pygame.time.Clock()
    asteroid_field = AsteroidField()
    dt = 0

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                return
        
        screen.fill("black")

        for u in updatable:
            u.update(dt)
        
        for d in drawable:
            d.draw(screen)
        
        for a in asteroids:
            if player.collides_with(a):
                log_event("player_hit")
                print("Game over!")
                return
        
        for a in asteroids:
            for s in shots:
                if s.collides_with(a):
                    log_event("asteroid_shot")
                    a.split()
                    s.kill()
        
        pygame.display.flip()
        dt = clock.tick(FPS)/1000


if __name__ == "__main__":
    main()
