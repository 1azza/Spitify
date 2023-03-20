from tkinter import *
from tkinter import filedialog
import tkinter as tk
import os
from tkinter import ttk
try:
    import audioplayer
    import requests
except:
    os.system('pip install audioplayer --user')
    os.system('pip install requests --user')
    import requests
    import audioplayer


class Track:
    def __init__(self, data):
        self.track = data
        self.artist = self.track['album']['artists'][0]['name']
        self.name = self.track['name']

    def __get_image(self):
        print(self.data['tracks']['items']['images'][0]['url'])
        img_data = requests.get(
            self.data['tracks']['items']['images'][0]['url']).content
        with open('image_name.jpg', 'wb') as handler:
            handler.write(img_data)


class Spotify:
    def __init__(self):
        auth_url = 'https://accounts.spotify.com/api/token'
        data = {
            'grant_type': 'client_credentials',
            'client_id': '2eff2f0720d741649dd8e6f831af5412',
            'client_secret': 'f74c496921504da6a4f03a46e9fe0a70',
        }
        auth_response = requests.post(auth_url, data=data)
        self.base_url = 'https://api.spotify.com/v1/'
        self.access_token = auth_response.json().get('access_token')
        self.headers = {
            'Authorization': 'Bearer {}'.format(self.access_token)
        }

    def get_track_details(self, filename):
        response = requests.request(
            'GET', f'https://api.spotify.com/v1/search?q={filename.split(".")[0]}&type=track', headers=self.headers)
        if response.json()['tracks']['items'] == []:
            data = {
                'api_token': '9dce630ffbacbb70498b032b790741b9',
                'return': 'apple_music,spotify',
            }
            files = {
                'file': open(filename, 'rb'),
            }
            data = requests.post(
                'https://api.audd.io/', data=data, files=files).json()['result']['spotify']
            return Track(data)
        return Track(response.json()['tracks']['items'][0])


class MusicPlayerGui:
    def __init__(self, window):
        window.geometry('320x200')
        window.title('Spitify')
        window.resizable(0, 0)
        window.configure(bg='#191414')

        self.Load = tk.Button(window, text='Load', width=10, font=(
            'Helvetica', 10, 'bold'), bg='#1DB954', fg='#FFFFFF', command=self.load)
        self.Play = tk.Button(window, text='Play ▶️', width=10, font=(
            'Helvetica', 10, 'bold'), bg='#1DB954', fg='#FFFFFF', command=self.play)
        self.Pause = tk.Button(window, text='Pause ⏸️', width=10, font=(
            'Helvetica', 10, 'bold'), bg='#1DB954', fg='#FFFFFF', command=self.pause)
        self.Stop = tk.Button(window, text='Stop', width=10, font=(
            'Helvetica', 10, 'bold'), bg='#1DB954', fg='#FFFFFF', command=self.stop)

        self.NowPlayingTrack = tk.Label(window, text="Track name: None", font=(
            'Helvetica', 10), fg='#FFFFFF', bg='#191414')
        self.NowPlayingArtist = tk.Label(window, text="Artist: None", font=(
            'Helvetica', 10), fg='#FFFFFF', bg='#191414')
        self.searchbar = tk.Entry(window, width=20, font=(
            'Helvetica', 16), bg='#FFFFFF', fg='#000000')
        self.searchbtn = tk.Button(window, text='Get', width=10, font=(
            'Helvetica', 10, 'bold'), bg='#1DB954', fg='#FFFFFF', command=lambda: self.search(self.searchbar.get()))
        self.searchbtn.grid(row=4, column=2, padx=5, pady=5)
        self.searchbar.grid(row=4, column=0, columnspan=3, padx=5, pady=5)
        self.Load.grid(row=0, column=0, padx=5, pady=5)
        self.Play.grid(row=0, column=1, padx=5, pady=5)
        self.Pause.grid(row=0, column=2, padx=5, pady=5)
        self.Stop.grid(row=1, column=1, padx=5, pady=5)

        self.NowPlayingTrack.grid(
            row=2, column=0, columnspan=3, padx=5, pady=5)
        self.NowPlayingArtist.grid(
            row=3, column=0, columnspan=3, padx=5, pady=5)

        self.music_file = False
        self.playing_state = False

    def load(self):
        self.music_file = filedialog.askopenfilename()
        filename = os.path.split(self.music_file)[1]
        if len(filename) == 0:
            return
        try:
            track = Spotify().get_track_details(filename)
        except:
            return
        self.display_track(track)
        self.player = audioplayer.AudioPlayer(self.music_file)
        self.player.play()
        self.player.pause()
    def display_track(self, track):
        self.NowPlayingTrack["text"] = f'Track name: {track.name}'
        self.NowPlayingArtist["text"] = f'Artist: {track.artist}'
    def play(self):
        self.player.resume()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def search(self, query):
        track = Spotify().get_track_details(query)
        self.display_track(track)

root = Tk()
app = MusicPlayerGui(root)
root.mainloop()
