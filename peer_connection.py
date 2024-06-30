import socket

# Define some constants used for the peer protocol
HANDSHAKE_PSTR = b"BitTorrent protocol"
HANDSHAKE_PSTRLEN = 19
HANDSHAKE_RESERVED = b"\x00" * 8

def make_handshake(info_hash, peer_id):
    """
    Create a handshake message for a peer connection.
    """
    return (
        bytes([HANDSHAKE_PSTRLEN]) +
        HANDSHAKE_PSTR +
        HANDSHAKE_RESERVED +
        info_hash +
        peer_id
    )

def connect_to_peer(peer_info, info_hash, peer_id):
    """
    Establish a connection to a given peer and complete the BitTorrent handshake.
    """
    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer_socket.settimeout(5)  # Set a timeout for connecting and handshaking

    try:
        peer_socket.connect((peer_info['ip'], peer_info['port']))
        print(f"Connected to peer: {peer_info['ip']}:{peer_info['port']}")

        # Send handshake
        handshake = make_handshake(info_hash, peer_id)
        peer_socket.sendall(handshake)
        print(f"Handshake sent to peer: {peer_info['ip']}:{peer_info['port']}")

        # Receive and validate handshake
        response = peer_socket.recv(len(handshake))
        if not response.startswith(bytes([HANDSHAKE_PSTRLEN]) + HANDSHAKE_PSTR):
            print(f"Invalid handshake received from peer: {peer_info['ip']}:{peer_info['port']}")
            return False
        else:
            print(f"Valid handshake received from peer: {peer_info['ip']}:{peer_info['port']}")
            return True

    except socket.error as e:
        print(f"Connection to peer failed: {e}")
        return False
    finally:
        peer_socket.close()

# Example usage
if __name__ == '__main__':
    # Example peer information and dummy values for info_hash and peer_id
    peer_info = {'ip': '127.0.0.1', 'port': 6881}
    info_hash = b'12345678901234567890'
    peer_id = b'-PC0001-123456789012'

    # Connect to peer and complete handshake
    if connect_to_peer(peer_info, info_hash, peer_id):
        print("Handshake successful")
    else:
        print("Handshake failed")

