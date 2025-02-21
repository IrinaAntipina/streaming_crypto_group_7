import subprocess
import time

def run_process(command):
    return subprocess.Popen(command, shell=True)

producer1 = run_process("python src/producer.py")
producer2 = run_process("python src/producer_s.py")

consumer1 = run_process("python src/consumer.py")
consumer2 = run_process("python src/consumer_s.py")

# time.sleep(10)
# dashboard = run_process("streamlit run src/dashboard.py")

producer1.wait()
producer2.wait()
consumer1.wait()
consumer2.wait()
#dashboard.wait()
