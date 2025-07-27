import json
import pathlib
from PIL import Image
from typing import Union
from core.math import *

class SpriteSheet(object):
    def __init__(
            self,
            img: Union[str, pathlib.Path],
            w: int, h: int
    ):
        if not isinstance(img, pathlib.Path):
            img = pathlib.Path(img)
        self._img = img
        self._size = Vector2(w, h)
        self._rects: list[SpriteRect] = []

    def get_img(self):
        return self._img

    def get_size(self):
        return self._size.x, self._size.y

    def append_sprite_rect(
            self,
            x: int,
            y: int,
            w: int,
            h: int,
            name:str=None
    ):
        if name is None:
            name = self._gen_sprite_name()
        self._rects.append(SpriteRect(x, y, w, h, name))

    def save(self, path):
        if not isinstance(path, pathlib.Path):
            path = pathlib.Path(path)
        if path.is_dir():
            self._save_as_sprite_images(path)
        elif path.suffix == '.json':
            self._save_as_json(path)

    def _save_as_sprite_images(self, directory: pathlib.Path):
        suffix = self._img.suffix
        img = Image.open(self._img)
        sprites = []
        for rect in self._rects:
            x, y = rect.pos
            w, h = rect.size
            sprite = img.crop((x, y, x + w, y + h))
            sprites.append((sprite, rect.name))
        for sprite, name in sprites:
            path = directory / f'{name}{suffix}'
            sprite.save(path)

    def _save_as_json(self, path: pathlib.Path):
        sprite_rects = []
        data = {
            'image': self._img.as_posix(),
            'width': self._size.x,
            'height': self._size.y,
            'rects': sprite_rects
        }
        for rect in self._rects:
            sprite_rects.append({
                'name': rect.name,
                'rect': {
                    'x': rect.x,
                    'y': rect.y,
                    'width': rect.width,
                    'height': rect.height
                }
            })
        with open(path, mode='w', encoding='utf-8') as fp:
            json.dump(data, fp, indent=4)

    def _gen_sprite_name(self) -> str:
        return str(len(self._rects))

    img = property(get_img)
    size = property(get_size)

class SpriteRect(Rect):
    def __init__(self, x, y, w, h, name):
        super().__init__(x, y, w, h)
        self._name = name

    def get_name(self):
        return self._name

    name = property(get_name)