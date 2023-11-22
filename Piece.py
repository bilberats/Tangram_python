from shapely import *
import pygame
from pygame import gfxdraw
import math

class Piece():
    def __init__(self,_polygon,_color,_coord=Point((0,0))):
        self.color = _color
        self.poly = Polygon(_polygon)
        self.coord = Point(_coord)
        self.grabOffset = self.coord

    def display(self,screen):
        pygame.gfxdraw.filled_polygon(screen, self.poly.exterior.coords,self.color)
        pygame.gfxdraw.aapolygon(screen, self.poly.exterior.coords,self.color)

    def getPoly(self):
        return self.poly
    
    def setPoly(self,newPoly):
        self.poly = Polygon(newPoly)

    def moveToPoint(self,point):
        x,y = point
        coords = self.poly.exterior.coords[:]
        for i in range(len(coords)):
            cx,cy = coords[i]
            coords[i] = (cx + (x - self.coord.x), cy + (y - self.coord.y))
        self.poly = Polygon(coords)
        self.coord = Point(point)

    def setOffset(self,mousePos):
        x,y = mousePos
        x -= self.coord.x
        y -= self.coord.y
        self.grabOffset = Point(x,y)

    def OnMouseDown(self,mousePos):
        print("mouseDown")
        self.setOffset(mousePos)

    def OnMouseUp(self):
        print("mouseUp")

    def OnGrab(self,mousePos,pieces):
        #grab management
        mouseX,mouseY = mousePos
        newX = mouseX - self.grabOffset.x
        newY = mouseY - self.grabOffset.y

        #keeping previous position in case of collision
        oldX = self.coord.x
        oldY = self.coord.y
        self.moveToPoint((newX,newY))
        if(self.CollisionCheck(pieces)):
            self.moveToPoint((oldX,oldY))
            self.setOffset(mousePos)


    def CollisionCheck(self,pieces):
        for piece in pieces:
            if(self.poly.intersects(piece.poly)):
                return True
    

    def Rotate(self, angle):
        self.poly = Polygon(RotatePoint(point,angle) for point in self.poly.exterior.coords)


# je sais pas ou mettre cette fonction pour que y'ai que la class piece.py dans ce fichier
def RotatePoint(point, angle):
    rad_angle = math.radians(angle)
    return(Point(point[0] * math.cos(rad_angle) - point[1] * math.sin(rad_angle), point[0] * math.sin(rad_angle) - point[1] * math.cos(rad_angle)))
