# Here's a basic outline of the server initialization script (server_init.py)

import socket

def start_server(host='127.0.0.1', port=8080):
    """
    Starts a simple HTTP server listening on the specified host and port.
    """
    # Create a socket object using IPv4 and TCP protocol
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the host and port
    server_socket.bind((host, port))

    # Start listening for incoming connections, with a specified backlog
    server_socket.listen(5)
    print(f"Server started on {host}:{port}")

    # Accept connections in a loop (this will be later expanded to handle requests)
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection received from {client_address}")

        # Here we will later add the code to handle the request

        # Close the connection (this will be modified later to keep connection open as needed)
        client_socket.close()

    # This part will be reached when the server is shut down
    server_socket.close()

# This function can be called with custom host and port if needed
if __name__ == "__main__":
    start_server()  # Starts the server with default settings


