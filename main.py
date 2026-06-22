import pygame
from constants import *
from drone import Drone
from intruder import Intruder
from ml_predictor import predict_threat
import csv
import os
from radar import Radar
radar = Radar(500, 350)

# -----------------------------
# ML Threat Priority
# -----------------------------
threat_priority = {
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3,
    "CRITICAL": 4
}

# -----------------------------
# Variables
# -----------------------------
capture_count = 0
capture_cooldown = 0
base_health = 100

threat_log = []
heatmap_points = []

# -----------------------------
# Pygame Setup
# -----------------------------
pygame.init()

hud_font = pygame.font.SysFont(None, 22)

clock = pygame.time.Clock()

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "Swarm Drone Defense Simulator"
)

# -----------------------------
# Dataset File
# -----------------------------
if not os.path.exists(
    "threat_dataset.csv"
):

    with open(
        "threat_dataset.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Type",
            "Speed",
            "DistanceToBase",
            "ThreatScore"
        ])

# -----------------------------
# Drones
# -----------------------------
drone1 = Drone(100, 100, "D1")
drone2 = Drone(900, 100, "D2")
drone3 = Drone(500, 600, "D3")

# -----------------------------
# Intruders
# -----------------------------
intruders = [
    Intruder(800, 500),
    Intruder(200, 400),
    Intruder(700, 200)
]

running = True

