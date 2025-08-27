from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Cubo:
    def __init__(self, centro=(0.0, 0.0, 0.0), arista=1.0):
        self.cx, self.cy, self.cz = map(float, centro)
        self.arista = float(arista)

    def set_centro(self, centro):
        self.cx, self.cy, self.cz = map(float, centro)

    def set_arista(self, arista):
        self.arista = float(arista)

    def mover(self, velocidad, direccion, tiempo):
        dx = velocidad * direccion[0] * tiempo
        dy = velocidad * direccion[1] * tiempo
        dz = velocidad * direccion[2] * tiempo
        self.cx += dx
        self.cy += dy
        self.cz += dz

    def draw(self):
        glPushMatrix()
        glTranslatef(self.cx, self.cy, self.cz)
        glScalef(self.arista, self.arista, self.arista)

        glBegin(GL_QUADS)

        # frente
        glColor3f(1.0, 0.2, 0.2)
        glNormal3f(0.0, 0.0, 1.0)
        glVertex3f(-0.5, -0.5,  0.5)
        glVertex3f( 0.5, -0.5,  0.5)
        glVertex3f( 0.5,  0.5,  0.5)
        glVertex3f(-0.5,  0.5,  0.5)

        # atrás
        glColor3f(0.2, 1.0, 0.2)
        glNormal3f(0.0, 0.0, -1.0)
        glVertex3f( 0.5, -0.5, -0.5)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5,  0.5, -0.5)
        glVertex3f( 0.5,  0.5, -0.5)

        # izquierda
        glColor3f(0.2, 0.4, 1.0)
        glNormal3f(-1.0, 0.0, 0.0)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5, -0.5,  0.5)
        glVertex3f(-0.5,  0.5,  0.5)
        glVertex3f(-0.5,  0.5, -0.5)

        # derecha
        glColor3f(1.0, 1.0, 0.2)
        glNormal3f(1.0, 0.0, 0.0)
        glVertex3f( 0.5, -0.5,  0.5)
        glVertex3f( 0.5, -0.5, -0.5)
        glVertex3f( 0.5,  0.5, -0.5)
        glVertex3f( 0.5,  0.5,  0.5)

        # arriba
        glColor3f(1.0, 0.2, 1.0)
        glNormal3f(0.0, 1.0, 0.0)
        glVertex3f(-0.5,  0.5,  0.5)
        glVertex3f( 0.5,  0.5,  0.5)
        glVertex3f( 0.5,  0.5, -0.5)
        glVertex3f(-0.5,  0.5, -0.5)

        # abajo
        glColor3f(0.2, 1.0, 1.0)
        glNormal3f(0.0, -1.0, 0.0)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f( 0.5, -0.5, -0.5)
        glVertex3f( 0.5, -0.5,  0.5)
        glVertex3f(-0.5, -0.5,  0.5)

        glEnd()
        glPopMatrix()