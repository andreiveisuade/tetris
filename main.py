import pygame
import random
import time

# Constantes
ANCHO_TABLERO = 10
ALTO_TABLERO = 20
TAMANO_CELDA = 30
ANCHO_PANEL = 200  # Ancho del panel de información
ANCHO_VENTANA = ANCHO_TABLERO * TAMANO_CELDA + ANCHO_PANEL
ALTO_VENTANA = ALTO_TABLERO * TAMANO_CELDA

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (128, 128, 128)
AZUL = (0, 0, 255)
CYAN = (0, 255, 255)
AMARILLO = (255, 255, 0)
MAGENTA = (255, 0, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
NARANJA = (255, 165, 0)

# Formas de las piezas
PIEZAS = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
]


class Estadisticas:
    def __init__(self):
        self.score = 0
        self.nivel = 1
        self.lineas_totales = 0
        self.piezas_totales = 0
        self.mejor_combo = 0
        self.combo_actual = 0
        self.tiempo_inicio = time.time()

    def actualizar_stats(self, lineas_eliminadas):
        # Puntos base por líneas
        puntos_base = [0, 40, 100, 300, 1200]  # 0, 1, 2, 3, 4 líneas

        # Actualizar combo
        if lineas_eliminadas > 0:
            self.combo_actual += 1
            self.mejor_combo = max(self.mejor_combo, self.combo_actual)
        else:
            self.combo_actual = 0

        # Calcular puntos con bonus por nivel y combo
        puntos = puntos_base[lineas_eliminadas] * self.nivel
        if self.combo_actual > 1:
            puntos = int(puntos * (1 + self.combo_actual * 0.1))

        self.score += puntos
        self.lineas_totales += lineas_eliminadas

        # Actualizar nivel (cada 10 líneas)
        self.nivel = (self.lineas_totales // 10) + 1

    def nueva_pieza(self):
        self.piezas_totales += 1

    def tiempo_jugado(self):
        segundos = int(time.time() - self.tiempo_inicio)
        minutos = segundos // 60
        segundos = segundos % 60
        return f"{minutos:02d}:{segundos:02d}"


def crear_tablero():
    return [[0 for _ in range(ANCHO_TABLERO)] for _ in range(ALTO_TABLERO)]


def obtener_pieza_aleatoria():
    forma = random.choice(PIEZAS)
    color = random.choice(
        [CYAN, AMARILLO, MAGENTA, ROJO, VERDE, AZUL, NARANJA])
    return {
        "forma": forma,
        "x": ANCHO_TABLERO // 2 - len(forma[0]) // 2,
        "y": 0,
        "color": color,
    }


def validar_movimiento(tablero, pieza, x, y):
    for i in range(len(pieza["forma"])):
        for j in range(len(pieza["forma"][0])):
            if pieza["forma"][i][j] == 0:
                continue
            nuevo_x = x + j
            nuevo_y = y + i
            if (
                nuevo_x < 0
                or nuevo_x >= ANCHO_TABLERO
                or nuevo_y >= ALTO_TABLERO
                or (nuevo_y >= 0 and tablero[nuevo_y][nuevo_x])
            ):
                return False
    return True


def fijar_pieza(tablero, pieza):
    for i in range(len(pieza["forma"])):
        for j in range(len(pieza["forma"][0])):
            if pieza["forma"][i][j] == 1:
                tablero[pieza["y"] + i][pieza["x"] + j] = pieza["color"]
    return tablero


def rotar_pieza(pieza):
    nueva_forma = list(zip(*pieza["forma"][::-1]))
    nueva_forma = [list(fila) for fila in nueva_forma]
    nueva_pieza = pieza.copy()
    nueva_pieza["forma"] = nueva_forma
    return nueva_pieza


def eliminar_lineas_completas(tablero):
    lineas_eliminadas = 0
    y = ALTO_TABLERO - 1
    while y >= 0:
        if all(cell != 0 for cell in tablero[y]):
            lineas_eliminadas += 1
            del tablero[y]
            tablero.insert(0, [0 for _ in range(ANCHO_TABLERO)])
        else:
            y -= 1
    return tablero, lineas_eliminadas


def dibujar_panel_info(screen, stats, siguiente_pieza):
    # Fondo del panel
    panel_rect = pygame.Rect(ANCHO_TABLERO * TAMANO_CELDA,
                             0, ANCHO_PANEL, ALTO_VENTANA)
    pygame.draw.rect(screen, GRIS, panel_rect)

    # Configurar fuente
    font = pygame.font.Font(None, 36)
    font_pequeña = pygame.font.Font(None, 24)

    # Función helper para renderizar texto
    def render_texto(texto, y_pos, fuente=font, color=BLANCO):
        text = fuente.render(texto, True, color)
        screen.blit(text, (ANCHO_TABLERO * TAMANO_CELDA + 10, y_pos))

    # Renderizar estadísticas
    render_texto(f"Nivel: {stats.nivel}", 20)
    render_texto(f"Puntos: {stats.score}", 60)
    render_texto(f"Líneas: {stats.lineas_totales}", 100)
    render_texto("Estadísticas:", 160)
    render_texto(f"Piezas: {stats.piezas_totales}", 200, font_pequeña)
    render_texto(f"Mejor combo: {stats.mejor_combo}", 230, font_pequeña)
    render_texto(f"Combo actual: {stats.combo_actual}", 260, font_pequeña)
    render_texto(f"Tiempo: {stats.tiempo_jugado()}", 290, font_pequeña)

    # Dibujar siguiente pieza
    render_texto("Siguiente:", 340)
    pieza_x = ANCHO_TABLERO * TAMANO_CELDA + 50
    pieza_y = 380
    for i in range(len(siguiente_pieza["forma"])):
        for j in range(len(siguiente_pieza["forma"][0])):
            if siguiente_pieza["forma"][i][j]:
                pygame.draw.rect(
                    screen,
                    siguiente_pieza["color"],
                    (pieza_x + j * 20, pieza_y + i * 20, 19, 19),
                )


def dibujar_celda(screen, color, x, y):
    """Dibuja una única celda en la pantalla"""
    pygame.draw.rect(screen, color,
                     (x * TAMANO_CELDA, y * TAMANO_CELDA,
                      TAMANO_CELDA - 1, TAMANO_CELDA - 1))


def dibujar_celda_transparente(screen, color, x, y, alpha=50):
    """Dibuja una celda transparente en la pantalla"""
    s = pygame.Surface((TAMANO_CELDA - 1, TAMANO_CELDA - 1))
    s.set_alpha(alpha)
    s.fill(color)
    screen.blit(s, (x * TAMANO_CELDA, y * TAMANO_CELDA))


def dibujar_piezas_fijas(screen, tablero):
    """Dibuja todas las piezas que ya están fijas en el tablero"""
    for y in range(ALTO_TABLERO):
        for x in range(ANCHO_TABLERO):
            if tablero[y][x]:
                dibujar_celda(screen, tablero[y][x], x, y)


def dibujar_pieza(screen, pieza, transparente=False):
    """Dibuja una pieza (actual o fantasma) en la pantalla"""
    for i in range(len(pieza['forma'])):
        for j in range(len(pieza['forma'][0])):
            if pieza['forma'][i][j]:
                x = pieza['x'] + j
                y = pieza['y'] + i
                if transparente:
                    dibujar_celda_transparente(screen, pieza['color'], x, y)
                else:
                    dibujar_celda(screen, pieza['color'], x, y)


def dibujar_pieza_fantasma(screen, tablero, pieza_actual):
    """Dibuja la previsualización de dónde caerá la pieza"""
    fantasma = obtener_posicion_fantasma(tablero, pieza_actual)
    dibujar_pieza(screen, fantasma, transparente=True)


def dibujar_tablero(screen, tablero, pieza_actual, mostrar_fantasma=True):
    """
    Dibuja el estado actual del tablero, incluyendo piezas fijas,
    pieza actual y opcionalmente la pieza fantasma.
    """
    # Limpiar pantalla
    screen.fill(NEGRO)

    # Dibujar los diferentes elementos
    dibujar_piezas_fijas(screen, tablero)

    if mostrar_fantasma:
        dibujar_pieza_fantasma(screen, tablero, pieza_actual)

    dibujar_pieza(screen, pieza_actual)


def dibujar_pausa(screen):
    # Crear una superficie semitransparente para oscurecer el juego
    s = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA))
    s.set_alpha(128)
    s.fill(NEGRO)
    screen.blit(s, (0, 0))

    # Mostrar texto de PAUSA
    font = pygame.font.Font(None, 74)
    texto_pausa = font.render('PAUSA', True, BLANCO)
    rect_pausa = texto_pausa.get_rect(
        center=(ANCHO_VENTANA//2, ALTO_VENTANA//2))
    screen.blit(texto_pausa, rect_pausa)

    # Mostrar instrucciones
    font_pequeña = pygame.font.Font(None, 36)
    texto_continuar = font_pequeña.render(
        'Presiona P para continuar', True, BLANCO)
    rect_continuar = texto_continuar.get_rect(
        center=(ANCHO_VENTANA//2, ALTO_VENTANA//2 + 50))
    screen.blit(texto_continuar, rect_continuar)


def calcular_velocidad(nivel):
    # Velocidad base de 0.5 segundos, disminuye con cada nivel
    return max(0.1, 0.5 - (nivel - 1) * 0.05)


def obtener_posicion_fantasma(tablero, pieza):
    """Calcula la posición más baja posible para la pieza actual"""
    fantasma = pieza.copy()
    while validar_movimiento(tablero, fantasma, fantasma["x"], fantasma["y"] + 1):
        fantasma["y"] += 1
    return fantasma


def caida_instantanea(tablero, pieza):
    """Mueve la pieza instantáneamente a la posición más baja posible"""
    while validar_movimiento(tablero, pieza, pieza["x"], pieza["y"] + 1):
        pieza["y"] += 1
    return pieza


def procesar_entrada_teclado(event, estado_juego):
    """Procesa los eventos de teclado y actualiza el estado del juego"""
    if event.key == pygame.K_p:
        estado_juego['pausado'] = not estado_juego['pausado']
        pygame.display.set_caption(
            'Tetris - PAUSADO' if estado_juego['pausado'] else 'Tetris')
        return None

    if event.key == pygame.K_h:
        estado_juego['mostrar_fantasma'] = not estado_juego['mostrar_fantasma']
        return None

    if estado_juego['pausado']:
        return None

    return procesar_movimientos_pieza(event, estado_juego)


def procesar_movimientos_pieza(event, estado_juego):
    """Procesa los movimientos de la pieza actual"""
    pieza = estado_juego['pieza_actual']
    tablero = estado_juego['tablero']
    x, y = pieza['x'], pieza['y']

    if event.key == pygame.K_LEFT and validar_movimiento(tablero, pieza, x - 1, y):
        pieza['x'] -= 1
    elif event.key == pygame.K_RIGHT and validar_movimiento(tablero, pieza, x + 1, y):
        pieza['x'] += 1
    elif event.key == pygame.K_DOWN and validar_movimiento(tablero, pieza, x, y + 1):
        pieza['y'] += 1
    elif event.key == pygame.K_UP:
        pieza_rotada = rotar_pieza(pieza)
        if validar_movimiento(tablero, pieza_rotada, x, y):
            estado_juego['pieza_actual'] = pieza_rotada
    elif event.key == pygame.K_SPACE:
        return procesar_caida_instantanea(estado_juego)

    return None


def procesar_caida_instantanea(estado_juego):
    """Procesa la caída instantánea de una pieza"""
    pieza = caida_instantanea(
        estado_juego['tablero'], estado_juego['pieza_actual'])
    return actualizar_despues_de_fijar_pieza(estado_juego, pieza)


def actualizar_despues_de_fijar_pieza(estado_juego, pieza):
    """Actualiza el estado del juego después de fijar una pieza"""
    tablero = fijar_pieza(estado_juego['tablero'], pieza)
    tablero, lineas_eliminadas = eliminar_lineas_completas(tablero)
    estado_juego['stats'].actualizar_stats(lineas_eliminadas)

    # Actualizar piezas
    estado_juego['pieza_actual'] = estado_juego['siguiente_pieza']
    estado_juego['siguiente_pieza'] = obtener_pieza_aleatoria()
    estado_juego['stats'].nueva_pieza()

    # Verificar game over
    if not validar_movimiento(tablero, estado_juego['pieza_actual'],
                              estado_juego['pieza_actual']['x'],
                              estado_juego['pieza_actual']['y']):
        return True  # Game Over

    estado_juego['tablero'] = tablero
    estado_juego['ultima_caida'] = time.time()
    return False


def procesar_caida_normal(estado_juego):
    """Procesa la caída normal de la pieza actual"""
    if estado_juego['pausado']:
        return False

    tiempo_actual = time.time()
    if tiempo_actual - estado_juego['ultima_caida'] <= calcular_velocidad(estado_juego['stats'].nivel):
        return False

    pieza = estado_juego['pieza_actual']
    if validar_movimiento(estado_juego['tablero'], pieza, pieza['x'], pieza['y'] + 1):
        pieza['y'] += 1
        estado_juego['ultima_caida'] = tiempo_actual
        return False

    return actualizar_despues_de_fijar_pieza(estado_juego, pieza)


def inicializar_juego():
    """Inicializa el estado del juego"""
    return {
        'tablero': crear_tablero(),
        'stats': Estadisticas(),
        'pieza_actual': obtener_pieza_aleatoria(),
        'siguiente_pieza': obtener_pieza_aleatoria(),
        'game_over': False,
        'pausado': False,
        'mostrar_fantasma': True,
        'ultima_caida': time.time()
    }


def dibujar_game_over(screen):
    """Dibuja la pantalla de Game Over"""
    font = pygame.font.Font(None, 48)
    game_over_text = font.render('GAME OVER', True, ROJO)
    screen.blit(game_over_text, (ANCHO_TABLERO *
                TAMANO_CELDA // 4, ALTO_VENTANA // 2))
    pygame.display.flip()
    time.sleep(3)


def main():
    pygame.init()
    screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption('Tetris')
    clock = pygame.time.Clock()

    estado_juego = inicializar_juego()
    estado_juego['stats'].nueva_pieza()

    while not estado_juego['game_over']:
        # Procesar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                game_over = procesar_entrada_teclado(event, estado_juego)
                if game_over:
                    estado_juego['game_over'] = True
                    break

        # Procesar caída de pieza
        if not estado_juego['game_over']:
            estado_juego['game_over'] = procesar_caida_normal(estado_juego)

        # Dibujar estado actual
        dibujar_tablero(screen, estado_juego['tablero'],
                        estado_juego['pieza_actual'],
                        estado_juego['mostrar_fantasma'])
        dibujar_panel_info(screen, estado_juego['stats'],
                           estado_juego['siguiente_pieza'])

        if estado_juego['pausado']:
            dibujar_pausa(screen)

        pygame.display.flip()
        clock.tick(60)

    dibujar_game_over(screen)
    pygame.quit()


if __name__ == '__main__':
    main()
