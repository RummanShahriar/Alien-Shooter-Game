# 🚀 Space Wars!! (Alien Shooter Game with PyOpenGL + GLUT)

A **classic top-down alien shooter** built entirely with **PyOpenGL** and **GLUT**.  
Every element — ships, bullets, power-ups — is drawn using **custom rasterization algorithms** (Bresenham’s line, midpoint circle, semicircle), rendered as `GL_POINTS`.  
No sprites. No textures. Just pure OpenGL primitives. 🎨

---

## 📖 Table of Contents
1. [Overview](#-overview)
2. [Features](#-features)
3. [Controls](#-controls)
4. [Gameplay Rules](#-gameplay-rules)
5. [Installation & Setup](#-installation--setup)
6. [Code Highlights](#-code-highlights)
7. [Customization](#-customization)
8. [License](#-license)
9. [Credits](#-credits)

---

## 🔭 Overview

**Space Wars!!** is a 2D alien shooter game where you:
- Control a player ship at the bottom of the screen.
- Shoot falling alien ships to score points.
- Collect or avoid power-ups that affect gameplay.
- Manage lives and survive as long as possible while the difficulty increases.

The game uses:
- **Orthographic projection**: `glOrtho(0, 800, 0, 600, -1, 1)`
- **Custom rasterization**: Line and circle algorithms
- **GLUT event loop** for rendering, input handling, and timers.

---

## ✨ Features

- 🛠 **Pure OpenGL Primitives**  
  No external images or sprites — everything is algorithmically drawn.

- 🖥 **Custom UI Buttons**  
  Restart ⟳, Pause/Play ⏯, and Quit ❌ buttons drawn directly in OpenGL.

- 🎮 **Dynamic Difficulty**  
  Enemy fall speed increases with score; slowed down by collecting speed power-ups.

- 💡 **Power-Ups & Penalties**
  - ⭐ **Star** → shoot for +100 points  
  - 🟢 **Plus** → increases bullet size  
  - 🔴 **Minus** → decreases bullet size  
  - 🩷 **Speed** → slows down falling enemies  
  - ❤️ **Love** → grants extra life  

---

## 🎮 Controls

### Keyboard
| Key        | Action                         |
|------------|--------------------------------|
| `← → ↑ ↓` | Move the player ship            |
| `Space`    | Shoot bullet                   |
| `y`        | Change ship color → Yellow     |
| `p`        | Change ship color → Pink       |
| `o`        | Change ship color → Orange     |
| `i`        | Change ship color → Indigo-Blue|

### Mouse (Top Bar UI)
| Button              | Action   |
|---------------------|----------|
| **Cyan Arrow** ⟳   | Restart  |
| **Orange Square** ⏯ | Pause/Resume |
| **Red X** ❌       | Quit     |

---

## 🎯 Gameplay Rules

- **Scoring**
  - +1 point → Shooting an alien ship  
  - +100 points → Shooting a ⭐ Star  

- **Lives**
  - Start with **3 lives**  
  - Max lives = **10** (collect ❤️ Love to increase)  
  - Lose 1 life if:
    - 5 enemies reach the bottom, **or**  
    - 5 misfires (missed bullets or pressing invalid keys while unpaused)  

- **Difficulty**
  - Enemy fall speed increases (`sp += 0.01`) with each alien kill  
  - Collecting a Speed power-up reduces speed (`sp -= 0.1`)  

---

## 🔧 Installation & Setup

### Requirements
- Python **3.8+**
- [PyOpenGL](https://pypi.org/project/PyOpenGL/)  
- [PyOpenGL_accelerate](https://pypi.org/project/PyOpenGL-accelerate/)  
- GLUT implementation (e.g., **freeglut**)

### Install Python Dependencies
```bash
pip install PyOpenGL PyOpenGL_accelerate
