import pandas as pd

class GaraMatematica:
    def __init__(self, squadre, num_problemi):
        self.num_problemi = num_problemi
        self.squadre = {squadra: {"punteggio": num_problemi * 10, "problema_jolly": None} for squadra in squadre}
        self.problemi = {i: 20 for i in range(1, num_problemi + 1)}
        self.risposte_giuste = {i: [] for i in range(1, num_problemi + 1)}

    def assegna_problema_jolly(self, squadra, problema):
        """ Assegna il problema jolly alla squadra """
        self.squadre[squadra]["problema_jolly"] = problema

    def aggiorna_punteggio(self, squadra, problema, risposta_corretta):
        """ Aggiorna il punteggio in base alla risposta fornita """
        if risposta_corretta:
            posizione = len(self.risposte_giuste[problema])
            bonus = [20, 15, 10, 8, 6, 5, 4, 3, 2, 1]
            punti_ottenuti = self.problemi[problema] + (bonus[posizione] if posizione < len(bonus) else 0)
            self.risposte_giuste[problema].append(squadra)
        else:
            punti_ottenuti = -10  # Penalità per risposta sbagliata

        # Raddoppia se è il problema jolly
        if self.squadre[squadra]["problema_jolly"] == problema:
            punti_ottenuti *= 2

        self.squadre[squadra]["punteggio"] += punti_ottenuti

    def visualizza_classifica(self):
        """ Mostra la classifica delle squadre usando Pandas (stampa su console) """
        df = pd.DataFrame([
            {"Squadra": squadra, "Punteggio": dati["punteggio"]}
            for squadra, dati in self.squadre.items()
        ]).sort_values(by="Punteggio", ascending=False)

        print("\n=== CLASSIFICA ===")
        print(df.to_string(index=False))  # Stampa la classifica in tabella

# Esempio di utilizzo
squadre = ["Squadra A", "Squadra B", "Squadra C"]
num_problemi = 10

gara = GaraMatematica(squadre, num_problemi)

# Assegna problemi jolly
gara.assegna_problema_jolly("Squadra A", 3)
gara.assegna_problema_jolly("Squadra B", 5)
gara.assegna_problema_jolly("Squadra C", 7)

# Simula risposte
gara.aggiorna_punteggio("Squadra A", 3, True)
gara.aggiorna_punteggio("Squadra B", 5, False)
gara.aggiorna_punteggio("Squadra C", 7, True)
gara.aggiorna_punteggio("Squadra B", 2, True)
gara.aggiorna_punteggio("Squadra A", 1, False)

# Visualizza classifica
gara.visualizza_classifica()
