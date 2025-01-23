import pygame
import time
import threading

# Pygame settings
pygame.init()
WIDTH, HEIGHT = 800, 750  # Larger window
FONT_SIZE = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 180, 34)
RED = (255, 0, 0)
BLUE = (0, 0, 255)  
PURPLE = (128, 0, 128)
DARK_RED = (139, 0, 0)
# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulazione gara a squadre")
font = pygame.font.Font(pygame.font.match_font('arial'), FONT_SIZE)
clock = pygame.time.Clock()
def rowColor(Problema):
    if Problema.solved:
        return GREEN
    else: 
        return BLACK
def statoRowColor(Problema):
        if Problema.solved:
            return GREEN
        else: 
            return RED
def erroriRowColor(Problema):
    if Problema.sbagliato == 0 or Problema.solved:
        return GREEN
    else: 
        return DARK_RED
def erroriString(problema):
    global incrememento_errore
    if problema.sbagliato == 0:
        return f'{problema.sbagliato}'
    else:
        return f'{problema.sbagliato} (+{incrememento_errore*problema.sbagliato})'
# Function to get user input in Pygame
def input_screen():
    inputs = ["Numero Problemi", "Valore Iniziale", "Incremento", "Intervallo (sec)","Incremento per ogni errore"]
    values = ["", "", "", "",""]
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
        self.valore = valore - incremento_problemi
        self.solved = False
        self.sbagliato = 0 # 0 < x < nSquadre

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

numero_problemi, valore_problemi, incremento_problemi, intervallo_incremento, incrememento_errore = result

# Create problems list 
Problemi = [Problema(i + 1, valore_problemi) for i in range(numero_problemi)]

# Start auto-increment thread
thread_incremento = threading.Thread(target=Incremento, args=(Problemi, incremento_problemi, intervallo_incremento))
thread_incremento.daemon = True
thread_incremento.start()

# Navigation variables
selected_index = 0
scroll_offset = 0
max_rows = 17 # Max visible rows

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
    y_offset = 165
    tutorial_text1 = font.render('Invio: Segna un problema come risolto, Shift: Annulla', True, BLACK)
    tutorial_text2 = font.render('X: Aggiunge un errore a un problema, Z: Annulla', True, BLACK)
    tutorial_text3 = font.render('+ e - per modificare manualmente il valore di un problema', True, BLACK)
    
    screen.blit(tutorial_text1, (20, 30))
    screen.blit(tutorial_text2, (20, 30 + FONT_SIZE + 5))
    screen.blit(tutorial_text3, (20, 30 + FONT_SIZE + 5 + FONT_SIZE))
    screen.blit(font.render('Problema',True, PURPLE), (40, 30 + FONT_SIZE + 5 + FONT_SIZE + FONT_SIZE  + 10)) 
    screen.blit(font.render('Valore',True, PURPLE), (200, 30 + FONT_SIZE + 5 + FONT_SIZE + FONT_SIZE + 10)) 
    screen.blit(font.render('Stato',True, PURPLE), (300, 30 + FONT_SIZE + 5 + FONT_SIZE + FONT_SIZE + 10)) 
    screen.blit(font.render('Errori',True, PURPLE), (450, 30 + FONT_SIZE + 5 + FONT_SIZE + FONT_SIZE + 10)) 
    for i in range(scroll_offset, min(scroll_offset + max_rows, len(Problemi))):
        problema = Problemi[i]

        # Status color
        stato_color = BLUE if i == selected_index else statoRowColor(problema)
        stato_str = "Risolto" if problema.solved else "Non risolto"
        errori_color = BLUE if i == selected_index else erroriRowColor(problema)
        # Row highlight color
        
        row_color = BLUE if i == selected_index else rowColor(problema)

        # Render text
        numero_text = font.render(f"{problema.numero}", True, row_color)
        valore_text = font.render(f"{problema.valore}", True, row_color)
        stato_text = font.render(stato_str, True, stato_color)
        
        sbagliato_text = font.render(erroriString(problema), True, errori_color)

        # Draw on screen
        screen.blit(numero_text, (40, y_offset))
        screen.blit(valore_text, (200, y_offset))
        screen.blit(stato_text, (300, y_offset))
        screen.blit(sbagliato_text, (450, y_offset))

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
            #if event.key == pygame.K_DOWN and selected_index < numero_problemi - 1:
              #  selected_index += 1
            #elif event.key == pygame.K_UP and selected_index > 0:
           #     selected_index -= 1
            if event.key == pygame.K_RETURN:  # Mark problem as solved
                Problemi[selected_index].solved = True
            elif event.key == pygame.K_x:
                if not Problemi[selected_index].solved:
                    Problemi[selected_index].sbagliato += 1
                    Problemi[selected_index].valore += incrememento_errore
            elif event.key == pygame.K_z:
                if not Problemi[selected_index].solved:
                    Problemi[selected_index].sbagliato -= 1
                    Problemi[selected_index].valore -= incrememento_errore
            elif event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                Problemi[selected_index].solved = False
            elif event.unicode == '+':
                Problemi[selected_index].valore += 1
            elif event.key == pygame.K_MINUS:
                Problemi[selected_index].valore -= 1
    keys = pygame.key.get_pressed()  
    if keys[pygame.K_DOWN] and selected_index < numero_problemi - 1:
        selected_index += 1
    elif keys[pygame.K_UP] and selected_index > 0:
        selected_index -= 1

    
    pygame.display.flip()
    clock.tick(30) 

pygame.quit()
