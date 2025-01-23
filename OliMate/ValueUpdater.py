import pandas as pd
import time
import threading
import os
# Funzione per colori nel terminale
RED = "\033[31m"
GREEN = "\033[32m"
CYAN = "\033[36m"
RESET = "\033[0m"

# ASCII Art per titoli
def print_title():
    os.system("cls" if os.name == "nt" else "clear")  # Pulisce la console
    print(f"""
{CYAN}

██╗██╗         ██╗  ██╗ █████╗ ███╗   ███╗██╗   ██╗███████╗
██║██║         ██║ ██╔╝██╔══██╗████╗ ████║╚██╗ ██╔╝╚══███╔╝
██║██║         █████╔╝ ███████║██╔████╔██║ ╚████╔╝   ███╔╝ 
██║██║         ██╔═██╗ ██╔══██║██║╚██╔╝██║  ╚██╔╝   ███╔╝  
██║███████╗    ██║  ██╗██║  ██║██║ ╚═╝ ██║   ██║   ███████╗
╚═╝╚══════╝    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝   ╚═╝   ╚══════╝
                                                           
 
                                            
{RESET}

{CYAN}>> Simulatore di Problemi v1.0 - IL KAMYZ 🚀 <<{RESET} 
    """)

class Problema:
    def __init__(self, valore):
        self.solved = False  # Se è stato risolto
        self.valore = valore  # Valore del problema

    def incrementa(self, incremento):
        if not self.solved:
            self.valore += incremento  # Incrementa solo se non è risolto

    def __repr__(self):
        return f"Problema(valore={self.valore}, solved={self.solved})"

# Funzione per incrementare i problemi
def Incremento(problemi, incremento):
    for problema in problemi:
        problema.incrementa(incremento)

# Funzione per ottenere input numerici
def get_int_input(prompt):
    while True:
        try:
            return int(input(f"{CYAN}{prompt}{RESET} "))
        except ValueError:
            print(f"{RED}Pensi che so scemo? Inserisci un numero intero.{RESET}")

# Funzione per segnare i problemi risolti
def segna_problemi_risolti(problemi):
    while True:
        numero = input(f"{CYAN}Inserisci il numero del problema risolto (0 per uscire): {RESET}")
        if numero == "0":
            print(f"{CYAN}Chiusura della risoluzione dei problemi...{RESET}")
            break  # Esce dal loop

        if numero.isdigit():
            numero = int(numero)
            if 1 <= numero <= len(problemi):
                if not problemi[numero - 1].solved:
                    problemi[numero - 1].solved = True
                    print(f"{GREEN}✅ Problema {numero} risolto! 🚀{RESET}")
                else:
                    print(f"{CYAN}⚠️ Il problema {numero} era già risolto.{RESET}")
            else:
                print(f"{RED}Numero non valido!{RESET}")
        else:
            print(f"{RED}Inserisci un numero valido!{RESET}")

# Stampa tabella problemi
def print_problems_table(problemi):
    os.system("cls" if os.name == "nt" else "clear")  # Pulisce la console
    print_title()

    dati = []
    for i, problema in enumerate(problemi, start=1):
        stato = f"{GREEN}✔ Risolto{RESET}" if problema.solved else f"{RED}❌ Non risolto{RESET}"
        dati.append([i, problema.valore, stato])

    df = pd.DataFrame(dati, columns=["Numero Problema", "Valore", "Stato"])
    print(df.to_string(index=False))

# Ottenere i parametri dall'utente
print_title()
numero_problemi = get_int_input("Quanti problemi ci sono:")
valore_problemi = get_int_input("Quanto vale inizialmente un problema:")
incremento_problemi = get_int_input("Inserisci l'incremento:")
intervallo_incremento = get_int_input("Ogni quanto avviene l'incremento? (Secondi):")

# Creazione problemi
Problemi = [Problema(valore_problemi) for _ in range(numero_problemi)]

# Avvio del thread per risolvere problemi
thread_risoluzione = threading.Thread(target=segna_problemi_risolti, args=(Problemi,))
thread_risoluzione.daemon = True  # Il thread si chiude quando il programma principale termina
thread_risoluzione.start()

# Ciclo principale di incremento
while True:
    Incremento(Problemi, incremento_problemi)  # Incrementa solo quelli non risolti

    print_problems_table(Problemi)  # Stampa la tabella aggiornata
    time.sleep(intervallo_incremento)  # Aspetta il tempo specificato prima del prossimo incremento
