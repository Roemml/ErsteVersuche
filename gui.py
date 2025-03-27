import tkinter as tk

import sprites

ALIGN_LEFT = "0"
ALIGN_CENTER = "1"

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
    """
    Parst einen geometry String (WIDTHxHEIGHT+X+Y) in ein Tupel (WIDTH,HEIGHT) 
    """
    split = geometry.split("x")
    return (int(split[0]), split[1].split("+")[0])
#111 last line

def erstelle_Fenster(fenster_name:str="Fenster",fenster_breite:int=0,fenster_hoehe:int=0,protocols:tuple[tuple[str,str]]=None,*widgets:dict) -> tk.Tk:
    """
    Erstellt dynamisch ein Fenster in der Mitte des aktuellen Bildschirms.

    ACHTUNG: die Funktionen für Protokolle und Buttons muss man natürlich selber schreiben
    Argumente:
        fenster_name - String: So wird das Fenster heißen
        fenster_breite - Integer: Breite des Fensters in Pixel, wenn nicht mitgegeben oder 0, oder nicht alles drauf passt, wird die Größe berechnet.
        fenster_hoehe - Integer: Höhe des Fensters in Pixel, wenn nicht mitgegeben oder 0, oder nicht alles drauf passt, wird die Größe berechnet.
        protocola - Tupel(String,String) Name des protokolls und Name der Funktion
        widget - Dictionary - Für jedes Element auf dem Fenster von Oben bis unten ein Dictionary, dass das Element beschreibt
    """
    fenster = tk.Tk()
    fenster.title = fenster_name
    min_breite = 0
    min_hoehe = 0
    elemente :tuple[tk.Widget] = []
    
    for protocol in protocols:
        try:
            fenster.protocol(protocol[0], protocol[1])
        except Exception as e:
            print(f"Protokoll {protocol} für Fenster {fenster_name} konnte nicht erstellt werden: {e}")
    for widget in widgets:
        if not ("Type" in widget): print(f"widget {widget} hat keinen Eintrag für Type")
        if widget["Type"] == "Space": 
            try: min_hoehe += int(widget["Space"])
            except Exception as e: print(f"Fehler beim Space erstellen: {e}")
        elif widget["Type"] == "Label": 
            try:
                element, min_hoehe, element_breite = __fenster_label(widget)
                if element_breite > min_breite: min_breite = element_breite
                elemente.append(element)
            except Exception as e:
                print(f"Fehler beim Label erstellen: {e}")
        elif widget["Type"] == "Button":
            try:
                element, min_hoehe, element_breite = __fenster_button(widget)
                if element_breite > min_breite: min_breite = element_breite
                elemente.append(element)
            except Exception as e:
                print(f"Fehler beim Button erstellen: {e}")
        
def __fenster_label(widget:dict,current_height:int)->tuple[tk.Label,int,int]: ...
def __fenster_button(widget:dict,current_height:int)->tuple[tk.Button,int,int]: ...