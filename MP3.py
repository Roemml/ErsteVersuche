import pygame
import threading

# Create a stop event
stop_event = threading.Event()

def play_mp3(mp3_file, stop_event):
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_file)
    pygame.mixer.music.play(-1)  # Loop indefinitely

    while not stop_event.is_set():
        pygame.time.Clock().tick(10)  # Check the stop event periodically
    try:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    except:
        pass


def start_mp3():
    global mp3_thread
    mp3_file = 'mhb.mp3'
    stop_event.clear()
    mp3_thread = threading.Thread(target=play_mp3, args=(mp3_file, stop_event))
    mp3_thread.start()

def end_mp3():
    stop_event.set()
    mp3_thread.join()
