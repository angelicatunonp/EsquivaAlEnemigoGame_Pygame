import pygame
import sys
import random
import time 

pygame.init()

# Configuración de pantalla
ANCHO = 600
ALTO = 400
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Esquiva al Enemigo")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)

# Reloj
clock = pygame.time.Clock()

# ---------------------------- FUNCIONES ---------------------------- #
def dibujar_texto(texto, tamano, x, y):
    font = pygame.font.SysFont(None, tamano)
    img = font.render(texto, True, BLANCO)
    pantalla.blit(img, (x, y))


def velocidad_no_cero():
    return random.choice([-4, -3, -2, 2, 3, 4])


def crear_enemigo():
    x = random.randint(0, ANCHO - 40)
    y = random.randint(0, ALTO - 40)
    return {
        "rect": pygame.Rect(x, y, 40, 40),
        "vx": velocidad_no_cero(),
        "vy": velocidad_no_cero()
    }


def mover_enemigo(enemigo):
    rect = enemigo["rect"]

    rect.x += enemigo["vx"]
    rect.y += enemigo["vy"]

    # Rebote horizontal
    if rect.x <= 0 or rect.x >= ANCHO - rect.width:
        enemigo["vx"] = -enemigo["vx"]

    # Rebote vertical
    if rect.y <= 0 or rect.y >= ALTO - rect.height:
        enemigo["vy"] = -enemigo["vy"]

    # Corrección de límites
    rect.x = max(0, min(rect.x, ANCHO - rect.width))
    rect.y = max(0, min(rect.y, ALTO - rect.height))

    # Cambiar la dirección al azar
    if random.randint(0, 20) == 0:
        enemigo["vx"] = velocidad_no_cero()
        enemigo["vy"] = velocidad_no_cero()


def menu_principal():
    while True:
        pantalla.fill(NEGRO)
        dibujar_texto("ESQUIVA AL ENEMIGO", 50, 100, 120)
        dibujar_texto("Presiona ESPACIO para jugar", 30, 140, 250)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return

        pygame.display.update()


def juego():
    jugador = pygame.Rect(300, 300, 40, 40)
    enemigo = crear_enemigo()

    velocidad = 5

    # --- INICIO DEL TIEMPO ---
    inicio_tiempo = time.time()

    while True:
        pantalla.fill(NEGRO)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT]:
            jugador.x -= velocidad
        if teclas[pygame.K_RIGHT]:
            jugador.x += velocidad
        if teclas[pygame.K_UP]:
            jugador.y -= velocidad
        if teclas[pygame.K_DOWN]:
            jugador.y += velocidad

        jugador.x = max(0, min(jugador.x, ANCHO - jugador.width))
        jugador.y = max(0, min(jugador.y, ALTO - jugador.height))

        mover_enemigo(enemigo)

        pygame.draw.rect(pantalla, AZUL, jugador)
        pygame.draw.rect(pantalla, ROJO, enemigo["rect"])

        # --- TIEMPO TRANSCURRIDO ---
        tiempo_actual = int(time.time() - inicio_tiempo)
        dibujar_texto(f"Tiempo: {tiempo_actual}s", 30, 10, 10)

        if jugador.colliderect(enemigo["rect"]):
            return

        pygame.display.update()
        clock.tick(60)


def fin_del_juego():
    while True:
        pantalla.fill(NEGRO)
        dibujar_texto("¡PERDISTE!", 60, 180, 120)
        dibujar_texto("Presiona ENTER para reiniciar", 30, 150, 250)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return

        pygame.display.update()


# ---------------------------- LOOP PRINCIPAL ---------------------------- #
while True:
    menu_principal()
    juego()
    fin_del_juego()
