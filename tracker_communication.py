import requests
import urllib.parse
import bencodepy

# This function now returns the base URL and the data as a dictionary
def build_tracker_request(info_hash, peer_id, port, uploaded, downloaded, left, event, tracker_url):
    base_url = tracker_url  # The base URL of the tracker
    data = {
        'info_hash': info_hash,
        'peer_id': peer_id,
        'port': port,
        'uploaded': uploaded,
        'downloaded': downloaded,
        'left': left,
        'event': event
    }

    return base_url, data

def send_tracker_request(base_url, data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    try:
        response = requests.post(base_url, data=data, headers=headers)
        response.raise_for_status()  # Check for HTTP errors
        return response.content
    except requests.RequestException as e:
        print(f"Failed to connect to tracker: {e}")
        return None


def parse_tracker_response(response):
    try:
        # Decode the bencoded response from the tracker
        decoded_response = bencodepy.decode(response)
        peers = decoded_response.get(b'peers')
        if isinstance(peers, list):
            # The tracker has returned a dictionary model (BEP3)
            return [{'ip': p[b'ip'].decode('utf-8'), 'port': p[b'port']} for p in peers]
        elif isinstance(peers, bytes):
            # The tracker has returned a binary model (BEP23)
            # This needs further parsing depending on the 'compact' flag
            # For simplicity, this example will not handle the binary model
            print("Tracker has returned peers in binary model which is not supported in this example.")
            return []
    except bencodepy.DecodingError as e:
        print(f"Failed to decode tracker response: {e}")
        return None

# Example usage
if __name__ == '__main__':
    # Dummy values for example purposes
    info_hash = b'12345678901234567890'  # Should be the SHA1 hash of the bencoded 'info' dictionary from the .torrent file
    peer_id = b'-PC0001-123456789012'   # Should be a unique ID for your client
    port = 6881                        # The port your client will listen on
    uploaded = 0                        # The total amount uploaded so far
    downloaded = 0                      # The total amount downloaded so far
    left = 0                            # The amount left to download
    event = 'started'                   # The event type: 'started', 'stopped', 'completed'
    tracker_url = 'http://yourtracker.com/announce'  # The tracker URL from the .torrent file

    # Build and send the tracker request
    request_url = build_tracker_request(info_hash, peer_id, port, uploaded, downloaded, left, event, tracker_url)
    response = send_tracker_request(request_url)
    
    # Parse the tracker response
    if response:
        peers = parse_tracker_response(response)
        print(peers)

