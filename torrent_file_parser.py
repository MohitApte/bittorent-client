import bencodepy

def read_torrent_file(file_path):
    with open(file_path, 'rb') as file:
        torrent_data = file.read()
    return torrent_data

def decode_torrent_data(torrent_data):
    try:
        decoded_data = bencodepy.decode(torrent_data)
        return decoded_data
    except bencodepy.DecodingError as e:
        print(f"Failed to decode torrent file: {e}")
        return None

def extract_info_from_decoded_data(decoded_data):
    # The 'info' dictionary within the torrent file contains the file names, piece length, and pieces
    info = decoded_data.get(b'info')
    if info:
        # Extracting and returning the relevant metadata
        return {
            'announce': decoded_data.get(b'announce').decode('utf-8'),
            'info_hash': bencodepy.encode(info),
            'piece_length': info.get(b'piece length'),
            'pieces': info.get(b'pieces'),
            'name': info.get(b'name').decode('utf-8'),
            # You can add more fields as needed
        }
    else:
        print("Info dictionary is missing in torrent file.")
        return None

# Example usage
if __name__ == '__main__':
    # Path to your .torrent file
    torrent_file_path = 'torrent_file.torrent'
    
    # Read and decode the .torrent file
    torrent_data = read_torrent_file(torrent_file_path)
    decoded_data = decode_torrent_data(torrent_data)
    
    # Extract the information
    if decoded_data:
        torrent_info = extract_info_from_decoded_data(decoded_data)
        print(torrent_info)

