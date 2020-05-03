import threading
import sys
from os import system

def run(command):
    system(command);

if __name__ == "__main__":
    commands = ' '.join(sys.argv[1:]).split('//')
    commands = [command.strip() for command in commands]
    threads = []
    for command in commands:
        thread = threading.Thread(group=None, target=run, name=command, args=(command,), daemon=True)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
