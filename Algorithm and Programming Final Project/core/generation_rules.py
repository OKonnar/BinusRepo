class Rules:
    def __init__(self,
                 wall: str = 'X',
                 empty: str = '.',
                 start: str = '-',
                 end: str = '+',
                 generation_type: str = 'perfect',
                 cols: int = 10,
                 rows: int = 10):
        self._wall = wall
        self._empty = empty
        self._start = start
        self._end = end
        self._generation_type = generation_type
        self._cols = cols
        self._rows = rows

    @property
    def wall(self):
        return self._wall

    @wall.setter
    def wall(self, value: str):
        if not isinstance(value, str) or len(value) != 1:
            raise ValueError("Wall must be a single character.")
        self._wall = value

    @property
    def empty(self):
        return self._empty

    @empty.setter
    def empty(self, value: str):
        if not isinstance(value, str) or len(value) != 1:
            raise ValueError("Empty space must be a single character.")
        self._empty = value

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value: str):
        if not isinstance(value, str) or len(value) != 1:
            raise ValueError("Start symbol must be a single character.")
        self._start = value

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value: str):
        if not isinstance(value, str) or len(value) != 1:
            raise ValueError("End symbol must be a single character.")
        self._end = value

    @property
    def generation_type(self):
        return self._generation_type

    @generation_type.setter
    def generation_type(self, value: str):
        if value not in ['perfect', 'imperfect']:
            raise ValueError("Generation type must be 'perfect' or 'imperfect'.")
        self._generation_type = value

    @property
    def cols(self):
        return self._cols

    @cols.setter
    def cols(self, value: int):
        if value < 5:
            raise ValueError("X size must be at least 5.")
        self._cols = value

    @property
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self, value: int):
        if value < 5:
            raise ValueError("Y size must be at least 5.")
        self._rows = value

    def __str__(self):
        return(f"\n\
            \tType: {self.generation_type}\n\
            \tSize: {self.cols} x {self.rows}\n\
            \tSkin: [{self.wall}{self.empty}{self.start}{self.end}]\n")