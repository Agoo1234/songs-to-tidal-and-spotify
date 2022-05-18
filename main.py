import tidalapi
from tidalapi import Config, Session, Quality
import spotipy
import cache
import os
import sys
import webbrowser
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from dotenv import load_dotenv
load_dotenv()
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config as KConfig
KConfig.set('graphics', 'resizable', '0')
KConfig.set('graphics', 'width', '400')
KConfig.set('graphics', 'height', '500')

SPOTIFY_CLIENT_ID = os.getenv("CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# config
CLEAR_CACHE_ON_START = False

if CLEAR_CACHE_ON_START:
    cache.clear()

qualityconfig = Config(quality=Quality('HIGH')) # works for free users, don't need LOSSLESS even if you are a paid user
session = tidalapi.Session(qualityconfig)


def connect_to_spotify():
    scope = 'user-library-read playlist-read-collaborative playlist-modify-public playlist-read-private playlist-modify-private user-read-private'
    token = util.prompt_for_user_token(
        scope=scope,
        client_id= SPOTIFY_CLIENT_ID,
        client_secret= SPOTIFY_CLIENT_SECRET,
        redirect_uri="http://localhost:8080"
    )

    if token:
        sp = spotipy.Spotify(auth=token)
        print("Logged in to Spotify")
    else:
        print("Can't get spotify token")
        sys.exit()

    return sp




class SongsApp(App):

    screen = 0 # 0 = main screen/login, 2 = search, 3 = results, 4 = success

    def logintidal(self, id, token):
        ses = session.load_oauth_session(session_id = id, access_token = token, token_type = "Bearer", refresh_token=True)
        if ses:
            print("Logged in to TIDAL")
            cache.save(session.session_id, session.access_token)
        else:
            self.tidalLogin = Label(
                text = f"go to {ses}",
                font_size = 48,
                color = "#ffffff",
                bold = False
            )

    def screen_layout(self, screen):
        if screen == 0:
            self.testbutton = Button(text="Test", size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
            #self.testbutton.bind(on_press=self.printa())
            self.window.add_widget(self.testbutton)

    def build(self):
        self.window = BoxLayout()
        self.window.cols = 1
        self.test = Label(
            text = "TEST", 
            font_size = 48,
            color = "#ffffff",
            bold = False
        )
        self.window.add_widget(self.test)

        self.screen_layout(self.screen)

        return self.window

if __name__ == "__main__":
    SongsApp().run()