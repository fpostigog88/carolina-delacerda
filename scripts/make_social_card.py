#!/usr/bin/env python3
"""Generate a share-card JPEG from the existing unaltered professional headshot."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
portrait = ROOT / "assets" / "carolina-headshot.webp"
target = ROOT / "assets" / "social-preview.jpg"
W, H = 1200, 630
bg = Image.new("RGB", (W, H), "#192b3d")
d = ImageDraw.Draw(bg)
ivory, rust, muted = "#FAF8F3", "#DCA28E", "#CBD8DE"

def font(name, size):
    folder = Path("/usr/share/fonts/truetype/dejavu")
    return ImageFont.truetype(str(folder / name), size=size)

display = font("DejaVuSerif.ttf", 65)
bold = font("DejaVuSans-Bold.ttf", 20)
regular = font("DejaVuSans.ttf", 24)
small = font("DejaVuSans.ttf", 18)

# Deliberately retain the original subject, without AI face generation.
d.rounded_rectangle((37, 38, 1162, 593), radius=19, outline="#475a69", width=2)
d.rectangle((75, 117, 154, 123), fill=rust)
d.text((75, 84), "PEOPLE STRATEGY   |   BUSINESS IMPACT", fill=muted, font=bold)
d.text((72, 167), "CAROLINA", fill=ivory, font=display)
d.text((72, 260), "DE LA CERDA", fill=ivory, font=display)
d.text((75, 390), "Strategic HR Business Partner", fill=rust, font=font("DejaVuSans-Bold.ttf", 27))
d.text((75, 449), "Manufacturing   |   Operations   |   Leader Advisory", fill=ivory, font=small)
d.line((75, 503, 685, 503), fill="#5d6e78", width=2)
d.text((75, 526), "Michigan Ross MBA    •    carolinadelacerda.com", fill=muted, font=small)

profile = Image.open(portrait).convert("RGB")
photo_size = 355
profile = ImageOps.fit(profile, (photo_size, photo_size), method=Image.Resampling.LANCZOS, centering=(.5, .4))
mask = Image.new("L", (photo_size, photo_size), 0)
ImageDraw.Draw(mask).ellipse((0, 0, photo_size - 1, photo_size - 1), fill=255)
cx, cy = 789, 143
d.ellipse((cx-11, cy-11, cx+photo_size+11, cy+photo_size+11), fill="#EFEBE3")
bg.paste(profile, (cx, cy), mask)
d.rounded_rectangle((812, 532, 1119, 567), radius=6, fill="#E4C4B0")
d.text((831, 540), "EMPLOYEE RELATIONS + WORKFORCE", fill="#192b3d", font=font("DejaVuSans-Bold.ttf", 11))

target.parent.mkdir(parents=True, exist_ok=True)
bg.save(target, "JPEG", quality=87, optimize=True, progressive=True, subsampling=0)
assert Image.open(target).size == (1200, 630)
assert target.stat().st_size < 5_000_000
print(f"Created {target.relative_to(ROOT)}: {W}x{H}, {target.stat().st_size} bytes")
