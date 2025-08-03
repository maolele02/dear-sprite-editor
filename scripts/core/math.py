__all__ = [
    'Vector2',
    'FVector2',
    'Rect',
    'FRect',
]

class Vector2(object):
    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y

    def get_x(self):
        return self._x

    def set_x(self, x):
        assert isinstance(x, int)
        self._x = x

    def get_y(self):
        return self._y

    def set_y(self, y):
        assert isinstance(y, int)
        self._y = y

    def __add__(self, other):
        self._x += other.x
        self._y += other.y

    def __sub__(self, other):
        self._x -= other.x
        self._y -= other.y

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector2(int(self._x * other), int(self._y * other))
        elif isinstance(other, Vector2):
            return Vector2(int(self._x * other.x), int(self._y * other.y))
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __iter__(self):
        yield self._x
        yield self._y

    def __repr__(self):
        return f'{self.__class__.__name__}({self.x}, {self.y})'

    x = property(get_x, set_x)
    y = property(get_y, set_y)

class FVector2(object):
    def __init__(self, x=.0, y=.0):
        self._x = x
        self._y = y

    def get_x(self):
        return self._x

    def set_x(self, x):
        assert isinstance(x, float)
        self._x = x

    def get_y(self):
        return self._y

    def set_y(self, y):
        assert isinstance(y, float)
        self._y = y

    def __add__(self, other):
        self._x += other.x
        self._y += other.y

    def __sub__(self, other):
        self._x -= other.x
        self._y -= other.y

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return FVector2(self._x * other, self._y * other)
        elif isinstance(other, Vector2):
            return FVector2(self._x * other.x, self._y * other.y)
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __iter__(self):
        yield self._x
        yield self._y

    def __repr__(self):
        return f'{self.__class__.__name__}({self.x}, {self.y})'

    x = property(get_x, set_x)
    y = property(get_y, set_y)

class Rect(object):

    def __init__(self, x=0, y=0, w=0, h=0):
        self._pos = Vector2(x, y)
        self._size = Vector2(w, h)

    def get_x(self):
        return self._pos.x

    def set_x(self, x):
        self._pos.x = x

    def get_y(self):
        return self._pos.y

    def set_y(self, y):
        self._pos.y = y

    def get_pos(self):
        return self._pos.x ,self._pos.y

    def set_pos(self, x, y):
        self._pos.x = x
        self._pos.y = y

    def get_size(self):
        return self._size.x, self._size.y

    def set_size(self, w, h):
        self._size.x = w
        self._size.y = h

    def get_width(self):
        return self._size.x

    def get_height(self):
        return self._size.y

    def to_tuple(self):
        return self.x, self.y, self.width, self.height

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            x = self.x * other
            y = self.y * other
            w = self.width * other
            h = self.height * other
            return Rect(int(x), int(y), int(w), int(h))
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.width
        yield self.height

    def __repr__(self):
        return f'{self.__class__.__name__}({self.x}, {self.y}, {self.width}, {self.height})'

    pos = property(get_pos, set_pos)
    size = property(get_size, set_size)
    x = property(get_x, set_x)
    y = property(get_y, set_y)
    width = property(get_width)
    height = property(get_height)

class FRect(object):

    def __init__(self, x=.0, y=.0, w=.0, h=.0):
        self._pos = FVector2(x, y)
        self._size = FVector2(w, h)

    def get_x(self):
        return self._pos.x

    def set_x(self, x):
        self._pos.x = x

    def get_y(self):
        return self._pos.y

    def set_y(self, y):
        self._pos.y = y

    def get_pos(self):
        return self._pos.x ,self._pos.y

    def set_pos(self, x, y):
        self._pos.x = x
        self._pos.y = y

    def get_size(self):
        return self._size.x ,self._size.y

    def set_size(self, w, h):
        self._size.x = w
        self._size.y = h

    def get_width(self):
        return self._size.x

    def get_height(self):
        return self._size.y

    def to_tuple(self):
        return self.x, self.y, self.width, self.height

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            x = self.x * other
            y = self.y * other
            w = self.width * other
            h = self.height * other
            return FRect(x, y, w, h)
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.width
        yield self.height

    def __repr__(self):
        return f'{self.__class__.__name__}({self.x}, {self.y}, {self.width}, {self.height})'

    pos = property(get_pos, set_pos)
    size = property(get_size, set_size)
    x = property(get_x, set_x)
    y = property(get_y, set_y)
    width = property(get_width)
    height = property(get_height)