import pygame
import random

class Intruder:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.radius = 10

        # Intruder Type
        self.intruder_type = random.choice([
            "MISSILE",
            "VEHICLE",
            "DRONE"
        ])

        # Threat Level
        if self.intruder_type == "MISSILE":
            self.threat = 8
            self.color = (255, 0, 0)

        elif self.intruder_type == "VEHICLE":
            self.threat = 3
            self.color = (255, 165, 0)

        else:
            self.threat = 6
            self.color = (255, 0, 255)

        # Random Speed
        self.speed = random.choice([
            0.8,
            1.2,
            1.8
        ])

        # Legacy movement values (kept for compatibility)
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])

    def move(self):

        self.x += self.dx
        self.y += self.dy

        if self.x <= 0 or self.x >= 1000:
            self.dx *= -1

        if self.y <= 0 or self.y >= 700:
            self.dy *= -1

    def move_towards_base(self, base_x, base_y):

        dx = base_x - self.x
        dy = base_y - self.y

        distance = (dx**2 + dy**2) ** 0.5

        if distance > 0:

            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

    def draw(self, screen):

        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x), int(self.y)),
            self.radius
        )

        # Show Type Label
        font = pygame.font.SysFont(None, 18)

        text = font.render(
            self.intruder_type,
            True,
            (0, 0, 0)
        )

        screen.blit(
            text,
            (self.x + 12, self.y - 10)
        )

    def respawn(self):

        self.x = random.randint(50, 950)
        self.y = random.randint(50, 650)

        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])

        # New Intruder Type
        self.intruder_type = random.choice([
            "MISSILE",
            "VEHICLE",
            "DRONE"
        ])

        if self.intruder_type == "MISSILE":
            self.threat = 8
            self.color = (255, 0, 0)

        elif self.intruder_type == "VEHICLE":
            self.threat = 3
            self.color = (255, 165, 0)

        else:
            self.threat = 6
            self.color = (255, 0, 255)

        self.speed = random.choice([
            0.8,
            1.2,
            1.8
        ])
    def get_threat_score(self, base_x, base_y):

        distance_to_base = (
            ((self.x - base_x) ** 2) +
            ((self.y - base_y) ** 2)
        ) ** 0.5

        distance_score = max(
            0,
            100 - distance_to_base
        )

        return (
            self.threat * 20
            + self.speed * 10
            + distance_score
        )