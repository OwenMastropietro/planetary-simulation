'''
Following along with Tech With Tim's tutorial on how to make a planetary orbit
simulation using pygame.
'''

import pygame
import math

pygame.init()


# Set up the drawing window
WIDTH, HEIGHT = 800, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

# Colors
WHITE = (255, 255, 255)
BLACk = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
DARK_GREY = (169, 169, 169)


class Planet:
    '''A planet class'''

    # Constants (todo: moveme)
    AU = 149600000000.0
    G = 6.67428e-11
    SCALE = 250 / AU
    TIMESTEP = 86400

    def __init__(self, x: int, y: int, radius: int, color: tuple, mass: int) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.x_velocity = 0
        self.y_velocity = 0
        self.is_sun = False
        self.distance_from_sun = 0
        self.orbit = []

    def draw(self, screen) -> None:
        '''Draws the planet'''

        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            scaled_points = []
            for point in self.orbit:
                x, y, = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                point = (x, y)
                scaled_points.append(point)

            pygame.draw.lines(surface=screen,
                              color=self.color,
                              closed=False,
                              points=scaled_points,
                              width=2)

        pygame.draw.circle(surface=screen,
                           color=self.color,
                           center=(x, y),
                           radius=self.radius)

    def attraction(self, other) -> tuple:
        '''
        Returns the force of attraction, in the x and y direction,
        between two planets.
        '''

        other_x, other_y = other.x, other.y
        distance_x, distance_y = other_x - self.x, other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.is_sun:
            self.distance_from_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)  # angle between planets
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y

    def update_position(self, planets: list):
        '''Updates the position of the planet.'''

        total_force_x, total_force_y = 0, 0

        for planet in planets:
            if self == planet:
                continue

            force_x, force_y = self.attraction(planet)
            total_force_x += force_x
            total_force_y += force_y

        self.x_velocity += total_force_x / self.mass * self.TIMESTEP
        self.y_velocity += total_force_y / self.mass * self.TIMESTEP

        self.x += self.x_velocity * self.TIMESTEP
        self.y += self.y_velocity * self.TIMESTEP

        self.orbit.append((self.x, self.y))


def main() -> None:
    '''Le Main'''

    # Create the planets (todo: change-radius, change-x, change-mass)
    sun = Planet(x=0, y=0, radius=30, color=YELLOW, mass=1.98892e30)
    sun.is_sun = True

    earth = Planet(x=-Planet.AU, y=0, radius=16, color=BLUE, mass=5.9742e24)
    earth.y_velocity = 29.783 * 1000  # todo: what does NASA say?

    mars = Planet(x=-1.524 * Planet.AU, y=0,
                  radius=12, color=RED, mass=6.39e23)
    mars.y_velocity = 24.077 * 1000  # todo: what does NASA say?

    mercury = Planet(x=0.387 * Planet.AU, y=0, radius=8,
                     color=DARK_GREY, mass=3.30e23)
    mercury.y_velocity = -47.4 * 1000  # todo: what does NASA say?

    venus = Planet(x=0.723 * Planet.AU, y=0, radius=14,
                   color=WHITE, mass=4.8685e24)
    venus.y_velocity = -35.02 * 1000  # todo: what does NASA say?

    planets = [sun, earth, mars, mercury, venus]

    # Run until the user asks to quit
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(60)
        SCREEN.fill(color=BLACk)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(SCREEN)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
