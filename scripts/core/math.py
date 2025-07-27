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

    pos = property(get_pos, set_pos)
    size = property(get_size, set_size)
    x = property(get_x, set_x)
    y = property(get_y, set_y)
    width = property(get_width)
    height = property(get_height)