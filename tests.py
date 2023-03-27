import requests
import pyaudio

# Set up the requests session
session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
    'Accept': 'audio/webm,audio/ogg,audio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5',
    'Accept-Language': 'en-GB,en;q=0.5',
    'Range': 'bytes=0-',
    'Connection': 'keep-alive',
    'Referer': 'https://www.goldenmp3.ru/',
    'Sec-Fetch-Dest': 'audio',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'cross-site',
    'Accept-Encoding': 'identity'
}
response = session.get(
    'https://listen.musicmp3.ru/1e4627a17ca3b507', headers=headers, stream=True)

# Set up the PyAudio stream
p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(2),
                channels=2,
                rate=44100,
                output=True)

# Stream the response directly to PyAudio for playback
for chunk in response.iter_content(chunk_size=512):
    stream.write(chunk)

# Clean up
stream.stop_stream()
stream.close()
p.terminate()
response.close()
session.close()
