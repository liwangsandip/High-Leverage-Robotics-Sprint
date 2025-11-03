#  🚀 21-Day High-Leverage Robotics Sprint

**Goal:** To build the most convincing proof-of-concept portfolio in the shortest time (21 days). We prioritize output over understanding, and demonstration over depth, using ROS 2, Gazebo, and AI tools.
 
---

## ✅ Phase 1: Foundation & Setup (Days 1-3) - COMPLETE

**Achievement:** Successfully installed the full ROS 2 Humble Docker environment and executed the full SLAM pipeline.

**Tangible Proof:** The generated map files are committed below, ready for Navigation2.

| File | Size | Purpose |
| :--- | :--- | :--- |
| [maps/turtlebot3_house_map.pgm](maps/turtlebot3_house_map.pgm) | 243 KB | The Occupancy Grid (Black/White Map Image) |
| [maps/turtlebot3_house_map.yaml](maps/turtlebot3_house_map.yaml) | 2.05 KB | Map Metadata (Resolution, Origin) |

---

## 🎯 Phase 2: Project 1 - "The Autonomous Square" (Days 4-7)

**Goal:** A robot that moves in a square pattern while actively avoiding obstacles using laser sensor data.

| Day | Task | High-Leverage Shortcut & Tool | Status |
| :--- | :--- | :--- | :--- |
| 4 | Create a "Square" Node | DO NOT write from scratch. Integrate and modify an existing ROS 2 Python node. Use AI (ChatGPT/Cursor) to explain logic line-by-line. | COMPLETE |
| 5 | Integrate Laser Data | Find a tutorial on reading laser scan data. Goal: print the distance to the nearest obstacle. | COMPLETE |
| 6 | Fuse Logic | Modify the square node with simple `if/else` logic: `if min_range < 0.5: stop(); else: continue_square()`. | IN PROGRESS |
| 7 | Polish & Record | Record a 30-second video demo (code, simulation, obstacle stop). Update README with video link. | PENDING |

---

## 👁️ Phase 3: Project 2 - "The Seeing Sentinel" (Days 8-14)

**Goal:** Add a camera and implement object detection without training a custom model.

---

## 🌉 Phase 4: Project 3 - "The Physical Bridge" (Days 15-21)

**Goal:** Port the AI object detection code onto a physical, pre-assembled robot (e.g., TurtleBot3 Burger) for final deployment proof.

---
