from PIL import Image, UnidentifiedImageError 
from typing import Literal, TypedDict
from io import BytesIO

from .text import render_mc_text
from .colors import Prestige

import vixlib as lib


class TextOptions(TypedDict):
    font_size: int
    position: tuple[int, int]
    shadow_offset: tuple[int, int] | None
    align: Literal["left", "right", "center"]

    @staticmethod
    def default() -> 'TextOptions':
        return {
            "font_size": 16,
            "position": (0, 0),
            "shadow_offset": None,
            "align": "left"
        }


class ImageRender:
    def __init__(self, base_image: Image.Image):
        self._image: Image.Image = base_image.convert("RGBA")
        self.text = TextRender(self._image)
        self.progress = ProgressRender(self._image, self.text)
        self.skin = SkinRender(self._image, self.text)

    def overlay_image(self, overlay_image: Image.Image) -> None:
        self._image.alpha_composite(overlay_image.convert("RGBA"))


    def to_bytes(self) -> bytes:
        image_bytes = BytesIO()
        self._image.save(image_bytes, format='PNG')
        image_bytes.seek(0)
        return image_bytes


    def save(self, filepath: str, **kwargs) -> None:
        self._image.save(filepath, **kwargs)


    @property
    def size(self) -> tuple[int, int]:
        return self._image.size


class TextRender:
    def __init__(self, image: Image.Image) -> None:
        self._image = image


    def draw(self, text: str, text_options: TextOptions = TextOptions.default()) -> None:
        if "position" not in text_options:
            text_options["position"] = (0, 0)
        render_mc_text(text, image=self._image, **text_options)


    def draw_many(
        self,
        text_info: list[tuple[str, TextOptions]],
        default_text_options: TextOptions
    ) -> None:
        for text, text_options in text_info:
            self.draw(
                text, {**default_text_options, **text_options}
            )        


class ProgressRender:
    progress_symbol = "⏹"
    progress_bar_max = 10

    def __init__(self, image: Image.Image, text_render: TextRender) -> None:
        self._image = image
        self._text_render = text_render  
    

    async def render_progress_bar(
        self, 
        level: float, 
        xp: int,
        progress_percentage: float,
        positions: dict, 
        font_size: int
    ) -> None:

        int_level = int(level)
        current_xp = xp

        if current_xp < 500:
            min_colored_boxes = 1
        elif 500 <= current_xp < 1000:
            min_colored_boxes = 2
        else:
            min_colored_boxes = 0  
        
        xp_bar_progress = self.progress_bar_max * progress_percentage / 100
        colored_boxes = max(int(xp_bar_progress), min_colored_boxes)
        
        if colored_boxes > self.progress_bar_max:
            colored_boxes = self.progress_bar_max

        colored_chars = self.progress_symbol * colored_boxes
        gray_chars = self.progress_symbol * (self.progress_bar_max - colored_boxes)

        chars_text = f'&b{colored_chars}&7{gray_chars}'

        formatted_level_text = f"{Prestige(int_level).formatted_level} &8[" 
        formatted_target_level_text = f"&8] {Prestige(int_level + 1).formatted_level}"

        self._text_render.draw(
            text=f'{formatted_level_text}',
            text_options={
                "font_size": font_size,
                "position": positions.get('left'),
                "shadow_offset": (2, 2),
                "align": "right"
            }
        )
        self._text_render.draw(
            text=f'{chars_text}',
            text_options={
                "font_size": font_size,
                "position": positions.get('center'),
                "shadow_offset": (2, 2),
                "align": "center"
            }
        )
        self._text_render.draw(
            text=f'{formatted_target_level_text}',
            text_options={
                "font_size": font_size,
                "position": positions.get('right'),
                "shadow_offset": (2, 2),
                "align": "left"
            }
        )


    async def render_progression(
        self, 
        xp: int, 
        xp_needed: int,
        position: tuple[int, int], 
        font_size: int        
    ) -> None:
        self._text_render.draw(
            text=f'&7EXP Progress: &b{xp:,}&8/&a{xp_needed:,}',
            text_options={
                "font_size": font_size,
                "position": position,
                "shadow_offset": (2, 2),
                "align": "center"
            }
        )

    async def render_prestige(
        self, 
        level: int, 
        position: tuple[int, int], 
        font_size: int
    ) -> None:
        self._text_render.draw(
            text=f'&7Level: {level}',
            text_options={
                "font_size": font_size,
                "position": position,
                "shadow_offset": (2, 2),
                "align": "center"
            }
        )


class SkinRender:
    def __init__(self, image: Image.Image, text_render: "TextRender") -> None:
        self._image = image
        self._text_render = text_render 

    async def _skin_url(self, uuid: str, style: str):
        return await lib.fetch_skin_model(uuid, style=style)

    async def paste_skin(
        self, 
        uuid: str, 
        position: tuple[int, int],
        size: tuple[int, int],
        style: str = 'full'
    ) -> None:
        skin_data = await self._skin_url(uuid, style)

        try:
            skin_model = BytesIO(skin_data)
            skin_model.seek(0)
            skin = Image.open(skin_model).convert("RGBA")
            skin = skin.resize(size)

            composite_image = Image.new("RGBA", self._image.size)
            composite_image.paste(skin, position, mask=skin.split()[3])

            self._image.alpha_composite(composite_image)

        except (UnidentifiedImageError, Exception) as error:
            print(error)

            
