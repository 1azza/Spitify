from tkinter import *
from tkinter import filedialog
import tkinter as tk
import os
import threading
from bs4 import BeautifulSoup
try:
    import audioplayer
    import requests
except:
    os.system('pip install audioplayer --user')
    os.system('pip install requests --user')
    import requests
    import audioplayer




class GoldenMp3:
    def __init__(self, track):
        self.track = track
        self.session = requests.Session()
        self.headers = {
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
    def generate_stream(self):
        # track = Spotify().get_track_details(query)
        print(self.track.album)
        url = "https://www.goldenmp3.ru/search.html"
        querystring = {"text": f'{self.track.album} {self.track.artist}'}
        payload = ""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0",
        }


        response = requests.request(
            "GET", url, data=payload, headers=headers, params=querystring)
        try:
            path = response.text.split('<dt><a href="/')[1].split('"')[0]
        except:
            tk.messagebox.showwarning('Track not found', 'Unable to generate a stream for this track')
            return 
        url = 'https://www.goldenmp3.ru/' + path.split('/')[0] + '/songs'
        print(url)
        response = requests.request("GET", url, data=payload, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        for i in soup.find_all('div', 'title_td_wrap'):
            name = i.text
            print(name)
            if name.upper().split('(')[0] == self.track.name.upper().split('(')[0]:
                stream_code = i.parent.parent.find('a', {'class': 'play'})['rel']
                print(stream_code)
                stream_url = f'https://listen.musicmp3.ru/{stream_code[0]}'
                return stream_url
    def download(self, url):
        print(url)
        response = self.session.get(
            url, headers=self.headers, stream=True)
        i = 0   
        # Save the response to a file
        with open(f'{self.track.name} - {self.track.artist}.mpeg', 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
                print(i)
                i += 1
                if i == 500:
                    f.close()
                    break
        # Clean up the response
        response.close()
        self.session.close()
class Track:
    def __init__(self, data):
        self.track = data
        self.artist = self.track['album']['artists'][0]['name']
        self.name = self.track['name']
        self.album = self.track['album']['name']
        print('Getting image')
        print(self.track['album']['images'][0]['url'])
        img_data = requests.request(
            'GET', self.track['album']['images'][0]['url']).content
        with open('cover.jfif', 'wb') as handler:
            handler.write(img_data)
        os.system('python convert.py')


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
        self.bg_image = tk.PhotoImage(file="cover.gif")
        self.bg_label = tk.Label(window, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.Load = tk.Button(window, text='Load', width=10, font=(
            'Helvetica', 10, 'bold'), bg='#1DB954', fg='#FFFFFF', command=self.load_music_gui)
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

    def __get_track_details_non_block(self, filename):
        self.track = Spotify().get_track_details(filename)
    def load_music_gui(self):
        self.music_file = filedialog.askopenfilename()
        track_name = os.path.split(self.music_file)[1]
        if len(track_name) == 0:
            return
        try:
            thread = threading.Thread(
                target=self.__get_track_details_non_block, args=(track_name,))
            thread.start()
            thread.join()
        except:
            return
        self.display_track()
        self.player = audioplayer.AudioPlayer(self.music_file)
        self.player.play()
        self.player.pause()

    def update_background(self, path):
        new_bg = tk.PhotoImage(file=path)
        self.bg_label.configure(image=new_bg)
        self.bg_label.image = new_bg # prevent image from being garbage collected
        
    def display_track(self):
        self.NowPlayingTrack["text"] = f'Track name: {self.track.name}'
        self.NowPlayingArtist["text"] = f'Artist: {self.track.artist}'
        self.update_background('cover.gif')

    def play(self):
        self.player.resume()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()
    def search(self, query):
        self.track = Spotify().get_track_details(query)
        self.display_track()
        mp3 = GoldenMp3(self.track)
        url = mp3.generate_stream()
        if url:
            res = tk.messagebox.askyesno(title="Download", message="Stream generated, do you want to download it? (This may take w while)")
            if res == True:
                mp3.download(url)
                self.music_file = f'{self.track.name} - {self.track.artist}.mpeg'
                self.display_track()
                self.player = audioplayer.AudioPlayer(self.music_file)
                self.player.play()
                self.player.pause()
                tk.messagebox.showinfo(title='Succesful', message=f'{self.track.name} by {self.track.artist} downloaded succesfully')
            else:
                return

root = Tk()
app = MusicPlayerGui(root)
root.mainloop()

# track = Spotify().get_track_details('RIP - playboi carti')
# print(track.name)
# url = "https://www.goldenmp3.ru/search.html"
# print(track.artist)
# querystring = {"text": f'{track.album} {track.artist}'}
# payload = ""
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0",
# }
# response = requests.request(
#     "GET", url, data=payload, headers=headers, params=querystring)
# path = response.text.split('<dt><a href="/')[1].split('"')[0]
# url = 'https://www.goldenmp3.ru/' + path.split('/')[0] + '/songs'
# print(url)
# response = requests.request("GET", url, data=payload, headers=headers)
# soup = BeautifulSoup(response.text, 'lxml')
# for i in soup.find_all('div', 'title_td_wrap'):
#     name = i.text
#     print(name)
#     if name.upper().split('(')[0] == track.name.upper().split('(')[0]:
#         stream_code = i.parent.parent.find('a', {'class': 'play'})['rel']
#         print(stream_code)
#         stream_url = f'https://www.goldenmp3.ru/{stream_code[0]}'
#         print(stream_url)
#         break

