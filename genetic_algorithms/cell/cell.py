import pygame
import math

class Cell:

    def __init__(self, x, y, radius):
        self.x = math.floor(x)
        self.y = math.floor(y)

        self.vx = 0
        self.vy = 0

        self.ax = 0
        self.ay = 0

        self.r = radius

        self.color = 255, 255, 255

        self.friction_state = False
        self.friction_value = 0

    def setColor(self, color):
        self.color = color

    def getPos(self):
        return self.x, self.y

    def setPos(self, pos):
        self.x = math.floor(pos[0])
        self.y = math.floor(pos[1])
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.r)

    def setSpeed(self, speed):
        self.vx = math.floor(speed[0])
        self.vy = math.floor(speed[1])

    def getSpeed(self):
        return self.vx, self.vy
    
    def addForce(self, force):
        self.ax += force[0]
        self.ay += force[1]

    def enableFriction(self, state, value):
        self.friction_state = state
        self.friction_value = value

    def updateFixed(self, interval):
        if self.friction_state == True:
            self.vx *= self.friction_value
            self.vy *= self.friction_value
            
        self.vx += self.ax * interval
        self.vy += self.ay * interval

        # self.x += math.floor(self.vx * interval)
        # self.y += math.floor(self.vy * interval)

        self.ax = 0
        self.ay = 0

    def update(self, interval):
        self.x += math.floor(self.vx * interval)
        self.y += math.floor(self.vy * interval)
        
