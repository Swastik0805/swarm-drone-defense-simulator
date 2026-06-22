import pygame
import math

class Drone:

    def __init__(self, x, y, name, color=(0, 0, 255)):
        self.angle = 0
        self.x = x
        self.y = y
        self.radius = 10
        self.color = color
        self.speed = 1
        self.direction = 1
        self.status = "PATROL"
        self.role = "PATROL"
        self.name = name
        self.radar_range = 150

    def draw(self, screen):
        if self.role == "INTERCEPT":
            self.color = (255, 0, 0)

        elif self.role == "TRACK":
            self.color = (255, 165, 0)

        elif self.role == "GUARD":
            self.color = (0, 255, 0)

        else:
            self.color = (0, 0, 255)

        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x), int(self.y)),
            self.radius
        )
        pygame.draw.circle(
        screen,
        (180, 180, 255),
        (int(self.x), int(self.y)),
        self.radar_range,
        1
        )

        font = pygame.font.SysFont(None, 24)

        text = font.render(
            
         f"{self.name} : {self.role}",
            True,
            (0,0,0)
        )
        screen.blit(
            text,
            (self.x + 15, self.y - 10)
        )

    def patrol_vertical(self):
        self.y += self.speed * self.direction

        if self.y >= 650:
            self.direction = -3

        if self.y <= 50:
            self.direction = 3

       
    def patrol_vertical_right(self):

        self.y += self.speed * self.direction

        if self.y >= 650:
            self.direction = -3

        if self.y <= 50:
            self.direction = 3
    
    def patrol_circle(self):

        center_x = 500
        center_y = 350

        orbit_radius = 200

        self.x = center_x + orbit_radius * math.cos(self.angle)
        self.y = center_y + orbit_radius * math.sin(self.angle)

        self.angle += 0.02

    def detect_intruder(self, intruder):

        distance = math.sqrt(
            (self.x - intruder.x)**2 +
            (self.y - intruder.y)**2
        ) 

        if distance <= 120:
           self.status = "TRACK"
           return True

        self.status = "PATROL"
        return False
    def distance_to_intruder(self, intruder):

        return math.sqrt(
            (self.x - intruder.x)**2 +
            (self.y - intruder.y)**2
        )
    
    def intercept(self, intruder):

        dx = intruder.x - self.x
        dy = intruder.y - self.y

        distance = math.sqrt(
            dx**2 + dy**2
        )

        if distance > 0:

            self.x += (dx / distance) * 3
            self.y += (dy / distance) * 3
    
    def capture_intruder(self, intruder):

        distance = math.sqrt(
            (self.x - intruder.x)**2 +
            (self.y - intruder.y)**2
        )

        if distance < 15:
            return True

        return False
    def track_intruder(self, intruder):

        dx = intruder.x - self.x
        dy = intruder.y - self.y

        distance = math.sqrt(
            dx**2 + dy**2
        )

        if distance > 100:

            self.x += (dx / distance) * 1.5
            self.y += (dy / distance) * 1.5
    def detect_with_radar(self, intruder):

        distance = (
        ((self.x - intruder.x) ** 2) +
        ((self.y - intruder.y) ** 2)
        ) ** 0.5

        return distance <= self.radar_range