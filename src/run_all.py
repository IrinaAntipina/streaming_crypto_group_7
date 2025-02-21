import subprocess
import time

def run_process(command):
    """ Kör ett kommando som en separat process. """
    return subprocess.Popen(command, shell=True)

def wait_for_postgres(host="localhost", port=5432, retries=10, delay=3):
    """ Väntar tills PostgreSQL är redo att ta emot anslutningar. """
    import socket
    for i in range(retries):
        try:
            with socket.create_connection((host, port), timeout=2):
                print(f"✅ PostgreSQL är redo!")
                return True
        except (OSError, ConnectionRefusedError):
            print(f"⏳ Väntar på PostgreSQL... ({i+1}/{retries})")
            time.sleep(delay)
    print("❌ PostgreSQL startade inte i tid.")
    return False

# 1. Starta Docker
print("🚀 Startar Docker containers...")
dockerUP = run_process("docker compose up -d")
dockerUP.wait()

# 2. Vänta tills PostgreSQL är redo
if not wait_for_postgres():
    exit(1)  # Avbryt om PostgreSQL inte startar

# 3. Starta producenter
print("▶️ Startar producenter...")
producer1 = run_process("python src/producer.py")
producer2 = run_process("python src/producer_s.py")

# 4. Starta konsumenter
print("▶️ Startar konsumenter...")
consumer1 = run_process("python src/consumer.py")
consumer2 = run_process("python src/consumer_s.py")

time.sleep(10)
dashboard = run_process("streamlit run src/dashboard.py")

# Vänta på att alla processer ska köra klart
producer1.wait()
producer2.wait()
consumer1.wait()
consumer2.wait()