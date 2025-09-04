# Alien-Shooter-Game
# 🚀 Space Wars!! (PyOpenGL + GLUT)

A classic top-down **alien shooter** rendered entirely with **PyOpenGL** and **GLUT**.  
No sprites or textures — every ship, bullet, and power-up is drawn with **custom line, circle, and semicircle rasterization** (Bresenham / midpoint algorithms) using `GL_POINTS`.

https://github.com/your-username/your-repo/assets/placeholder/demo.gif <!-- (optional) drop a GIF/screenshot here) -->

---

## ✨ What makes this project interesting

- **Pure OpenGL primitives**: lines & circles drawn via your own implementations, not convenience APIs.
- **Orthographic canvas**: `glOrtho(0, 800, 0, 600, -1, 1)` with a bottom-left origin.
- **UI drawn in OpenGL**: clickable **Restart**, **Pause/Play**, and **Quit** buttons at the top bar.
- **Dynamic difficulty**: enemy fall speed ramps with score; a pickup can slow them back down.
- **Power-ups & penalties** with distinct shapes:
  - ⭐ **Star** (shoot to gain points)
  - 🕸️ **Plus** (green “web”) → bigger bullets
  - 🕸️ **Minus** (red “web”) → smaller bullets
  - ➖ **Speed** (pink “minus”) → slows enemy fall
  - ❤️ **Love** (heart) → extra life

---

## 🕹️ Controls

**Keyboard**
- `← / → / ↑ / ↓` — Move the player ship
- `Space` — Shoot
- `y` / `p` / `o` / `i` — Change ship color (yellow / pink / orange / indigo-blue)

**Mouse (top bar buttons)**
- **Left cyan arrow** — Restart
- **Orange square** — Pause/Resume (toggles to a ► play icon)
- **Red X** — Quit

---

## 🎯 Gameplay Rules

- **Score**
  - +1 for shooting an alien ship
  - +100 for shooting a ⭐ **Star** (you *shoot* stars — you don’t collect them)
- **Lives**
  - Start with **3** lives (can grow up to **10** with ❤️ **Love**)
  - Lose **1** life if:
    - **5 enemies** pass the bottom (misses), **or**
    - **5 misfires/missed shots** occur  
      (missed bullets that leave the screen; also pressing non-`Space` keys while unpaused increases the misfire counter)
- **Difficulty**
  - Each alien kill slightly increases enemy fall speed (`sp += 0.01`)
  - Picking up **Speed** reduces it (`sp -= 0.1`)
- **Pickups (collide with the player unless noted)**
  - ⭐ **Star** — **shoot** it for +100 points
  - 🕸️ **Plus** (green) — increases bullet radius (up to +30)
  - 🕸️ **Minus** (red) — decreases bullet radius (down to −5)
  - ➖ **Speed** (pink) — slows alien fall speed
  - ❤️ **Love** (heart) — +1 life (max 10)

---

## 🔧 Install & Run

> You need **Python 3.8+**, **PyOpenGL**, and a **GLUT** implementation (e.g., **freeglut**).

### 1) Install Python dependencies
```bash
pip install PyOpenGL PyOpenGL_accelerate

