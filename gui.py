import tkinter as tk

import sprites

starten: bool = True

# Funktion, die beim Drücken des Buttons aufgerufen wird
def startSpiel(fenster: tk.Tk) -> None:
    """
    Startet das Spiel nach Drücken auf "Start" Button.
    """
    fenster.destroy()
def start_fenster_schliessen(fenster: tk.Tk) -> None:
    """
    Startfenster schließen und somit Anwendung gleich beenden.
    """
    global starten
    starten = False
    fenster.destroy()

def init_start_fenster() -> None:
    """
    Startfenster erzeugen und anzeigen.
    """
    # Erstelle das Hauptfenster
    fenster = tk.Tk()
    fenster.title("Start")
    tkwidth = 220
    tkheight = 0

    # Erstelle den Button und platziere ihn
    start_button = tk.Button(fenster, text="Start", command=lambda: startSpiel(fenster), width=5, height=1)
    tkheight += 5
    start_button.place(x = (tkwidth - start_button.winfo_reqwidth())//2, y = tkheight); tkheight += start_button.winfo_reqheight() + 5

    # Erstelle label
    label = tk.Label(fenster, text="Drücke auf Start zum Spiel starten")
    label.place(x=(tkwidth - label.winfo_reqwidth())//2, y=tkheight); tkheight += label.winfo_reqheight()
    label = tk.Label(fenster, text="Steuerung:")
    label.place(x=(tkwidth - label.winfo_reqwidth())//2, y=tkheight); tkheight += label.winfo_reqheight()
    label = tk.Label(fenster, text="Pfeiltasten: Bewegen")
    label.place(x=0, y=tkheight); tkheight += label.winfo_reqheight()
    label = tk.Label(fenster, text="Links STRG: Schießen")
    label.place(x=0, y=tkheight); tkheight += label.winfo_reqheight()
    label = tk.Label(fenster, text="P: Pause")
    label.place(x=0, y=tkheight); tkheight += label.winfo_reqheight()
    label = tk.Label(fenster, text="ESC oder Links ALT + Q: Spiel beenden")
    label.place(x=0, y=tkheight); tkheight += label.winfo_reqheight()

    # Setze die Fenstergröße
    fenster.geometry(f"{tkwidth}x{tkheight}+{(fenster.winfo_screenwidth()-tkwidth)//2}+{(fenster.winfo_screenheight()-tkheight)//2}")

    # Setze die Funktion für das Schließen des Fensters
    fenster.protocol("WM_DELETE_WINDOW", lambda: start_fenster_schliessen(fenster))

    # Starte die Anwendung
    fenster.mainloop()
def init_pause() -> None:
    """
    Zeigt das Pause Fenster.
    """
     # Erstelle das Hauptfenster
    fenster = tk.Tk()
    fenster.title("Pause")
    tkwidth = 220
    tkheight = 0


    # Erstelle label
    label = tk.Label(fenster, text="Pause")
    label.place(x=(tkwidth - label.winfo_reqwidth())//2, y=tkheight); tkheight += label.winfo_reqheight()
    label = tk.Label(fenster, text="Zum Weiter spielen Fenster schließen")
    label.place(x=(tkwidth - label.winfo_reqwidth())//2, y=tkheight); tkheight += label.winfo_reqheight()

    # Setze die Fenstergröße
    fenster.geometry(f"{tkwidth}x{tkheight}+{(fenster.winfo_screenwidth()-tkwidth)//2}+{(fenster.winfo_screenheight()-tkheight)//2}")
    # Starte die Anwendung
    fenster.mainloop()

def init_game_over() -> None:
    """
    Game Over Screen anzeigen
    """
     # Erstelle das Hauptfenster
    fenster = tk.Tk()
    fenster.title("Game Over")
    tkwidth = 250
    tkheight = 0

    # Erstelle label
    label = tk.Label(fenster, text="Game Over")
    label.place(x=(tkwidth - label.winfo_reqwidth())//2, y=tkheight); tkheight += label.winfo_reqheight()
    label = tk.Label(fenster, text=f"Score: {sprites.score}")
    label.place(x=(tkwidth - label.winfo_reqwidth())//2, y=tkheight); tkheight += label.winfo_reqheight()
    if sprites.score > sprites.highscore:
        label = tk.Label(fenster, text="Das ist ein neuer Highscore!")
        label.place(x=(tkwidth - label.winfo_reqwidth())//2, y=tkheight); tkheight += label.winfo_reqheight()
        sprites.set_new_highscore()
    else:
        label = tk.Label(fenster, text=f"Highcore: {sprites.highscore}")
        label.place(x=(tkwidth - label.winfo_reqwidth())//2, y=tkheight); tkheight += label.winfo_reqheight()
    label = tk.Label(fenster, text="Vielen Dank für das Spielen von 2D Power!")
    label.place(x=(tkwidth - label.winfo_reqwidth())//2, y=tkheight); tkheight += label.winfo_reqheight()
    # Setze die Fenstergröße
    fenster.geometry(f"{tkwidth}x{tkheight}+{(fenster.winfo_screenwidth()-tkwidth)//2}+{(fenster.winfo_screenheight()-tkheight)//2}")
    # Starte die Anwendung
    fenster.mainloop()

def parse_geometry(geometry: str) -> tuple[int, int]:
    split = geometry.split("x")
    return (int(split[0]), split[1].split("+")[0])

    