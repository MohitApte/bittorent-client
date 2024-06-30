from client import TorrentClient

def main():
    # Replace with the path to your actual .torrent file
    print("Running the main application...")
    torrent_file_path = 'torrent_file.torrent'
    client = TorrentClient(torrent_file_path)
    client.start()

if __name__ == '__main__':
    main()

