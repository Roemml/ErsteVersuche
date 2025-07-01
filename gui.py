#Python Imports
import tkinter as tk
#Eigene Imports
import sprites
import  Roemdules.gui as Roemgui
#Methoden
def startSpiel(fenster:tk.Tk) -> None:
    """
    Startet das Spiel nach Drücken auf "Start" Button.
    """
    fenster.destroy()
def start_fenster_schliessen(fenster:tk.Tk,game_state) -> None:
    """
    Startfenster schließen und somit Anwendung gleich beenden.
    """
    game_state.close()
    fenster.destroy()
def init_start_fenster(game_state) -> None:
    """
    Startfenster erzeugen und anzeigen.
    """
    fenster = Roemgui.erstelle_Fenster(
        {"type":"button", "text":"Start", "command":"startSpiel(fenster)", "width":5, "height":1, "align":Roemgui.ALIGN_CENTER}
        ,{"type":"label", "text":"Drücke auf Start zum Spiel starten", "align":Roemgui.ALIGN_CENTER}
        ,{"type":"label", "text":"Steuerung:", "align":Roemgui.ALIGN_LEFT}
        ,{"type":"label", "text":"Pfeiltasten: Bewegen", "align":Roemgui.ALIGN_LEFT}
        ,{"type":"label", "text":"Links STRG: Schießen", "align":Roemgui.ALIGN_LEFT}
        ,{"type":"label", "text":"P: Pause", "align":Roemgui.ALIGN_LEFT}
        ,{"type":"label", "text":"ESC oder Links ALT + Q: Spiel beenden", "align":Roemgui.ALIGN_LEFT}
        ,fenster_name = "Start", protocols = (("WM_DELETE_WINDOW", "start_fenster_schliessen(fenster,game_state)"),)
        ,context = {'game_state': game_state, 'start_fenster_schliessen': start_fenster_schliessen, 'startSpiel': startSpiel}
        )
    fenster.mainloop()
def init_game_done(game_state) -> None:
    """
    Game Over Screen anzeigen
    """
    if sprites.Ship.score > sprites.Ship.highscore:
        hs_text = "Das ist ein neuer Highscore!"
        sprites.set_new_highscore()
    else:
        hs_text = f"Highcore: {sprites.Ship.highscore}"
    fenster = Roemgui.erstelle_Fenster(
        {"type":"label", "text":"Herzlichen Glückwunsch!", "align":Roemgui.ALIGN_CENTER}
        ,{"type":"label", "text":f"Score: {sprites.Ship.score}", "align":Roemgui.ALIGN_CENTER}
        ,{"type":"label", "text":hs_text, "align":Roemgui.ALIGN_CENTER}
        ,{"type":"label", "text":"Vielen Dank für das Spielen von 2D Power!", "align":Roemgui.ALIGN_CENTER}
        ,{"type":"button", "text":"Start von Vorne", "command":"startSpiel(fenster)", "function":startSpiel, "width":15, "height":1, "align":Roemgui.ALIGN_CENTER}
        ,fenster_name = "Gewonnen",protocols = (("WM_DELETE_WINDOW", "start_fenster_schliessen(fenster,game_state)"),)
        ,context = {'game_state': game_state, 'start_fenster_schliessen': start_fenster_schliessen, 'startSpiel': startSpiel}
        )
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
    fenster = Roemgui.erstelle_Fenster(
        {"type":"label", "text":"Game Over", "align":Roemgui.ALIGN_CENTER}
        ,{"type":"label", "text":f"Score: {sprites.Ship.score}", "align":Roemgui.ALIGN_CENTER}
        ,{"type":"label", "text":hs_text, "align":Roemgui.ALIGN_CENTER}
        ,{"type":"label", "text":"Vielen Dank für das Spielen von 2D Power!", "align":Roemgui.ALIGN_CENTER}
        ,fenster_name = "Game Over"
        )
    fenster.mainloop()