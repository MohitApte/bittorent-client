# Here's a basic outline of the request handler script (request_handler.py)

def parse_request(client_socket):
    """
    Parses the HTTP request from the client socket.
    """
    # Read the request from the socket (assuming a small request for simplicity)
    request_data = client_socket.recv(1024).decode('utf-8')
    # Split the request into lines
    lines = request_data.split('\r\n')

    # Extract the request line (first line)
    request_line = lines[0]
    # Split the request line into its components (Method, URI, HTTP Version)
    method, uri, http_version = request_line.split(' ')

    # Extract headers (all lines until the first empty line)
    headers = {}
    for line in lines[1:]:
        if line == '':  # End of headers
            break
        header, value = line.split(': ')
        headers[header] = value

    # Body (if any) will be after an empty line following headers
    body_index = lines.index('') + 1
    body = '\n'.join(lines[body_index:]) if body_index < len(lines) else ''

    # Return the parsed components
    return {
        'method': method,
        'uri': uri,
        'http_version': http_version,
        'headers': headers,
        'body': body
    }

# This function will be used in the server script to handle requests
# For now, it just prints the parsed request for demonstration
def handle_request(client_socket):
    request = parse_request(client_socket)
    print("Received Request:")
    print(request)  # In the actual implementation, this will be replaced with response generation logic


