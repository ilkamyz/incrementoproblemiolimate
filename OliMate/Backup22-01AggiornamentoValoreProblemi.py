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
BLUE = (0, 0, 255)  # Highlight color

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gara di Matematica")
font = pygame.font.Font(None, FONT_SIZE)

# Function to get user input in Pygame
def input_screen():
    inputs = ["Numero Problemi", "Valore Iniziale", "Incremento", "Intervallo (sec)"]
    values = ["", "", "", ""]
    selected_index = 0

    running = True
    while running:
        screen.fill(WHITE)

        title = font.render("Inserisci i dati iniziali:", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        for i, (label, value) in enumerate(zip(inputs, values)):
            color = GREEN if i == selected_index else BLACK
            text = font.render(f"{label}: {value}", True, color)
            screen.blit(text, (50, 150 + i * 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and selected_index < len(inputs) - 1:
                    selected_index += 1
                elif event.key == pygame.K_UP and selected_index > 0:
                    selected_index -= 1
                elif event.key == pygame.K_BACKSPACE:
                    values[selected_index] = values[selected_index][:-1]
                elif event.key == pygame.K_RETURN and all(values):
                    return list(map(int, values))
                elif event.unicode.isdigit():
                    values[selected_index] += event.unicode

# Problem class
class Problema:
    def __init__(self, numero, valore):
        self.numero = numero
        self.valore = valore
        self.solved = False

    def incrementa(self, incremento):
        if not self.solved:
            self.valore += incremento

# Function to update values periodically
def Incremento(problemi, incremento, intervallo):
    while True:
        for problema in problemi:
            problema.incrementa(incremento)
        time.sleep(intervallo)

# Get user input
result = input_screen()
if not result:
    exit()

numero_problemi, valore_problemi, incremento_problemi, intervallo_incremento = result

# Create problems list (without pandas)
Problemi = [Problema(i + 1, valore_problemi) for i in range(numero_problemi)]

# Start auto-increment thread
thread_incremento = threading.Thread(target=Incremento, args=(Problemi, incremento_problemi, intervallo_incremento))
thread_incremento.daemon = True
thread_incremento.start()

# Navigation variables
selected_index = 0
scroll_offset = 0
max_rows = 50 # Max visible rows

running = True

# Main Pygame loop
while running:
    screen.fill(WHITE)

    # Manage scrolling
    if selected_index >= scroll_offset + max_rows:
        scroll_offset += 1
    elif selected_index < scroll_offset:
        scroll_offset -= 1

    # Draw table
    y_offset = 50

    for i in range(scroll_offset, min(scroll_offset + max_rows, len(Problemi))):
        problema = Problemi[i]

        # Status color
        stato_color = GREEN if problema.solved else RED
        stato_str = "✔ Risolto" if problema.solved else "❌ Non risolto"

        # Row highlight color
        row_color = BLUE if i == selected_index else BLACK

        # Render text
        numero_text = font.render(f"{problema.numero}", True, row_color)
        valore_text = font.render(f"{problema.valore}", True, row_color)
        stato_text = font.render(stato_str, True, stato_color)

        # Draw on screen
        screen.blit(numero_text, (50, y_offset))
        screen.blit(valore_text, (150, y_offset))
        screen.blit(stato_text, (300, y_offset))

        y_offset += FONT_SIZE + 5  # Move down

    # Scroll indicators
    if scroll_offset > 0:
        up_arrow = font.render("▲", True, BLACK)
        screen.blit(up_arrow, (WIDTH - 40, 20))
    if scroll_offset + max_rows < len(Problemi):
        down_arrow = font.render("▼", True, BLACK)
        screen.blit(down_arrow, (WIDTH - 40, HEIGHT - 40))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and selected_index < numero_problemi - 1:
                selected_index += 1
            elif event.key == pygame.K_UP and selected_index > 0:
                selected_index -= 1
            elif event.key == pygame.K_RETURN:  # Mark problem as solved
                Problemi[selected_index].solved = True

    pygame.display.flip()

pygame.quit()
