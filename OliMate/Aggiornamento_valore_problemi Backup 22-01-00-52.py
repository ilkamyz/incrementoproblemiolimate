import pygame
import time
import threading

# Pygame settings
pygame.init()
WIDTH, HEIGHT = 800, 900  # Larger window
FONT_SIZE = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulazione gara a squadre")
font = pygame.font.Font(pygame.font.match_font('arial', bold=True), FONT_SIZE)

def draw_rounded_box(x, y, w, h, color):
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=15)

def draw_centered_text(text, x, y, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x - text_surface.get_width() // 2, y))

def animate_value_change(problema, target_value):
    steps = abs(target_value - problema.valore)
    step_size = (target_value - problema.valore) / max(steps, 1)
    for _ in range(steps):
        problema.valore += step_size
        pygame.display.flip()
        pygame.time.delay(30)

class Problema:
    def __init__(self, numero, valore):
        self.numero = numero
        self.valore = valore
        self.solved = False
        self.sbagliato = 0

    def incrementa(self, incremento):
        if not self.solved:
            self.valore += incremento

def Incremento(problemi, incremento, intervallo):
    while True:
        for problema in problemi:
            problema.incrementa(incremento)
        time.sleep(intervallo)

numero_problemi = 10
valore_problemi = 100
incremento_problemi = 10
intervallo_incremento = 5
incrememento_errore = 5

Problemi = [Problema(i + 1, valore_problemi) for i in range(numero_problemi)]

thread_incremento = threading.Thread(target=Incremento, args=(Problemi, incremento_problemi, intervallo_incremento))
thread_incremento.daemon = True
thread_incremento.start()

selected_index = 0
scroll_offset = 0
max_rows = 10
running = True

while running:
    screen.fill(WHITE)
    draw_rounded_box(30, 100, WIDTH - 60, HEIGHT - 200, GRAY)
    draw_centered_text("Simulazione gara a squadre", WIDTH // 2, 30, BLACK)

    y_offset = 130
    for i in range(scroll_offset, min(scroll_offset + max_rows, len(Problemi))):
        problema = Problemi[i]
        row_color = BLUE if i == selected_index else BLACK
        stato_color = GREEN if problema.solved else RED
        draw_centered_text(f"{problema.numero}", 100, y_offset, row_color)
        draw_centered_text(f"{int(problema.valore)}", 250, y_offset, row_color)
        draw_centered_text("Risolto" if problema.solved else "Non risolto", 400, y_offset, stato_color)
        draw_centered_text(f"Errori: {problema.sbagliato}", 550, y_offset, row_color)
        y_offset += FONT_SIZE + 10

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and selected_index < numero_problemi - 1:
                selected_index += 1
            elif event.key == pygame.K_UP and selected_index > 0:
                selected_index -= 1
            elif event.key == pygame.K_RETURN:
                Problemi[selected_index].solved = True
            elif event.key == pygame.K_x:
                Problemi[selected_index].sbagliato += 1
                animate_value_change(Problemi[selected_index], Problemi[selected_index].valore + incrememento_errore)
            elif event.key == pygame.K_z:
                Problemi[selected_index].sbagliato -= 1
                animate_value_change(Problemi[selected_index], Problemi[selected_index].valore - incrememento_errore)
            elif event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                Problemi[selected_index].solved = False
            elif event.unicode == '+':
                animate_value_change(Problemi[selected_index], Problemi[selected_index].valore + 1)
            elif event.key == pygame.K_MINUS:
                animate_value_change(Problemi[selected_index], Problemi[selected_index].valore - 1)

    pygame.display.flip()

pygame.quit()
