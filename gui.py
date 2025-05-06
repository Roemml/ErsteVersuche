#Python Imports
import tkinter as tk
#Eigene Imports
import sprites
#Globalle Konstanzen
ALIGN_LEFT = "0"
ALIGN_CENTER = "1"
#Globale Variablen
#Methoden
def startSpiel(fenster:tk.Tk) -> None:
    """
    Startet das Spiel nach Drücken auf "Start" Button.
    """
    fenster.destroy()
def start_fenster_schliessen(fenster:tk.Tk) -> None:
    """
    Startfenster schließen und somit Anwendung gleich beenden.
    """
    sprites.state = sprites.STATE_CLOSE
    fenster.destroy()
def init_start_fenster() -> None:
    """
    Startfenster erzeugen und anzeigen.
    """
    fenster = erstelle_Fenster({"type":"button", "text":"Start", "command":"startSpiel(fenster)", "width":5, "height":1, "align":ALIGN_CENTER}
                             ,{"type":"label", "text":"Drücke auf Start zum Spiel starten", "align":ALIGN_CENTER}, {"type":"label", "text":"Steuerung:", "align":ALIGN_LEFT}
                             ,{"type":"label", "text":"Pfeiltasten: Bewegen", "align":ALIGN_LEFT}, {"type":"label", "text":"Links STRG: Schießen", "align":ALIGN_LEFT}
                             ,{"type":"label", "text":"P: Pause:", "align":ALIGN_LEFT}, {"type":"label", "text":"ESC oder Links ALT + Q: Spiel beenden", "align":ALIGN_LEFT}
                             ,fenster_name = "Start", protocols = (("WM_DELETE_WINDOW", "start_fenster_schliessen(fenster)"),))
    fenster.mainloop()
def init_pause() -> None:
    """
    Zeigt das Pause Fenster.
    """
    fenster=erstelle_Fenster({"type":"label", "text":"Pause", "align":ALIGN_CENTER}, {"type":"label", "text":"Zum Weiter spielen Fenster schließen", "align":ALIGN_CENTER}, fenster_name = "Pause")
    fenster.mainloop()
def init_game_done() -> None:
    """
    Game Over Screen anzeigen
    """
    if sprites.Ship.score > sprites.Ship.highscore:
        hs_text = "Das ist ein neuer Highscore!"
        sprites.set_new_highscore()
    else:
        hs_text = f"Highcore: {sprites.Ship.highscore}"
    fenster = erstelle_Fenster({"type":"label", "text":"Herzlichen Glückwunsch!", "align":ALIGN_CENTER}, {"type":"label", "text":f"Score: {sprites.Ship.score}", "align":ALIGN_CENTER}
                             ,{"type":"label", "text":hs_text, "align":ALIGN_CENTER}, {"type":"label", "text":"Vielen Dank für das Spielen von 2D Power!", "align":ALIGN_CENTER}
                             ,{"type":"button", "text":"Start von Vorne", "command":"startSpiel(fenster)", "width":15, "height":1, "align":ALIGN_CENTER}
                             ,fenster_name = "Gewonnen",protocols = (("WM_DELETE_WINDOW", "start_fenster_schliessen(fenster)"),))
    fenster.mainloop()
def init_game_over() -> None:
    """
    Game Over Screen anzeigen
    """
    if sprites.Ship.score > sprites.Ship.highscore:
        hs_text = "Das ist ein neuer Highscore!"
        sprites.set_new_highscore()
    else:
        hs_text = f"Highcore: {sprites.Ship.highscore}"
    fenster = erstelle_Fenster({"type":"label", "text":"Game Over", "align":ALIGN_CENTER}, {"type":"label", "text":f"Score: {sprites.Ship.score}", "align":ALIGN_CENTER}
                             ,{"type":"label", "text":hs_text, "align":ALIGN_CENTER}, {"type":"label", "text":"Vielen Dank für das Spielen von 2D Power!", "align":ALIGN_CENTER}, fenster_name = "Game Over")
    fenster.mainloop()
def parse_geometry(geometry:str) -> tuple[int,int]:
    """
    Parst einen geometry String (WIDTHxHEIGHT+X+Y) in ein Tupel (WIDTH,HEIGHT) 
    """
    split=geometry.split("x")
    return (int(split[0]), split[1].split("+")[0])
