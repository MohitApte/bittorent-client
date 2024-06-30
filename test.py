import bencodepy
import os
import hashlib
import requests
torrent_file_path = "torrent_file.torrent"
torrent_data = None
peer_id = os.urandom(20)
with open(torrent_file_path, 'rb') as file:
    torrent_data = file.read()


decoded_data = bencodepy.decode(torrent_data)

info = decoded_data.get(b'info')

torrent_info = {
    'announce': decoded_data.get(b'announce').decode('utf-8'),
    'info_hash': bencodepy.encode(info),
    'piece_length': info.get(b'piece length'),
    'pieces': info.get(b'pieces'),
    'name': info.get(b'name').decode('utf-8'),
}

if torrent_info:
    info_hash = hashlib.sha1(torrent_info['info_hash']).digest()
    tracker_url = torrent_info['announce']

port=9999  
uploaded=0
downloaded=0
left=0
event='started'

base_url = tracker_url

data = {
    'info_hash': info_hash,
    'peer_id': peer_id,
    'port': port,
    'uploaded': uploaded,
    'downloaded': downloaded,
    'left': left,
    'event': event
}
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

try:
    response = requests.post(base_url, data=data, headers=headers)
    response.raise_for_status()  # Check for HTTP errors
    tracker_response = response.content
except requests.RequestException as e:
    print(f"Failed to connect to tracker: {e}")
    tracker_response = None

decoded_response = bencodepy.decode(tracker_response)
peers = decoded_response.get(b'peers')


print('peers :', peers)

print(decoded_response)
