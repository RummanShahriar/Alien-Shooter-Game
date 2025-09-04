from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import math
import random

life = 3
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
MAX_RADIUS = 30
MIN_RADIUS = 10
SHIP_WIDTH = 40
SHIP_HEIGHT = 60
BULLET_RADIUS = 5
b_size_plus = 0
sp = 0
MAX_MISS_COUNT = 5
MAX_MISFIRE_COUNT = 5
MAX_FALLING_SHIPS = 3
SHIP_GENERATION_DELAY = 1000  
cl = "y"
paused = False  

def drawPixel(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def draw8way(x, y, zone):
    if zone == 0:
        drawPixel(x, y)
    elif zone == 1:
        drawPixel(y, x)
    elif zone == 2:
        drawPixel(-y, x)
    elif zone == 3:
        drawPixel(-x, y)
    elif zone == 4:
        drawPixel(-x, -y)
    elif zone == 5:
        drawPixel(-y, -x)
    elif zone == 6:
        drawPixel(y, -x)
    elif zone == 7:
        drawPixel(x, -y)

def drawLine_0(x0, y0, x1, y1, zone):
    dx = x1 - x0
    dy = y1 - y0
    delE = 2 * dy
    delNE = 2 * (dy - dx)
    d = 2 * dy - dx
    x = x0
    y = y0
    while x < x1:
        draw8way(x, y, zone)
        if d < 0:
            d += delE
            x += 1
        else:
            d += delNE
            x += 1
            y += 1

def drawLine(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    if abs(dx) >= abs(dy): 
        if dx >= 0:
            if dy >= 0:
                drawLine_0(x0, y0, x1, y1, 0)
            else:
                drawLine_0(x0, -y0, x1, -y1, 7)
        else:
            if dy >= 0:
                drawLine_0(-x0, y0, -x1, y1, 3)
            else:
                drawLine_0(-x0, -y0, -x1, -y1, 4)
    else:  
        if dx >= 0:
            if dy >= 0:
                drawLine_0(y0, x0, y1, x1, 1)
            else:
                drawLine_0(-y0, x0, -y1, x1, 6)
        else:
            if dy >= 0:
                drawLine_0(y0, -x0, y1, -x1, 2)
            else:
                drawLine_0(-y0, -x0, -y1, -x1, 5)

def drawSemiCircle(x, y, radius):
    def draw8way(x, y, zone):
        if zone == 0:
            drawPixel(x, y)
        elif zone == 1:
            drawPixel(y, x)
        elif zone == 2:
            drawPixel(-y, x)
        elif zone == 3:
            drawPixel(-x, y)
        elif zone == 4:
            drawPixel(-x, -y)
        elif zone == 5:
            drawPixel(-y, -x)
        elif zone == 6:
            drawPixel(y, -x)
        elif zone == 7:
            drawPixel(x, -y)

    def drawPixel(x, y):
        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glEnd()

    x_center = x
    y_center = y
    r = radius

    x = r
    y = 0

    P = 1 - r

    while x > y:
        y += 1
        
        if P <= 0: 
            P = P + 2 * y + 1
  
        else:		 
            x -= 1
            P = P + 2 * y - 2 * x + 1
         
        if x < y:
            break
            
        draw8way(x + x_center, y + y_center, 0)
        draw8way(-x + x_center, y + y_center, 0)
            
        if x != y:
            draw8way(y + x_center, x + y_center, 0)
            draw8way(-y + x_center, x + y_center, 0)
 

def drawCircle(x, y, radius):
    def draw8way(x, y, zone):
        if zone == 0:
            drawPixel(x, y)
        elif zone == 1:
            drawPixel(y, x)
        elif zone == 2:
            drawPixel(-y, x)
        elif zone == 3:
            drawPixel(-x, y)
        elif zone == 4:
            drawPixel(-x, -y)
        elif zone == 5:
            drawPixel(-y, -x)
        elif zone == 6:
            drawPixel(y, -x)
        elif zone == 7:
            drawPixel(x, -y)

    def drawPixel(x, y):
        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glEnd()

    x_center = x
    y_center = y
    r = radius

    x = r
    y = 0

    P = 1 - r

    while x > y:
        y += 1
        
        if P <= 0: 
            P = P + 2 * y + 1
  
        else:		 
            x -= 1
            P = P + 2 * y - 2 * x + 1
         
        if x < y:
            break
            
        draw8way(x + x_center, y + y_center, 0)
        draw8way(-x + x_center, y + y_center, 0)
        draw8way(x + x_center, -y + y_center, 0)
        draw8way(-x + x_center, -y + y_center, 0)
            
        if x != y:
            draw8way(y + x_center, x + y_center, 0)
            draw8way(-y + x_center, x + y_center, 0)
            draw8way(y + x_center, -x + y_center, 0)
            draw8way(-y + x_center, -x + y_center, 0)


class Ship :
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self,a):
        if a == 1 : #Player
            drawLine(self.x - self.width / 2, self.y, self.x + self.width / 2, self.y)  
            drawLine(self.x - self.width / 4, self.y, self.x - self.width / 4, self.y + self.height)  
            drawLine(self.x + self.width / 4, self.y, self.x + self.width / 4, self.y + self.height) 

            #wings
            drawLine(self.x - self.width / 2, self.y,self.x, self.y + self.height / 2)
            drawLine(self.x + self.width / 2, self.y, self.x, self.y + self.height / 2)
            drawLine(self.x - self.width / 2, self.y, self.x, self.y - self.height / 2)  
            drawLine(self.x + self.width / 2, self.y, self.x, self.y - self.height / 2)  

            #Cockpit
            drawLine(self.x - self.width / 8, self.y, self.x + self.width / 8, self.y)  
            drawLine(self.x - self.width / 8, self.y, self.x - self.width / 8, self.y - self.height / 8) 
            drawLine(self.x + self.width / 8, self.y, self.x + self.width / 8, self.y - self.height / 8) 
            #Cockpit 2.0
            drawLine(self.x - self.width / 8, self.y + self.height / 4, self.x + self.width / 8, self.y + self.height / 4) 
            drawLine(self.x - self.width / 8, self.y + self.height / 4, self.x - self.width / 6, self.y + self.height / 3)  
            drawLine(self.x + self.width / 8, self.y + self.height / 4, self.x + self.width / 6, self.y + self.height / 3)  
        
        
        elif a == 2 : #aliens
            drawLine(self.x - self.width / 2, self.y + self.height / 2, self.x + self.width / 2, self.y + self.height / 2)  
            drawLine(self.x - self.width / 2, self.y + self.height / 2, self.x, self.y - self.height / 2)  
            drawLine(self.x, self.y - self.height / 2, self.x + self.width / 2, self.y + self.height / 2)  
            drawCircle(self.x, self.y,5)
            drawCircle(self.x,self.y,8)
            drawSemiCircle(self.x+9,self.y+30,4)
            drawSemiCircle(self.x-9,self.y+30,4)

            #Cockpit
            drawLine(self.x - self.width / 4, self.y + self.height / 2, self.x + self.width / 4, self.y + self.height / 2)  
            drawLine(self.x - self.width / 4, self.y + self.height / 2, self.x, self.y + self.height / 3) 
            drawLine(self.x, self.y + self.height / 3, self.x + self.width / 4, self.y + self.height / 2)             

def generate_falling_ship():
    return Ship(random.randint(SHIP_WIDTH // 2, WINDOW_WIDTH - SHIP_WIDTH // 2), WINDOW_HEIGHT, SHIP_WIDTH, SHIP_HEIGHT)

shooter = Ship(WINDOW_WIDTH // 2, SHIP_HEIGHT // 2, SHIP_WIDTH, SHIP_HEIGHT)
projectiles = []  
falling_ships = []

falling_powers = []    #star ... 100x points 
falling_power_timer = 0

falling_speed = []   #minus look alike shape
falling_speed_timer = 0

falling_love = []   #life
falling_love_timer = 0

falling_plus = []    #ball size plus
falling_plus_timer = 0

falling_minus = []   #ball size minus
falling_minus_timer = 0

falling_ship_timer = 0
game_over = False 
score = 0
miss_count = 0
misfire_count = 0

class Power:  # star shape
    def __init__(self, x, y, size):
        self.x = x
        self.y = y+15
        self.size = size
        self.radius = size

    def draw(self):
        half_size = self.size // 2

        drawLine(self.x, self.y - half_size, self.x + half_size, self.y)  
        drawLine(self.x + half_size, self.y, self.x, self.y + half_size)  
        drawLine(self.x, self.y + half_size, self.x - half_size, self.y)  
        drawLine(self.x - half_size, self.y, self.x, self.y - half_size)  

        gun_size = self.size // 4
        drawLine(self.x - half_size, self.y, self.x - half_size - gun_size, self.y)  
        drawLine(self.x + half_size, self.y, self.x + half_size + gun_size, self.y)  
        drawLine(self.x, self.y - half_size, self.x, self.y - half_size - gun_size) 
        drawLine(self.x, self.y + half_size, self.x, self.y + half_size + gun_size) 


def generate_falling_power():
    return Power(random.randint(MAX_RADIUS, WINDOW_WIDTH - MAX_RADIUS), WINDOW_HEIGHT, random.randint(MIN_RADIUS, MAX_RADIUS))

class Plus: # spider web (green)
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self):
        x = self.radius
        y = 0
       
        draw8way(x + self.x, y + self.y, 0)
       
        if self.radius > 0:
            draw8way(x + self.x, -y + self.y, 0)
            draw8way(y + self.x, x + self.y, 0)
            draw8way(-y + self.x, x + self.y, 0)
       
        P = 1 - self.radius 
        while x > y:
            y += 1
        
            if P <= 0: 
                P = P + 2 * y + 1
  
            else:		 
                x -= 1
                P = P + 2 * y - 2 * x + 1
         
            if x < y:
                break
            
            draw8way(x + self.x, y + self.y, 0)

            draw8way(-x + self.x, y + self.y, 0)

            draw8way(x + self.x, -y + self.y, 0)
            draw8way(-x + self.x, -y + self.y, 0)
            drawCircle(self.x,self.y,13)

            drawCircle(self.x,self.y,8)

            drawCircle(self.x,self.y,5)
            if x != y:
                draw8way(y + self.x, x + self.y, 0)
                draw8way(-y + self.x, x + self.y, 0)
                draw8way(y + self.x, -x + self.y, 0)
                draw8way(-y + self.x, -x + self.y, 0)

class Minus:  #spider web (red)
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self):
        x = self.radius
        y = 0
       
        draw8way(x + self.x, y + self.y, 0)
       
        if self.radius > 0:
            draw8way(x + self.x, -y + self.y, 0)
            draw8way(y + self.x, x + self.y, 0)
            draw8way(-y + self.x, x + self.y, 0)
       
        P = 1 - self.radius 
        while x > y:
            y += 1
        
            if P <= 0: 
                P = P + 2 * y + 1
  
            else:		 
                x -= 1
                P = P + 2 * y - 2 * x + 1
         
            if x < y:
                break
            
            draw8way(x + self.x, y + self.y, 0)
            draw8way(-x + self.x, y + self.y, 0)
            draw8way(x + self.x, -y + self.y, 0)
            draw8way(-x + self.x, -y + self.y, 0)
            drawCircle(self.x,self.y,13)
 
            drawCircle(self.x,self.y,8)

            drawCircle(self.x,self.y,5)
            if x != y:
                draw8way(y + self.x, x + self.y, 0)
                draw8way(-y + self.x, x + self.y, 0)
                draw8way(y + self.x, -x + self.y, 0)
                draw8way(-y + self.x, -x + self.y, 0)


class Love: # life
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self):
        x = self.radius
        y = 0
       
        draw8way(x + self.x, y + self.y, 0)
       
        if self.radius > 0:
            draw8way(x + self.x, -y + self.y, 0)
            draw8way(y + self.x, x + self.y, 0)
            draw8way(-y + self.x, x + self.y, 0)
       
        P = 1 - self.radius 
        while x > y:
            y += 1
        
            if P <= 0: 
                P = P + 2 * y + 1
  
            else:		 
                x -= 1
                P = P + 2 * y - 2 * x + 1
         
            if x < y:
                break
            
            #Love
            drawSemiCircle(self.x+4,self.y,4)
            drawSemiCircle(self.x-4,self.y,4)
            drawLine(self.x+9,self.y,self.x,self.y-11)
            drawLine(self.x-9,self.y,self.x,self.y-11)
            
            drawSemiCircle(self.x+5,self.y,5)
            drawSemiCircle(self.x-5,self.y,5)
            drawLine(self.x+10,self.y,self.x,self.y-12)
            drawLine(self.x-10,self.y,self.x,self.y-12)
            #Love
            drawSemiCircle(self.x+4,self.y,4)
            drawSemiCircle(self.x-4,self.y,4)
            drawLine(self.x+8,self.y,self.x,self.y-10)
            drawLine(self.x-8,self.y,self.x,self.y-10)

            drawCircle(self.x,self.y,17)

            draw8way(x + self.x, y + self.y, 0)
            draw8way(-x + self.x, y + self.y, 0)
            draw8way(x + self.x, -y + self.y, 0)
            draw8way(-x + self.x, -y + self.y, 0)
           
            if x != y:
                draw8way(y + self.x, x + self.y, 0)
                draw8way(-y + self.x, x + self.y, 0)
                draw8way(y + self.x, -x + self.y, 0)
                draw8way(-y + self.x, -x + self.y, 0)
               
class Speed: #minus shape
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self):
        x = self.radius
        y = 0
       
        draw8way(x + self.x, y + self.y, 0)
       
        if self.radius > 0:
            draw8way(x + self.x, -y + self.y, 0)
            draw8way(y + self.x, x + self.y, 0)
            draw8way(-y + self.x, x + self.y, 0)
       
        P = 1 - self.radius 
        while x > y:
            y += 1
        
            if P <= 0: 
                P = P + 2 * y + 1
  
            else:		 
                x -= 1
                P = P + 2 * y - 2 * x + 1
         
            if x < y:
                break
            
            draw8way(x + self.x, y + self.y, 0)
            draw8way(-x + self.x, y + self.y, 0)
            draw8way(x + self.x, -y + self.y, 0)
            draw8way(-x + self.x, -y + self.y, 0)
            
            if x != y:
                draw8way(y + self.x, x + self.y, 0)
                draw8way(-y + self.x, x + self.y, 0)
                draw8way(y + self.x, -x + self.y, 0)
                draw8way(-y + self.x, -x + self.y, 0)
                
        drawLine(self.x - self.radius+5, self.y, self.x + self.radius-5, self.y)

        drawLine(self.x - self.radius+5, (self.y - self.radius // 3) , self.x + self.radius-5, self.y - self.radius // 3)
        drawLine(self.x - self.radius+5, self.y,self.x - self.radius+5,(self.y - self.radius // 3))
        drawLine(self.x + self.radius-5, self.y,self.x + self.radius-5, self.y - self.radius // 3)

def generate_falling_love():
    return Love(random.randint(MAX_RADIUS, WINDOW_WIDTH - MAX_RADIUS), WINDOW_HEIGHT, 18 )

def generate_falling_speed():
    return Speed(random.randint(MAX_RADIUS, WINDOW_WIDTH - MAX_RADIUS), WINDOW_HEIGHT, 18 )
def generate_falling_minus():
    return Minus(random.randint(MAX_RADIUS, WINDOW_WIDTH - MAX_RADIUS), WINDOW_HEIGHT, 18 )

def generate_falling_plus():
    return Plus(random.randint(MAX_RADIUS, WINDOW_WIDTH - MAX_RADIUS), WINDOW_HEIGHT, 18 )


def reset_game():
    global game_over,cl,life, falling_love,falling_love_timer,score,falling_powers,sp ,falling_ships, falling_ship_timer, miss_count,falling_speed,falling_speed_timer, misfire_count,falling_power_timer,falling_plus,falling_plus_timer,b_size_plus,falling_minus,falling_minus_timer
    game_over = False
    score = 0
    sp = 0
    life = 3
    cl = "y"
    falling_love_timer = 0
    falling_love = []
    b_size_plus = 0
    falling_speed = []
    falling_speed_timer = 0
    falling_powers = []
    falling_plus = []
    falling_ships = []
    falling_minus= []
    falling_minus_timer = 0
    falling_ship_timer = 0
    falling_plus_timer = 0
    miss_count = 0
    misfire_count = 0
    shooter.x = WINDOW_WIDTH // 2 
    shooter.y = SHIP_HEIGHT // 2
    projectiles.clear()  

def draw_button(color, x, y, width, height, shape):
    global paused
    glColor3f(*color)
    if shape == "arrow_left":
        drawLine(x + width, y, x +20, y + height / 2)
        drawLine(x +20 , y + height / 2 , x + 70 , y + height / 2)
        drawLine(x + width, y + height, x + 20 , y + height / 2)
    elif shape == "rectangle":
        drawLine(x, y, x + width, y)
        drawLine(x + width, y,x + width, y + height)
        drawLine(x, y + height,x + width, y + height)
        drawLine(x, y + height,x, y)

        if paused == False :
            glColor3f(1.0, 1.0, 1.0)  
            drawLine(x + width * 0.35, y + height * 0.1,x + width * 0.35, y + height * 0.9)
            drawLine(x + width * 0.70, y + height * 0.1,x + width * 0.70, y + height * 0.9)
        else :
            glColor3f(1.0, 1.0, 1.0) 
            drawLine(x + width * 0.1, y + height * 0.1,x + width * 0.1, y + height * 0.9)
            drawLine(x + width * 0.1, y + height * 0.9,x + width * 0.9, y + height / 2)
            drawLine(x + width * 0.9, y + height / 2,x + width * 0.1, y + height * 0.1)
    elif shape == "cross":
        drawLine(x-20 , y,x + width, y + height)
        drawLine(x + width, y,x-20 , y + height)

def mouse_click_listener(button, state, x, y):
    global paused, game_over, score

    if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
        ndc_x = (2 * x) / WINDOW_WIDTH - 1
        ndc_y = 1 - (2 * y) / WINDOW_HEIGHT

        if -0.9 <= ndc_x <= -0.7 and 0.9 <= ndc_y <= 1:
            print("Starting Over")
            reset_game()
        elif -0.1 <= ndc_x <= 0.1 and 0.9 <= ndc_y <= 1:
            paused = not paused
        elif 0.7 <= ndc_x <= 0.9 and 0.9 <= ndc_y <= 1:
            print("Goodbye. Your score:", score)
            glutLeaveMainLoop()

def specialkeylistener(key, x, y) :
    global misfire_count, game_over, paused, projectiles

    if not game_over:
        if not paused:
            if key == GLUT_KEY_UP :  
                if shooter.y + SHIP_HEIGHT // 2 < WINDOW_HEIGHT - 5:
                    shooter.y += 10
            elif key == GLUT_KEY_DOWN :  
                if shooter.y - SHIP_HEIGHT // 2 > 5:
                    shooter.y -= 10
            elif key == GLUT_KEY_RIGHT : 
                if shooter.x + SHIP_WIDTH // 2 < WINDOW_WIDTH - 5:
                    shooter.x += 10
            elif key == GLUT_KEY_LEFT :  
                if shooter.x - SHIP_WIDTH // 2 > 5:
                    shooter.x -= 10


def keyboard(key, x, y):
    global misfire_count, game_over, paused, projectiles,b_size_plus,cl

    if not game_over:
        if not paused:
            if key == b"p" :
                cl = "p"
            if key == b"y" :
                cl = "y"    
            if key == b"o" :
                cl = "o"
            if key == b"i" :
                cl = "i"        
            if key == b' ':  
                projectiles.append(Circle(shooter.x, shooter.y + SHIP_HEIGHT / 2 + BULLET_RADIUS, BULLET_RADIUS+ b_size_plus ))
            else:
                misfire_count += 1


class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self):
        x = self.radius
        y = 0
       
        draw8way(x + self.x, y + self.y, 0)
       
        if self.radius > 0:
            draw8way(x + self.x, -y + self.y, 0)
            draw8way(y + self.x, x + self.y, 0)
            draw8way(-y + self.x, x + self.y, 0)
       
        P = 1 - self.radius 
        while x > y:
            y += 1
        
            if P <= 0: 
                P = P + 2 * y + 1
  
            else:		 
                x -= 1
                P = P + 2 * y - 2 * x + 1
         
            if x < y:
                break
            
            draw8way(x + self.x, y + self.y, 0)
            draw8way(-x + self.x, y + self.y, 0)
            draw8way(x + self.x, -y + self.y, 0)
            draw8way(-x + self.x, -y + self.y, 0)
            
            if x != y:
                draw8way(y + self.x, x + self.y, 0)
                draw8way(-y + self.x, x + self.y, 0)
                draw8way(y + self.x, -x + self.y, 0)
                draw8way(-y + self.x, -x + self.y, 0)

def generate_falling_circle():
    return Circle(random.randint(MAX_RADIUS, WINDOW_WIDTH - MAX_RADIUS), WINDOW_HEIGHT, random.randint(MIN_RADIUS, MAX_RADIUS))

def display():
    global game_over,cl

    if not game_over:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        drawScore()
        draw_button((0.0, 0.8, 0.8), 10, WINDOW_HEIGHT - 30, 50, 20, "arrow_left")  
        draw_button((1.0, 0.5, 0.0), WINDOW_WIDTH / 2 - 10, WINDOW_HEIGHT - 30, 20, 20, "rectangle")  
        draw_button((1.0, 0.0, 0.0), WINDOW_WIDTH - 60, WINDOW_HEIGHT - 30, 50, 20, "cross")  

        glClearColor(0.0, 0.0, 0.0, 1.0)
        
        if cl == "y" :
            glColor3f(1.0, 1.0, 0.0) 
            shooter.draw(1)
        if cl == "p" :
            glColor3f(1.0, 0.75, 0.8)
            shooter.draw(1) 
        if cl == "o" :
            glColor3f(1.0, 0.5, 0.0)
            shooter.draw(1) 
        if cl == "i" :
            glColor3f(0.5, 0.5, 1.0)
            shooter.draw(1)

 
        glColor3f(1.0, 1.0, 0.0) 
        for projectile in projectiles:  
            projectile.draw()
 
        glColor3f(1.0, 1.0, 0.0) 
        for ship in falling_ships:
            ship.draw(2)
            
        glColor3f(1.0, 1.0, 0.0)    
        for power in falling_powers:
            power.draw()    

        glColor3f(0.0, 0.5, 0.0)  
        for plus in falling_plus:
            plus.draw()  

        glColor3f(1.0, 0.0, 0.0)    
        for minus in falling_minus :
            minus.draw()  

        
        glColor3f(1.0, 0.75, 0.8)   
        for speed in falling_speed  :
            speed.draw() 

        glColor3f(0.5, 0.0, 0.0)   
        for love in falling_love  :
            love.draw()            

    else:
        
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        drawGameOver()
        draw_button((0.0, 0.8, 0.8), 10, WINDOW_HEIGHT - 30, 50, 20, "arrow_left")  
        draw_button((1.0, 0.5, 0.0), WINDOW_WIDTH / 2 - 10, WINDOW_HEIGHT - 30, 20, 20, "rectangle")  
        draw_button((1.0, 0.0, 0.0), WINDOW_WIDTH - 60, WINDOW_HEIGHT - 30, 50, 20, "cross")  

        glColor3f(1.0, 1.0, 0.0) 
        shooter.draw(1)
    
    glutSwapBuffers()

MAX_FALLING_BALLS = 2

def update(value):
    global miss_count, misfire_count,life,sp,falling_love,falling_love_timer,falling_speed,falling_speed_timer, falling_ship_timer, score, game_over,falling_power_timer,falling_plus_timer, b_size_plus,falling_minus_timer,falling_minus
    glutPostRedisplay()
    glutTimerFunc(30, update, 0)
    
    if game_over:
        return 
    
    if not paused:
    
        for projectile in projectiles:  
            if projectile.y > 0:
                projectile.y += 20
                for ship in falling_ships: #enemy ship
                    if ((ship.x - projectile.x) ** 2 + (ship.y - projectile.y) ** 2) ** 0.5 <= max(ship.width, ship.height) / 2 + projectile.radius:
                        falling_ships.remove(ship)
                        projectiles.remove(projectile)
                        score += 1
                        sp += 0.01   # Level up
                        print("Score:", score)
                        if len(falling_ships) < MAX_FALLING_SHIPS:
                            falling_ships.append(generate_falling_ship()) 
                        break


                for power in falling_powers:
                    if ((power.x - projectile.x) ** 2 + (power.y - projectile.y) ** 2) ** 0.5 <= power.radius + projectile.radius :
                    
                        falling_powers.remove(power)
                        projectiles.remove(projectile)
                        score += 100
                        print("Score:", score)
                        if len(falling_powers) < 3 :
                            falling_powers.append(generate_falling_power()) 
                        break
  

        for projectile in projectiles[:]:  
            if projectile.y > WINDOW_HEIGHT:
                projectiles.remove(projectile)
                misfire_count += 1
                print("Missed shots:", misfire_count)
                
        for ship in falling_ships[:]:  
            ship.y -= (random.randint(1, 5)+sp)
            # if ship.y - ship.height / 2 <= 0:
            if ship.y < -20 :    
                falling_ships.remove(ship)
                miss_count += 1
                print("Ship missed:", miss_count)

        for power in falling_powers[:]:  
            power.y -= random.randint(1, 5)
            if power.y - power.radius / 2 <= 0:
                falling_powers.remove(power)
                print("Ship missed:", miss_count)


        for plus in falling_plus[:]:  
            plus.y -= (random.randint(1, 5)+0.5)
            if plus.y - plus.radius / 2 <= 0:
                falling_plus.remove(plus)
                print("Ball size increaser missed")
                if len(falling_plus) < 1 :
                    falling_plus.append(generate_falling_plus()) 
                break


        for speed in falling_speed[:]:  
            speed.y -= random.randint(1, 5)
            if speed.y - speed.radius / 2 <= 0:
                falling_speed.remove(speed)
                print("Falling Ship Speed decreaser missed")
                if len(falling_speed) < 1 :
                    falling_speed.append(generate_falling_speed()) 
                break


        for love in falling_love[:]:  
            love.y -= random.randint(1, 5)
            if love.y - love.radius / 2 <= 0:
                falling_love.remove(love)
                print("Life boost missed")
                if len(falling_love) < 1 :
                    falling_love.append(generate_falling_love()) 
                break


        for minus in falling_minus[:]:  
            minus.y -= random.randint(1, 5)
            if minus.y - minus.radius / 2 <= 0:
                falling_minus.remove(minus)
                if len(falling_plus) < 1 :
                    falling_minus.append(generate_falling_minus()) 
                break    


        for ship in falling_ships:  
            # if abs(ship.x - shooter.x) <= max(ship.width, ship.height) / 2 + max(shooter.width, shooter.height) / 2 and abs(ship.y - shooter.y) <= max(ship.width, ship.height) / 2 + max(shooter.width, shooter.height) / 2:
            if ((ship.x - shooter.x) ** 2 + (ship.y - shooter.y) ** 2) ** 0.5 <= max(ship.width, ship.height) / 2 + max(shooter.width, shooter.height) / 2:    
                life -= 1
                falling_ships.remove(ship)
                miss_count = 0
                misfire_count = 0
                print("Life",life)
                if life <= 0 : 
                    print("Game Over! Final Score:", score)
                    game_over = True
                return
            

        for plus in falling_plus:  
            
            if abs(plus.x - shooter.x) <= plus.radius and abs(plus.y - shooter.y) <= plus.radius :
                
                if b_size_plus <= 30 :

                    b_size_plus += 1    
                    print("BALL size increased")
                    falling_plus.remove(plus)
               
                return   
            
        for speed in falling_speed:  
            
            if abs(speed.x - shooter.x) <= speed.radius and abs(speed.y - shooter.y) <= speed.radius :
                sp -= 0.1
                print("Speed DECREASED")
                falling_speed.remove(speed)
            return   
            
        for love in falling_love :  
            
            if abs(love.x - shooter.x) <= love.radius and abs(love.y - shooter.y) <= love.radius :
                
                if life < 10 :
                    
                    life += 1

                    print("Life",life)
                    print("Life BOOST")
                    falling_love.remove(love)
              
            return  
                   
        for minus in falling_minus:  
            
            if abs(minus.x - shooter.x) <= minus.radius and abs(minus.y - shooter.y) <= minus.radius :
                if b_size_plus > -5 :
                    b_size_plus -= 1
                    print("BALL size decreased")
                    falling_minus.remove(minus)
            return        


        if miss_count >= MAX_MISS_COUNT or misfire_count >= MAX_MISFIRE_COUNT:
            life -= 1
            miss_count = 0
            misfire_count = 0
            print("Life",life)
            if life <= 0 :
                print("Game Over! Final Score:", score)
                game_over = True
        
        falling_ship_timer += 30
        if falling_ship_timer >= SHIP_GENERATION_DELAY and len(falling_ships) < MAX_FALLING_SHIPS:
            falling_ships.append(generate_falling_ship())
            falling_ship_timer = 0

        falling_power_timer += 100
        if falling_power_timer >= 1000 and len(falling_powers) < 5 :
            falling_powers.append(generate_falling_power())
            falling_power_timer = 0

        falling_plus_timer += 1.7
        if falling_plus_timer >= 1000 and len(falling_plus) < 1 :
            falling_plus.append(generate_falling_plus())
            falling_plus_timer = 0   

        falling_minus_timer += 1.4
        if falling_minus_timer >= 1000 and len(falling_minus) < 1 :
            falling_minus.append(generate_falling_minus())
            falling_minus_timer = 0     

        falling_speed_timer += 1.3
        if falling_speed_timer >= 1000 and len(falling_speed) < 1 :
            falling_speed.append(generate_falling_speed())
            falling_speed_timer = 0  

        falling_love_timer += 1.5
        if falling_love_timer >= 1000 and len(falling_love) < 1 :
            falling_love.append(generate_falling_love())
            falling_love_timer = 0         

def drawScore():
    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2f(10, WINDOW_HEIGHT - 50)
    score_text = f"Score: {score}\n"
    lifes = f"Life: {life}"
    for character in score_text:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(character))
    for character in lifes :
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(character))    

def drawGameOver():

    glColor3f(1.0, 0.0, 0.0)
    glRasterPos2f(WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2)
    game_over_text = "Game Over ! "
    score_text = f" Score: {score}"
    for character in game_over_text:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(character))
    for character in score_text:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(character))


glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
glutCreateWindow(b"Space Wars !!")
glClearColor(0.0, 0.0, 0.0, 1.0) 
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, -1, 1)
glMatrixMode(GL_MODELVIEW)
glutMouseFunc(mouse_click_listener)
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutSpecialFunc(specialkeylistener)
glutTimerFunc(30, update, 0)
glutMainLoop()
