import pygame
import threading

# Create a stop event
stop_event = threading.Event()
pause_event = threading.Event()
resume_event = threading.Event()

def play_music(mp3_file, stop_event, pause_event, resume_event) -> None:
    """
    Hintergrundmusik Spieler im Loop.
    """
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_file)
    pygame.mixer.music.play(-1)  # Loop indefinitely

    while not stop_event.is_set():
        if pause_event.is_set():
            pygame.mixer.music.pause()
            pause_event.clear()
        elif resume_event.is_set():
            pygame.mixer.music.unpause()
            resume_event.clear()
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
    stop_event.clear()
    mp3_thread = threading.Thread(target=play_music, args=(mp3_file, stop_event, pause_event, resume_event))
    mp3_thread.start()

def end_music() -> None:
    """
    Beendet die Hintergrundmusik.
    """
    stop_event.set()
    mp3_thread.join()

def pause_music() -> None:
    """
    Pausiert die Hintergrundmusik.
    """
    pause_event.set()

def resume_music() -> None:
    """
    Hintergrundmusik wird wieder fortgesetzt.
    """
    resume_event.set()