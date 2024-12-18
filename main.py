import itertools
import string
import threading
import time

# The target password (for testing purposes)
target_password = "abc"

# Define the character set (lowercase letters + digits)
charset = string.ascii_lowercase + string.digits

# This will store the found password once it's cracked
password_found = None
lock = threading.Lock()

# Function to perform brute-force cracking
def brute_force_cracker(start_index, charset, target_password, password_length):
    global password_found
    for guess in itertools.product(charset, repeat=password_length):
        guess_password = ''.join(guess)
        if guess_password == target_password:
            with lock:  # Ensure only one thread updates the result
                password_found = guess_password
                print(f"Password found: {guess_password}")
                return

# Function to manage threads
def run_threads(target_password, charset):
    global password_found
    password_length = len(target_password)

    # Set the number of threads to use
    num_threads = 4
    threads = []

    # Divide the charset into chunks and assign each chunk to a thread
    chunk_size = len(charset) // num_threads

    for i in range(num_threads):
        start_index = i * chunk_size
        thread = threading.Thread(target=brute_force_cracker, args=(start_index, charset, target_password, password_length))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    if password_found:
        print(f"Password cracked: {password_found}")
    else:
        print("Password not found.")

# Timing the process
start_time = time.time()
run_threads(target_password, charset)
end_time = time.time()

print(f"Cracking took {end_time - start_time:.2f} seconds.")
