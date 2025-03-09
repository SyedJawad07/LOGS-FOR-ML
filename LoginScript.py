import paramiko
import time
import threading

# Server Details (Replace with your actual server details)
HOST = "10.10.90.102"
USERNAME = "wash"
PASSWORD = "wash"

# Flag to stop the script
running = True

def ssh_connect():
    global running
    while running:
        try:
            print("\n[+] Connecting to server...")
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(HOST, username=USERNAME, password=PASSWORD, timeout=10)

            print("[✅] Connected to the server!")

            # Open an interactive shell session
            shell = ssh.invoke_shell()

            # Print to indicate we are in the server terminal
            print("[❗] Server terminal is active. Wait for 30 seconds...")

            # Wait for 30 seconds on the server
            time.sleep(30)

            # Send the exit command to disconnect from the server
            print("[❌] Sending 'exit' command to the server...")
            shell.send("exit\n")

            # Wait a bit for the exit command to take effect
            time.sleep(2)

            print("[❌] Disconnected from server.")
            # The terminal will return to the local machine's prompt

            # Wait for 3 minutes before reconnecting
            for remaining in range(180, 0, -1):
                if not running:
                    print("\n[⛔] Stopping the script...")
                    return
                time.sleep(1)

        except Exception as e:
            print(f"[⚠] SSH Connection Failed: {e}")
            time.sleep(10)  # Wait 10 sec before retrying

# Function to listen for Shift + Esc key to stop script permanently
def listen_for_stop():
    global running
    import keyboard
    keyboard.wait("shift+esc")
    running = False
    print("\n[⛔] Stopping SSH script permanently...")

# Start listening for the stop key in a separate thread
stop_thread = threading.Thread(target=listen_for_stop, daemon=True)
stop_thread.start()

# Run the SSH function
ssh_connect()