def erstelle_Fenster(*widgets:dict, fenster_name:str = "Fenster", fenster_breite:int = 0, fenster_hoehe:int = 0, protocols:tuple[tuple[str, str]] = None) -> tk.Tk:
    """
    Erstellt dynamisch ein Fenster in der Mitte des aktuellen Bildschirms.

    ACHTUNG: die Funktionen für Protokolle und Buttons muss man natürlich selber schreiben.\n
    für protocol und command wird automatisch ein lambda erstellt, an den beiden Stellen nur die Funktion mit Parameter übergeben

    Argumente:
        fenster_name - String: So wird das Fenster heißen
        fenster_breite - Integer: Breite des Fensters in Pixel, wenn nicht mitgegeben oder 0, oder nicht alles drauf passt, wird die Größe berechnet.
        fenster_hoehe - Integer: Höhe des Fensters in Pixel, wenn nicht mitgegeben oder 0, oder nicht alles drauf passt, wird die Größe berechnet.
        protocol - Tupel(String,String) Name des protokolls und Name der Funktion. die Funktion wird automatisch mit Lambda aufgerufen für Parameter
        widget - Dictionary - Für jedes Element auf dem Fenster von Oben bis unten ein Dictionary, dass das Element beschreibt
    """
    fenster = tk.Tk()
    fenster.title = fenster_name
    min_breite = 0
    min_hoehe = 0
    elemente:tuple[tuple[tk.Widget,int]] = []
    if not protocols == None:
        for protocol in protocols:
            try:
                if protocol[1].find("(") != -1:
                    procdict = {}
                    einzel_argument = ""
                    protocol_funktion = protocol[1]
                    protocol_funktion = protocol_funktion.lstrip()
                    for char in protocol_funktion:
                        if str(char).isalnum() or str(char) == "_":
                            einzel_argument += str(char)
                        elif einzel_argument != "":
                            procdict[einzel_argument] = eval(einzel_argument)
                            einzel_argument=""
                    fenster.protocol(protocol[0], lambda pc=protocol,pd=procdict: eval(pc[1], pd))    
                else:
                    fenster.protocol(protocol[0], lambda pc=protocol: eval(pc[1]))
            except Exception as e:
                print(f"Protokoll {protocol} für Fenster {fenster_name} konnte nicht erstellt werden: {e}")
    for widget in widgets:
        if not ("type" in widget): print(f"widget {widget} hat keinen Eintrag für Type")
        if widget["type"] == "space": 
            try: min_hoehe += int(widget["space"])
            except Exception as e: print(f"Fehler beim Space erstellen: {e}")
        elif widget["type"] == "label": 
            try:
                element = tk.Label(fenster, text = widget["text"])
                element_top=min_hoehe
                min_hoehe+=element.winfo_reqheight()
                if element.winfo_reqwidth()>min_breite:min_breite=element.winfo_reqwidth()
                if "align" in widget: align = widget["align"]
                else: align = ALIGN_CENTER
                elemente.append((element, element_top, align))
            except Exception as e:
                print(f"Fehler beim Label erstellen: {e}")
        elif widget["type"] == "button":
            try:
                if widget["command"].find("(") != -1:
                    comdict = {}
                    einzel_argument = ""
                    command_funktion = widget["command"]
                    command_funktion = command_funktion.lstrip()
                    for char in command_funktion:
                        if str(char).isalnum() or str(char) == "_":
                            einzel_argument += str(char)
                        elif einzel_argument  != "":
                            comdict[einzel_argument] = eval(einzel_argument)
                            einzel_argument = ""
                    element = tk.Button(fenster, text = widget["text"], command = lambda wc = widget["command"], cd = comdict: eval(wc, cd), width = widget["width"], height = widget["height"])
                else:
                    element = tk.Button(fenster, text = widget["text"], command = lambda wc = widget["command"]: eval(wc), width=widget["width"], height = widget["height"])
                element_top = min_hoehe
                min_hoehe += element.winfo_reqheight()
                if element.winfo_reqwidth() > min_breite: min_breite = element.winfo_reqwidth()
                if element.winfo_reqwidth() > min_breite: min_breite = element.winfo_reqwidth()
                if "align" in widget: align = widget["align"]
                elemente.append((element, element_top, align))
            except Exception as e:
                print(f"Fehler beim Button erstellen: {e}")
        else:
            print(f"{widget["type"]} ist kein gültuger Widget typ")
    if min_breite > fenster_breite:
        fenster_breite = min_breite
    if min_hoehe > fenster_hoehe:
        fenster_hoehe = min_hoehe
    for element in elemente:
        if element[2] == ALIGN_CENTER: element[0].place(x = (fenster_breite - element[0].winfo_reqwidth()) // 2, y = element[1])
        elif element[2] == ALIGN_LEFT: element[0].place(x = 0, y = element[1])
    fenster.geometry(f"{fenster_breite}x{fenster_hoehe}+{(fenster.winfo_screenwidth() - fenster_breite) // 2}+{(fenster.winfo_screenheight() - fenster_hoehe) // 2}")
    return fenster