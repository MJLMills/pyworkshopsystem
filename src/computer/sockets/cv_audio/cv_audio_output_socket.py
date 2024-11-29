from multiplexed_input import IO


class CVAudioOutputSocket(IO):
    ...


class CVAudioOutputSocketOne(CVAudioOutputSocket):
    @property
    def pin_id(self):
        return None


class CVAudioOutputSocketTwo(CVAudioOutputSocket):
    @property
    def pin_id(self):
        return None
