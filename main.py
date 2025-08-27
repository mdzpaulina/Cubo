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

# Variables para el espejo y rayos
espejo_centro = (0.0, -1.0, 0.0) # Centro del plano del espejo
espejo_normal = (0.0, 1.0, 0.0) # Normal del plano del espejo
vertices = []
proyectiles = []

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
    actualizar_proyectiles()

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

# Funciones parte 2 de la actividad

def dot(v1, v2):
    """Calcula el producto punto de dos vectores."""
    return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]

def normalizar(v):
    """Normaliza un vector."""
    n = norma(v)
    if n == 0.0:
        return (0.0, 0.0, 0.0)
    return (v[0]/n, v[1]/n, v[2]/n)

def calcular_reflejo(v_incidente, n):
    """
    Calcula el vector de un rayo reflejado.
    """
    v = normalizar(v_incidente)
    n = normalizar(n)
    
    # 1) v_paralelo = n * (n . v)
    v_paralelo = tuple(val * dot(n, v) for val in n)
    
    # 2) v_perpendicular = v - v_paralelo
    v_perpendicular = (v[0] - v_paralelo[0], v[1] - v_paralelo[1], v[2] - v_paralelo[2])
    
    # 3) v_reflejado = v_perpendicular - v_paralelo  
    v_reflejado = (v_perpendicular[0] - v_paralelo[0],
                   v_perpendicular[1] - v_paralelo[1],
                   v_perpendicular[2] - v_paralelo[2])
    return v_reflejado

def actualizar_proyectiles():
    global proyectiles, vertices, cubo, espejo_centro, espejo_normal
    proyectiles = []
    
    # Calcular los 8 vértices del cubo en su posición actual
    half_arista = cubo.arista / 2.0
    cx, cy, cz = cubo.cx, cubo.cy, cubo.cz
    
    vertices = [
        (cx + half_arista, cy + half_arista, cz + half_arista),
        (cx - half_arista, cy + half_arista, cz + half_arista),
        (cx + half_arista, cy - half_arista, cz + half_arista),
        (cx - half_arista, cy - half_arista, cz + half_arista),
        (cx + half_arista, cy + half_arista, cz - half_arista),
        (cx - half_arista, cy + half_arista, cz - half_arista),
        (cx + half_arista, cy - half_arista, cz - half_arista),
        (cx - half_arista, cy - half_arista, cz - half_arista)
    ]
    
    for v_origen in vertices:
        # Vector del rayo incidente (desde el vértice al centro del espejo)
        v_incidente = (espejo_centro[0] - v_origen[0],
                       espejo_centro[1] - v_origen[1],
                       espejo_centro[2] - v_origen[2])

        # Se encuentra el punto de intersección con el plano
        # Ecuación del plano: (P - Po) . n = 0
        # Ecuación del rayo: P = O + t*D
        # (O + t*D - Po) . n = 0
        # t*D.n + (O-Po).n = 0
        # t = -((O-Po).n) / (D.n)
        
        O = v_origen
        D = v_incidente
        Po = espejo_centro
        n = espejo_normal
        
        denominador = dot(D, n)
        if abs(denominador) > 0.0001:
            t = -dot((O[0]-Po[0], O[1]-Po[1], O[2]-Po[2]), n) / denominador
            if t > 0:
                punto_impacto = (O[0] + t * D[0],
                                 O[1] + t * D[1],
                                 O[2] + t * D[2])

                # Vector de reflexión
                v_reflejado = calcular_reflejo(v_incidente, espejo_normal)
                
                proyectiles.append({
                    "origen": v_origen,
                    "impacto": punto_impacto,
                    "reflejado_dir": v_reflejado
                })

def draw_espejo():
    """ Dibuja un plano rectangular para simular el espejo. """
    glDisable(GL_CULL_FACE)
    glBegin(GL_QUADS)
    glColor4f(0.5, 0.5, 1.0, 0.4) # Color azul transparente
    glVertex3f(-5.0, espejo_centro[1], -5.0)
    glVertex3f( 5.0, espejo_centro[1], -5.0)
    glVertex3f( 5.0, espejo_centro[1],  5.0)
    glVertex3f(-5.0, espejo_centro[1],  5.0)
    glEnd()
    glEnable(GL_CULL_FACE)
    
def draw_proyectiles():
    """ Dibuja los rayos incidentes y reflejados. """
    glDisable(GL_CULL_FACE)
    glLineWidth(2.5)
    
    for p in proyectiles:
        # Rayo incidente (blanco)
        glBegin(GL_LINES)
        glColor3f(1.0, 1.0, 1.0)
        glVertex3f(*p["origen"])
        glVertex3f(*p["impacto"])
        glEnd()
        
        # Rayo reflejado (amarillo)
        glBegin(GL_LINES)
        glColor3f(1.0, 1.0, 0.2)
        # El rayo reflejado va del punto de impacto en la dirección del vector reflejado
        fin_reflejo = (p["impacto"][0] + p["reflejado_dir"][0] * 5.0,
                       p["impacto"][1] + p["reflejado_dir"][1] * 5.0,
                       p["impacto"][2] + p["reflejado_dir"][2] * 5.0)
        glVertex3f(*p["impacto"])
        glVertex3f(*fin_reflejo)
        glEnd()
        
    glEnable(GL_CULL_FACE)

# OpenGL / GLUT
def init_gl():
    glClearColor(0.08, 0.08, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

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
    # Ajusta la cámara para ver la escena desde un nuevo ángulo
    gluLookAt(4.0, 4.5, 8.0,  0.0, 0.0, 0.0,  0.0, 1.0, 0.0)

    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle * 0.5, 1.0, 0.0, 0.0)

    # Dibuja la ruta si la animación está activa (para que se vea el recorrido)
    if anim["activo"]:
        dibujar_ruta()

    cubo.draw()
    draw_espejo()
    draw_proyectiles()
    
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
            # Llega y se detiene
            cubo.set_centro(anim["B"])
            anim["activo"] = False
        else:
            # Avanza 
            cubo.mover(anim["vel"], anim["dir"], dt)
    
    actualizar_proyectiles()
    glutPostRedisplay()

def keyboard(key, x, y):
    if key in (b'\x1b', b'q'):
        sys.exit(0)
    elif key == b'1':
        # Ejemplo: mover de A a B
        iniciar_movimiento(A=(-2.0, 2.0, 0.0), B=( 2.0, 2.0, 0.0), duracion_seg=3.0)
    elif key == b'2':
        # Ejemplo: mover de B a A
        iniciar_movimiento(A=( 2.0, 2.0, 0.0), B=(-2.0, 2.0, 0.0), duracion_seg=3.0)

def main():
    global cubo
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(900, 600)
    glutCreateWindow(b"Cubo OpenGL - animacion y reflejos")

    init_gl()
    cubo = Cubo(centro=(0.0, 2.0, 0.0), arista=2.0)
    actualizar_proyectiles()

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutIdleFunc(idle)
    glutKeyboardFunc(keyboard)

    glutMainLoop()

if __name__ == "__main__":
    main()