# =============================
# MAIN LOOP
# =============================
while running:

    # -------------------------
    # Events
    # -------------------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # -------------------------
    # Patrol Behaviors
    # -------------------------
    drone1.patrol_vertical()
    drone2.patrol_vertical_right()
    drone3.patrol_circle()

    # -------------------------
    # Base
    # -------------------------
    base_x = 500
    base_y = 350

    # -------------------------
    # Move Intruders
    # -------------------------
    for intruder in intruders:

        intruder.move_towards_base(
            base_x,
            base_y
        )

        distance_to_base = (
            ((intruder.x - base_x) ** 2)
            +
            ((intruder.y - base_y) ** 2)
        ) ** 0.5

        if distance_to_base < 60:

            base_health -= 1

            intruder.respawn()

    # -------------------------
    # Mission Failure
    # -------------------------
    if base_health <= 0:

        print("MISSION FAILED")

        running = False

    # -------------------------
    # AI Target Selection
    # -------------------------

    detected_intruders = radar.detect_intruders(
        intruders
    )

    if len(detected_intruders) > 0:

        target_intruder = max(
            detected_intruders,
            key=lambda intruder:
            threat_priority.get(
                predict_threat(
                    intruder,
                    base_x,
                    base_y
                )[0],
                0
            )
        )

        predicted_threat, confidence = predict_threat(
            target_intruder,
            base_x,
            base_y
        )

        sorted_intruders = sorted(
            detected_intruders,
            key=lambda intruder:
            intruder.get_threat_score(
                base_x,
                base_y
            ),
            reverse=True
        )

    else:

        target_intruder = None
        predicted_threat = "NONE"
        confidence = 0

        sorted_intruders = []

    # -------------------------
    # Drone Assignments
    # -------------------------
    assignments = {}
    drones = [
        drone1,
        drone2,
        drone3
    ]

    available_drones = drones.copy()

    sorted_intruders = sorted(
        detected_intruders,
        key=lambda intruder:
        intruder.get_threat_score(
            base_x,
            base_y
        ),
        reverse=True
    )

    for intruder in sorted_intruders:

        if len(available_drones) == 0:
            break

        closest_drone = min(
            available_drones,
            key=lambda drone:
            drone.distance_to_intruder(
                intruder
            )
        )

        assignments[closest_drone] = intruder

        available_drones.remove(
            closest_drone
        )

        # -------------------------
        # Dataset Logging
        # -------------------------
    if target_intruder:

            distance_to_base = (
                ((target_intruder.x - base_x) ** 2)
                +
                ((target_intruder.y - base_y) ** 2)
            ) ** 0.5

            threat_score = (
                target_intruder.get_threat_score(
                    base_x,
                    base_y
                )
            )

            with open(
                "threat_dataset.csv",
                "a",
                newline=""
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    target_intruder.intruder_type,
                    target_intruder.speed,
                    round(distance_to_base, 2),
                    round(threat_score, 2)
                ])

    else:

            threat_score = 0

    # -------------------------
    # Swarm Assignment
    # -------------------------
    if target_intruder:

        d1_distance = drone1.distance_to_intruder(
            target_intruder
        )

        d2_distance = drone2.distance_to_intruder(
            target_intruder
        )

        d3_distance = drone3.distance_to_intruder(
            target_intruder
        )

        distances = [
            (drone1, d1_distance),
            (drone2, d2_distance),
            (drone3, d3_distance)
        ]

        distances.sort(
            key=lambda x: x[1]
        )

    else:

     distances = []
    print("\nCONTACTS:", len(detected_intruders))

    for drone, target in assignments.items():

        print(
            drone.name,
            "->",
            target.intruder_type
        )

    # -------------------------
    # Drone Roles
    # -------------------------

    # -------------------------
    # Drone Roles
    # -------------------------

    for drone in drones:

        if drone in assignments:

            drone.role = "INTERCEPT"

        else:

            drone.role = "STANDBY"

    # -------------------------
    # Execute Roles
    # -------------------------

    for drone in drones:

        if drone in assignments:

            target = assignments[drone]

            drone.intercept(target)

     # -------------------------
    # Capture Logic
    # -------------------------
    if capture_cooldown > 0:
        capture_cooldown -= 1

    if capture_cooldown == 0:

        for drone in drones:

            for intruder in intruders:

                if drone.capture_intruder(intruder):

                    heatmap_points.append(
                        (
                            int(intruder.x),
                            int(intruder.y)
                        )
                    )

                    threat_log.append(
                        intruder.intruder_type
                    )

                    if len(threat_log) > 5:
                        threat_log.pop(0)

                    print(
                        f"{intruder.intruder_type} CAPTURED BY {drone.name}"
                    )

                    capture_count += 1

                    intruder.respawn()

                    capture_cooldown = 60

                    break

            if capture_cooldown > 0:
                break

    # -------------------------
    # Mission Status
    # -------------------------
    if base_health > 50:

        mission_status = "SECURE"

    elif base_health > 20:

        mission_status = "WARNING"

    else:

        mission_status = "CRITICAL"

    # =========================
    # DRAWING
    # =========================
    screen.fill(WHITE)

    # Base Color
    if base_health > 70:
        base_color = (0, 255, 0)

    elif base_health > 30:
        base_color = (255, 255, 0)

    else:
        base_color = (255, 0, 0)

    pygame.draw.rect(
        screen,
        base_color,
        (450, 300, 100, 100)
    )

    #Radar Visualization
    pygame.draw.circle(
        screen,
       (0, 255, 255),
       (500, 350),
       radar.range,
       2
    )

    # Danger Zone
    pygame.draw.circle(
        screen,
        (255, 0, 0),
        (500, 350),
        60,
        2
    )

    # Heatmap
    for point in heatmap_points:

        pygame.draw.circle(
            screen,
            (255, 100, 100),
            point,
            5
        )

    # Drones
    drone1.draw(screen)
    drone2.draw(screen)
    drone3.draw(screen)

    # Intruders
    for intruder in intruders:
        intruder.draw(screen)

    # Target Ring
    if target_intruder:

       pygame.draw.circle(
        screen,
        (255, 255, 0),
        (
            int(target_intruder.x),
            int(target_intruder.y)
        ),
        20,
        2
    )

    # HUD
    hud_lines = [
        "SWARM STATUS",
        f"STATUS: {mission_status}",
        f"BASE HP: {base_health}",
        f"CAP: {capture_count}",
        f"CONTACTS: {len(detected_intruders)}",
        f"D1: {drone1.role}",
        f"D2: {drone2.role}",
        f"D3: {drone3.role}",
        f"TARGET: {target_intruder.intruder_type if target_intruder else 'NONE'}",
        f"THREAT: {target_intruder.threat if target_intruder else '-'}",
        f"SCORE: {int(threat_score) if target_intruder else 0}",
        f"AI: {predicted_threat}",
        f"CONF: {confidence:.1f}%",
        "-----",
        "RECENT THREATS"
    ]
    for threat in threat_log:
        hud_lines.append(threat)

    hud_lines.append("-----")
    hud_lines.append("ASSIGNMENTS")

    for drone, target in assignments.items():

        hud_lines.append(
            f"{drone.name}->{target.intruder_type}"
        )

    for i, line in enumerate(
        hud_lines
    ):

        text = hud_font.render(
            line,
            True,
            BLACK
        )

        screen.blit(
            text,
            (760, 15 + i * 22)
        )
    pygame.display.update()

    clock.tick(60)

pygame.quit()