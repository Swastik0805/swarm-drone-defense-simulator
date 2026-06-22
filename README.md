# Swarm Drone Defense Simulator

An AI-powered swarm defense simulation developed using Python, Pygame, and Machine Learning.

## Simulation Preview

![Swarm Simulator](screenshots/swarm_simulator.png)

---

## Features

- Central Radar Detection System
- Autonomous Drone Swarm Coordination
- Machine Learning Threat Classification
- Dynamic Threat Prioritization
- Multi-Target Assignment Engine
- Real-Time Interception
- Base Defense Monitoring
- Threat Logging & Heatmap Visualization

---

## System Architecture

```text
Intruders Spawn
       ↓
Central Radar Detects
       ↓
ML Threat Classification
       ↓
Threat Prioritization
       ↓
Drone Assignment Engine
       ↓
Interception / Tracking
       ↓
Capture & Threat Logging
```

---

## Project Structure

```text
swarm-drone-defense-simulator/
│
├── main.py              # Main simulation loop
├── drone.py             # Drone behavior and swarm logic
├── intruder.py          # Intruder generation and movement
├── radar.py             # Central radar detection system
├── ml_predictor.py      # ML threat classification
├── train_model.py       # Model training script
├── constants.py         # Global constants
│
├── screenshots/
│   └── swarm_simulator.png
│
├── README.md
└── LICENSE
```

---

## Technologies Used

- Python
- Pygame
- Scikit-Learn
- Pandas
- Joblib
- Git
- GitHub

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Swastik0805/swarm-drone-defense-simulator.git
cd swarm-drone-defense-simulator
```

Install dependencies:

```bash
pip install pygame pandas scikit-learn joblib
```

Train the model:

```bash
python train_model.py
```

Run the simulator:

```bash
python main.py
```

---

## Current Capabilities

- Multi-drone autonomous defense
- Real-time target assignment
- Centralized radar-based detection
- Machine learning threat evaluation
- Dynamic swarm coordination
- Capture and respawn simulation
- Threat scoring and prioritization
- Base defense monitoring

---

## Sample Features Demonstrated

```text
✓ Centralized Radar Architecture
✓ Multi-Drone Coordination
✓ Dynamic Target Assignment
✓ Threat Scoring
✓ Machine Learning Classification
✓ Real-Time Interception
✓ Base Defense Simulation
✓ Threat Heatmap Logging
```

---

## Skills Demonstrated

- Python Programming
- Object-Oriented Design
- Machine Learning
- Swarm Intelligence
- Autonomous Systems
- Simulation Development
- Real-Time Decision Making
- Defense System Architecture

---

## Future Enhancements

- [ ] Computer Vision Based Target Recognition (YOLO)
- [ ] Human / Vehicle / Drone Classification
- [ ] Predictive Interception Algorithms
- [ ] Multi-Radar Network
- [ ] Drone Formation Control
- [ ] Pixhawk Integration
- [ ] Real-Time Telemetry Dashboard
- [ ] Raspberry Pi Deployment
- [ ] Autonomous Mission Planning

---

## Author

**Swastik Singh**

B.Tech Electronics and Communication Engineering  
PSIT Kanpur

---

## Version

**v1.0 - Centralized AI Swarm Defense System**
