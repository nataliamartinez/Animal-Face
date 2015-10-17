import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import random


quote = random.choice(list(open('quotes.txt')))
# print quote

# font = ImageFont.truetype("Norican-Regular.ttf",14)
font = ImageFont.truetype("Norican-Regular.ttf",20)
img=Image.new("RGBA", (500,250),(255,255,255))
draw = ImageDraw.Draw(img)
draw.text((0, 0), quote ,(0,0,0),font=font)
draw = ImageDraw.Draw(img)
img.save("a_test.png")