from copy import copy
from pyglet import resource, media


class JuniorPlayer:
    def __init__(self, path, name_list):
        # Redirect the file path
        resource.path.append(path)
        resource.reindex()

        # The list of resources' name
        self._name_list = name_list

        # Load sound resources into mem
        self._resources = {
            music: resource.media(music + ".mp3", streaming=False) for music in self._name_list
        }

    def play(self, name):
        self._resources[name].play()


class SeniorPlayer(JuniorPlayer):
    """
    A music player, into which prepared resources can be loaded
    """
    def __init__(self, path, name_list):
        super(SeniorPlayer, self).__init__(path, name_list)

        # Create a music player
        self._player = media.Player()

        # Record the playing source name
        self._source_name = None

    def play(self, name=None, volume=None, loop=None):
        # TODO: Add more senior functions, such as min_distance, max_distance, pitch, on_player_eos(), etc.
        """Play the current music source, or play a new music resource.
        :param name: The name of music resource to play
        :param volume: The volume of the music player
        :param loop: If the music player loops

        Example::

            # player pause
            senior_player.pause()

            # play the current music source
            senior_player.play()
            
            # play a new music resource
            senior_player.play('new_music', loop=False)
        """

        # If vol or loop not given, use previous ones
        if volume is not None:
            self._player.volume = volume
        if loop is not None:
            self._player.loop = loop

        # Determination concerning param 'name'
        if name is None:
            try:
                self._player.play()
            except Exception as e:
                raise e
        elif name in self._name_list:
            if name == self._source_name:
                return
            else:
                self._player.queue(self._resources[name])
                if self._source_name is not None:
                    self._player.next_source()
                self._source_name = name
                self._player.play()
        else:
            raise ValueError(f'''
            No music resource named "{name}"
            ''')

    def pause(self):
        """Pause the current music source exists

        Example::

            senior_player.pause()
        """
        try:
            self._player.pause()
        except Exception as e:
            raise e

    def get_resource(self, name):
        """Get the music resource by its name
        """
        if name in self._name_list:
            return self._resources[name]
        else:
            raise ValueError(f'''
            No music resource named "{name}"
            ''')

    def get_volume(self):
        return copy(self._player.volume)

    def volume_to(self, vol):
        if vol < 0:
            self._player.volume = 0
        elif vol > 1:
            self._player.volume = 1.0
        else:
            self._player.volume = vol

    def volume_add(self, vol):
        if self._player.volume + vol < 0:
            self._player.volume = 0
        elif self._player.volume + vol > 1:
            self._player.volume = 1.0
        else:
            self._player.volume += vol

    def volume_mul(self, times):
        if times >= 0:
            if self._player.volume * times > 1:
                self._player.volume = 1.0
            else:
                self._player.volume *= times
        else:
            raise ValueError("Function volume_mul() can only receive nonnegative arg")
