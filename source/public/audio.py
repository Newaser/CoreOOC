from manager.audio_manager import JuniorPlayer as _JP
from manager.audio_manager import SeniorPlayer as _SP

# Sound resources
_sound_path = "../res/sound"
_sound_list = ['button_selected', 'button_activate', 'page_slide', 'shrill_page_slide']
sound = _JP(_sound_path, _sound_list)

# Music resources
_music_path = "../res/music"
_music_list = ['impassioned', 'mild', 'going_deep']
music = _SP(_music_path, _music_list)
