#Global Imports
import pygame
import threading
# Globale Variablen
stop__music_event = threading.Event()
pause_music_event = threading.Event()
resume_music_event = threading.Event()
def play_music(mp3_file, stop_music_event, pause_music_event, resume_music_event) -> None:
    """
    Hintergrundmusik Spieler im Loop.
    """
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_file)
    pygame.mixer.music.play(-1)  # Loop indefinitely
    while not stop_music_event.is_set():
        if pause_music_event.is_set():
            pygame.mixer.music.pause()
            pause_music_event.clear()
        elif resume_music_event.is_set():
            pygame.mixer.music.unpause()
            resume_music_event.clear()
        pygame.time.Clock().tick(10)  # Check the stop event periodically
    try:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    except:
        pass
def start_music() -> None:
    """
    Startet die Hintergrundmusik.
    """
    global mp3_thread
    mp3_file = 'mhb.mp3'
    stop__music_event.clear()
    mp3_thread = threading.Thread(target = play_music, args = (mp3_file, stop__music_event, pause_music_event, resume_music_event))
    mp3_thread.start()
def end_music() -> None:
    """
    Beendet die Hintergrundmusik.
    """
    stop__music_event.set()
    mp3_thread.join()
def pause_music() -> None:
    """
    Pausiert die Hintergrundmusik.
    """
    pause_music_event.set()
def resume_music() -> None:
    """
    Hintergrundmusik wird wieder fortgesetzt.
    """
    resume_music_event.set()