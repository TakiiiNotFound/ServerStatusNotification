import time
import platform
import subprocess
import pygame
import os
import sys
from colorama import init, Fore, Back, Style

# config
AUDIO_UP = "up.wav"
AUDIO_DOWN = "down.wav"
CHECK_INTERVAL = 10 #values = seconde
IP_FILE = "ip.txt" #file located inside the script folder

# some shit logic below
pygame.mixer.init()
init(autoreset=True)

def clear_console():
    os.system('cls' if platform.system().lower() == 'windows' else 'clear') # because pygame is a pain

def read_ip():
    try:
        with open(IP_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"Error: '{IP_FILE}' not found. create it yourself") 
        sys.exit(1)

def play_audio(file_path):
    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    except Exception as e:
        print(f"Error playing audio: {e}")

def is_server_up(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        result = subprocess.run(["ping", param, "1", ip],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
        return result.returncode == 0
    except Exception as e:
        print(f"Ping failed: {e}")
        return False

def print_status(is_up):
    if is_up:
        text = Back.GREEN + Fore.WHITE + Style.BRIGHT + "  STATUS: UP   "
    else:
        text = Back.RED + Fore.WHITE + Style.BRIGHT + "  STATUS: DOWN "
    
    sys.stdout.write('\r' + text + Style.RESET_ALL)
    sys.stdout.flush()

# loop loop loopy ##i need mantal help
def main():
    clear_console()
    ip_address = read_ip()
    last_status = None
    print("Monitoring server:", ip_address)

    while True:
        is_up = is_server_up(ip_address)

        if is_up and last_status != True:
            play_audio(AUDIO_UP)
        elif not is_up and last_status != False:
            play_audio(AUDIO_DOWN)

        print_status(is_up)
        last_status = is_up
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
