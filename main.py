import sys
import pygame
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from cubo import Cubo

from pygame.locals import DOUBLEBUF, OPENGL, QUIT

angle = 0.0
cubo = None

anim = {
    "activo": False,
    "A": (0.0, 0.0, 0.0),
    "B": (0.0, 0.0, 0.0),
    "dir": (0.0, 0.0, 0.0),   # dirección normalizada
    "vel": 0.0,               # distancia / duración
    "t_prev": 0.0             # tiempo anterior (s)
}

def norma(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])

def iniciar_movimiento(A, B, duracion_seg=2.0):
    """
    Inicia una animación para mover el cubo de A a B en 'duracion_seg' segundos
    usando cubo.mover(velocidad, direccion, tiempo).
    """
    global anim, cubo
    A = tuple(map(float, A))
    B = tuple(map(float, B))
    vec = (B[0]-A[0], B[1]-A[1], B[2]-A[2])
    dist = norma(vec)

    # Colocar el cubo en A
    cubo.set_centro(A)

    # Casos borde: distancia o duración nulas -> saltar directo a B
    if dist == 0.0 or duracion_seg <= 0.0:
        cubo.set_centro(B)
        anim["activo"] = False
        glutPostRedisplay()
        return

    dir_norm = (vec[0]/dist, vec[1]/dist, vec[2]/dist)
    vel = dist / float(duracion_seg)

    anim["A"] = A
    anim["B"] = B
    anim["dir"] = dir_norm
    anim["vel"] = vel
    anim["t_prev"] = glutGet(GLUT_ELAPSED_TIME) / 1000.0
    anim["activo"] = True

def dibujar_ruta():
    """ Dibuja una línea entre A y B para visualizar el recorrido. """
    glDisable(GL_CULL_FACE)
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 1.0)
    glVertex3f(*anim["A"])
    glVertex3f(*anim["B"])
    glEnd()

    glPointSize(6.0)
    glBegin(GL_POINTS)
    glColor3f(1.0, 1.0, 1.0)
    glVertex3f(*anim["A"])
    glVertex3f(*anim["B"])
    glEnd()
    glEnable(GL_CULL_FACE)

# ======================
# OpenGL / GLUT
# ======================
def init_gl():
    glClearColor(0.08, 0.08, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)

def reshape(w, h):
    h = max(h, 1)
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, float(w) / float(h), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def display():
    global angle, cubo
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    gluLookAt(0.0, 1.5, 6.0,  0.0, 0.0, 0.0,  0.0, 1.0, 0.0)

    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle * 0.5, 1.0, 0.0, 0.0)

    # Dibuja la ruta si la animación está activa (para que se vea el recorrido)
    if anim["activo"]:
        dibujar_ruta()

    cubo.draw()
    glutSwapBuffers()

def idle():
    global angle, cubo, anim
    angle = (angle + 0.25) % 360.0

    # Actualización de animación basada en tiempo real
    if anim["activo"]:
        t_now = glutGet(GLUT_ELAPSED_TIME) / 1000.0
        dt = t_now - anim["t_prev"]
        anim["t_prev"] = t_now
        if dt < 0.0:
            dt = 0.0

        # Longitud del paso a dar en este frame
        paso = anim["vel"] * dt

        # Distancia restante al objetivo B
        rvec = (anim["B"][0] - cubo.cx,
                anim["B"][1] - cubo.cy,
                anim["B"][2] - cubo.cz)
        dist_rest = norma(rvec)

        if paso >= dist_rest or dist_rest == 0.0:
            # Llega (o se pasa) -> clampa a B y detén animación
            cubo.set_centro(anim["B"])
            anim["activo"] = False
        else:
            # Avanza usando TU función mover(velocidad, direccion, tiempo)
            cubo.mover(anim["vel"], anim["dir"], dt)

    glutPostRedisplay()

def keyboard(key, x, y):
    if key in (b'\x1b', b'q'):
        sys.exit(0)
    elif key == b'1':
        # Ejemplo: mover de A a B
        iniciar_movimiento(A=(-2.0, 0.0, 0.0), B=( 2.0, 0.0, 0.0), duracion_seg=3.0)
    elif key == b'2':
        # Ejemplo: mover de B a A
        iniciar_movimiento(A=( 2.0, 0.0, 0.0), B=(-2.0, 0.0, 0.0), duracion_seg=3.0)

def main():
    global cubo
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(900, 600)
    glutCreateWindow(b"Cubo OpenGL - animacion A->B con mover(vel, dir, tiempo)")

    init_gl()
    cubo = Cubo(centro=(0.0, 0.0, 0.0), arista=2.0)

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutIdleFunc(idle)
    glutKeyboardFunc(keyboard)

    # Si quieres que arranque moviéndose automáticamente, descomenta:
    # iniciar_movimiento(A=(-2.0, 0.0, 0.0), B=(2.0, 0.0, 0.0), duracion_seg=3.0)

    glutMainLoop()

if __name__ == "__main__":
    main()