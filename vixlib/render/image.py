from PIL import Image, UnidentifiedImageError 
from typing import Literal, TypedDict
from io import BytesIO

from .text import render_mc_text
from .prestige import Prestige

from vixlib.api import fetch_skin_model


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
    

    async def draw_progress_bar(
        self,
        level: int,
        progress_percentage: int | float,
        positions: dict, 
        font_size: int
    ) -> None:
        
        xp_bar_progress = self.progress_bar_max * progress_percentage / 100
        colored_chars = self.progress_symbol * int(xp_bar_progress)
        gray_chars = self.progress_symbol * (self.progress_bar_max - int(xp_bar_progress))

        chars_text = f'&b{colored_chars}&7{gray_chars}'
        formatted_lvl_text = Prestige(int(level)).color_level
        formatted_target_text = Prestige(int(level) + 1).color_level

        self._text_render.draw(
            text=f'{formatted_lvl_text} &8[',
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
            text=f'&8] {formatted_target_text}',
            text_options={
                "font_size": font_size,
                "position": positions.get('right'),
                "shadow_offset": (2, 2),
                "align": "left"
            }
        )


    async def draw_progression(
        self, 
        progress: int,
        target: int,
        position: tuple[int, int], 
        font_size: int        
    ) -> None:
        self._text_render.draw(
            text=f'&7EXP Progress: &b{progress:,}&8/&a{target:,}',
            text_options={
                "font_size": font_size,
                "position": position,
                "shadow_offset": (2, 2),
                "align": "center"
            }
        )

    async def draw_prestige(
        self, 
        level: int, 
        position: tuple[int, int], 
        font_size: int
    ) -> None:
        self._text_render.draw(
            text=f'&7Level: {Prestige(int(level)).color_level}',
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
        return await fetch_skin_model(uuid, style=style)

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

            
