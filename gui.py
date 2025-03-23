import tkinter as tk

fenster: tk.Tk = None
starten: bool = True

# Funktion, die beim Drücken des Buttons aufgerufen wird
def startGame():
    global fenster
    fenster.destroy()
def start_fenster_schliessen():
    global starten, fenster
    starten = False
    fenster.destroy()

def init_menu():
    global fenster
    # Erstelle das Hauptfenster
    fenster = tk.Tk()
    fenster.title("Start")

    # Setze die Fenstergröße
    fenster.geometry("220x160")

    # Erstelle den Button und platziere ihn
    start_button = tk.Button(fenster, text="Start", command=startGame, width=5, height=1)
    start_button.place(x = 90, y = 5)

    # Erstelle label
    label = tk.Label(fenster, text="Drücke auf Start zum Spiel starten")
    label.place(x=0, y=35)
    label = tk.Label(fenster, text="Steuerung:")
    label.place(x=0, y=55)
    label = tk.Label(fenster, text="Pfeiltasten: Bewegen")
    label.place(x=0, y=75)
    label = tk.Label(fenster, text="Links STRG: Schießen")
    label.place(x=0, y=95)
    label = tk.Label(fenster, text="P: Pause")
    label.place(x=0, y=115)
    label = tk.Label(fenster, text="ESC oder Links ALT + Q: Spiel beenden")
    label.place(x=0, y=135)


    # Setze die Funktion für das Schließen des Fensters
    fenster.protocol("WM_DELETE_WINDOW", start_fenster_schliessen)

    # Starte die Anwendung
    fenster.mainloop()
def init_pause():
    global fenster
     # Erstelle das Hauptfenster
    fenster = tk.Tk()
    fenster.title("Pause")

    # Setze die Fenstergröße
    fenster.geometry("220x50")

    # Erstelle label
    label = tk.Label(fenster, text="Pause")
    label.place(x=90, y=5)
    label = tk.Label(fenster, text="Zum Weiter spielen Fenster schließen")
    label.place(x=0, y=25)
    # Starte die Anwendung
    fenster.mainloop()