import os
import torrent_file_parser
import tracker_communication
import peer_connection
import hashlib



class TorrentClient:
    def __init__(self, torrent_file_path):
        self.torrent_file_path = torrent_file_path
        self.torrent_data = None
        self.peer_id = self.generate_peer_id()
        self.info_hash = None
        self.tracker_url = None
        self.peers = []

    @staticmethod
    def generate_peer_id():
        # Generate a 20-byte peer ID. This is just an example.
        return os.urandom(20)

    def start(self):
        # Read and parse the .torrent file
        print("Client app started")
        self.torrent_data = torrent_file_parser.read_torrent_file(self.torrent_file_path)
        decoded_data = torrent_file_parser.decode_torrent_data(self.torrent_data)
        torrent_info = torrent_file_parser.extract_info_from_decoded_data(decoded_data)



        if torrent_info:
            print(torrent_info)
            print("Decoded data :",decoded_data)
            self.info_hash = torrent_info['info_hash']
            self.tracker_url = torrent_info['announce']
            
            bencoded_info = self.info_hash

            new_info_hash = hashlib.sha1(bencoded_info).digest()

            base_url, data = tracker_communication.build_tracker_request(
                self.info_hash,
                self.peer_id,
                port=6881,
                uploaded=0,
                downloaded=0,
                left=0,
                event='started',
                tracker_url=self.tracker_url
            )
            tracker_response = tracker_communication.send_tracker_request(base_url, data)
            self.peers = tracker_communication.parse_tracker_response(tracker_response)


            # Attempt to connect to the first peer (for simplicity)
            if self.peers:
                first_peer = self.peers[0]
                peer_connection.connect_to_peer(first_peer, self.info_hash, self.peer_id)

    def stop(self):
        # To be implemented: Perform any cleanup on stopping the client
        pass

# Example usage
if __name__ == '__main__':
    print("Running the main application...")
    torrent_file_path = 'torrent_file.torrent'  # Replace with the path to your .torrent file
    client = TorrentClient(torrent_file_path)
    client.start()

