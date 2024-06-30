# Here's a basic outline of the response builder script (response_builder.py)

def build_response(status_code, body='', headers=None):
    """
    Builds an HTTP response with the given status code, body, and optional headers.
    """
    # Standard HTTP response line
    http_version = "HTTP/1.1"
    status_messages = {
        200: "OK",
        404: "Not Found",
        500: "Internal Server Error"
    }
    status_message = status_messages.get(status_code, "Unknown Status")

    # Construct the response line
    response_line = f"{http_version} {status_code} {status_message}\r\n"

    # Default headers (if not provided)
    if headers is None:
        headers = {
            "Content-Type": "text/html",
            "Content-Length": len(body)
        }

    # Construct headers
    header_lines = [f"{key}: {value}" for key, value in headers.items()]
    headers_str = "\r\n".join(header_lines)

    # Final response
    response = f"{response_line}{headers_str}\r\n\r\n{body}"

    return response

# Example usage
if __name__ == "__main__":
    # Example of a simple 200 OK response
    body = "<html><body><h1>Hello, World!</h1></body></html>"
    print(build_response(200, body))

    # Example of a 404 Not Found response
    print(build_response(404))


