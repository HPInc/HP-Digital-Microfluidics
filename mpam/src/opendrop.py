import mpam.device

class Board(mpam.device.Board):
    def __init__(self, dev : str):
        self._dev = dev
        self._states = bytearray(128)
        self._states[21] = 1
        self._states[23] = 1
        self._states[25] = 1
        self._stream = None
        
    def update_state(self):
        if self._stream is None:
            self._stream = open(self._dev, "wb")
        self._stream.write(self._states)
        # I'm not sure why, but it seems that nothing happens until the 
        # first byte of the next round gets sent. (Sending 129 bytes works, 
        # but then the next round will use that extra byte.  Sending everything
        # twice seems to do the job.  I'll look into this further.
        self._stream.write(self._states)
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._stream is not None:
            self._stream.close()
            self._stream = None
        return super().__exit__(exc_type, exc_val, exc_tb)
    