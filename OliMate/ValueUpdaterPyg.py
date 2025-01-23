import pygame
import pandas as pd
import time
import threading

# Impostazioni di Pygame
pygame.init()
WIDTH, HEIGHT = 800, 900  # Finestra più grande
FONT_SIZE = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)  # Highlight color

# Creazione della finestra
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gara di Matematica")
font = pygame.font.Font(None, FONT_SIZE)

# Funzione per la schermata di input
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

# Classe Problema
class Problema:
    def __init__(self, valore):
        self.solved = False
        self.valore = valore

    def incrementa(self, incremento):
        if not self.solved:
            self.valore += incremento

# Funzione per aggiornare i valori periodicamente
def Incremento(problemi, incremento, intervallo):
    while True:
        for problema in problemi:
            problema.incrementa(incremento)
        time.sleep(intervallo)

# Schermata iniziale per inserire i parametri
result = input_screen()
if not result:
    exit()

numero_problemi, valore_problemi, incremento_problemi, intervallo_incremento = result

# Creazione problemi
Problemi = [Problema(valore_problemi) for _ in range(numero_problemi)]

# Avvio del thread per gli incrementi automatici
thread_incremento = threading.Thread(target=Incremento, args=(Problemi, incremento_problemi, intervallo_incremento))
thread_incremento.daemon = True
thread_incremento.start()

# Variabili per navigazione nella tabella
selected_index = 0
scroll_offset = 0
max_rows = 30  # Numero massimo di righe visibili

running = True

# Loop principale di Pygame per la tabella
while running:
    screen.fill(WHITE)

    # Creazione tabella dati
    dati = []
    for i, problema in enumerate(Problemi, start=1):
        stato = "Risolto" if problema.solved else "Non risolto"
        dati.append([i, problema.valore, stato])

    df = pd.DataFrame(dati, columns=["Numero Problema", "Valore", "Stato"])

    # Gestione dello scrolling
    if selected_index >= scroll_offset + max_rows:
        scroll_offset += 1
    elif selected_index < scroll_offset:
        scroll_offset -= 1

    # Disegna tabella sulla finestra
    y_offset = 50

    for i, row in df.iloc[scroll_offset:scroll_offset + max_rows].iterrows():
        # Convert Pandas row values to strings to avoid type issues
        numero_str = str(row['Numero Problema'])
        valore_str = str(row['Valore'])
        stato_str = str(row['Stato'])

        # Determine colors
        if stato_str == "Risolto":
            stato_color = GREEN
        else:
            stato_color = RED

        row_color = BLUE if (i + scroll_offset) == selected_index else BLACK

        # Render text with correct colors
        numero_text = font.render(numero_str, True, row_color)
        valore_text = font.render(valore_str, True, row_color)
        stato_text = font.render(stato_str, True, stato_color)

        # Positioning and drawing on screen
        screen.blit(numero_text, (50, y_offset))
        screen.blit(valore_text, (150, y_offset))
        screen.blit(stato_text, (300, y_offset))

        y_offset += FONT_SIZE + 5  # Move down for next row

    # Indicatore di scrolling
    if scroll_offset > 0:
        up_arrow = font.render("▲", True, BLACK)
        screen.blit(up_arrow, (WIDTH - 40, 20))
    if scroll_offset + max_rows < len(Problemi):
        down_arrow = font.render("▼", True, BLACK)
        screen.blit(down_arrow, (WIDTH - 40, HEIGHT - 40))

    # Gestione eventi utente
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and selected_index < numero_problemi - 1:
                selected_index += 1
            elif event.key == pygame.K_UP and selected_index > 0:
                selected_index -= 1
            elif event.key == pygame.K_RETURN:  # Premi INVIO per segnare risolto
                Problemi[selected_index].solved = True

    pygame.display.flip()

pygame.quit()
