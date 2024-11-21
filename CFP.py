import hashlib
import random
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import requests

font_urls = [
    "https://github.com/google/fonts/raw/main/ofl/lato/Lato-Regular.ttf",
    "https://github.com/google/fonts/raw/main/ofl/merriweather/Merriweather-Regular.ttf",
    "https://github.com/google/fonts/raw/main/ufl/ubuntu/Ubuntu-Regular.ttf",
    "https://github.com/ryanoasis/nerd-fonts/raw/refs/heads/master/patched-fonts/AnonymousPro/Italic/AnonymiceProNerdFontMono-Italic.ttf",
    "https://github.com/ryanoasis/nerd-fonts/raw/refs/heads/master/patched-fonts/Agave/AgaveNerdFontMono-Bold.ttf",
]

downlaodedfonts = []


def download(url: str) -> ImageFont.FreeTypeFont:
    for font_bytes, font_url in downlaodedfonts:
        if url == font_url:
            font_bytes = io.BytesIO(font_bytes)
            return ImageFont.truetype(font_bytes, random.choice([11, 18, 24]))
    try:
        response = requests.get(url)
        response.raise_for_status()
        downlaodedfonts.append((response.content, url))
        font_bytes = io.BytesIO(response.content)
        return ImageFont.truetype(font_bytes, random.choice([11, 18, 24]))
    except Exception as e:
        raise Exception(f"Error downloading font: {e}")


def hash(s: str) -> int:
    hash_value = 0
    for char in s:
        hash_value = (hash_value << 5) - hash_value + ord(char)
        hash_value &= 0xFFFFFFFF
    return hash_value


def cfp():
    try:
        font_url = random.choice(font_urls)
        font = download(font_url)

        width, height = 2000, 200
        img = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(img)

        for _ in range(random.randint(5, 15)):
            x1, y1 = random.randint(0, width // 2), random.randint(0, height // 2)
            x2, y2 = random.randint(x1, width), random.randint(y1, height)
            color = tuple(random.randint(0, 255) for _ in range(3))
            draw.rectangle([x1, y1, x2, y2], fill=color)

        for _ in range(random.randint(2, 5)):
            x, y = random.randint(0, width - 200), random.randint(0, height - 50)
            text = "".join(
                random.choices(
                    "abcdefghijklmnopqrstuvwxyz0123456789@#$%^&*🥹😈👍🥒🤭🥶🤓🔍©️🤣♥️😜😛😌🥶🤬😡🐀🐁🪲🪰🐛⛷️",
                    k=random.randint(10, 50),
                )
            )
            color = tuple(random.randint(0, 255) for _ in range(3))
            draw.text((x, y), text, fill=color, font=font)

        for _ in range(random.randint(5, 10)):
            x1, y1 = random.randint(0, width // 2), random.randint(0, height // 2)
            x2, y2 = random.randint(x1, width), random.randint(y1, height)
            color = tuple(random.randint(0, 255) for _ in range(3))
            draw.ellipse([x1, y1, x2, y2], fill=color)

        ut = ["canvas randomness:true"]
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_data = base64.b64encode(buffered.getvalue()).decode("utf-8")
        ut.append(f"canvas fp:data:image/png;base64,{img_data}")

        result = hash("~".join(ut))
        return result

    except Exception as e:
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    print("CFP:", cfp())
