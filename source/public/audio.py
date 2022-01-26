from manager.audio_manager import JuniorPlayer
from manager.audio_manager import SeniorPlayer

__all__ = ['sound', 'music']

# Sound resources
sound_path = "../res/sound"
sound_list = ['button_selected', 'button_activate', 'page_slide', 'shrill_page_slide', 'drop', 'dull_activate',
              'coin_clatter', 'sell_buy_item', 'ring_knock']
sound = JuniorPlayer(sound_path, sound_list)

# Music resources
music_path = "../res/music"
music_list = ['impassioned', 'mild', 'going_deep']
music = SeniorPlayer(music_path, music_list)
