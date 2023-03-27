from PIL import Image
img = Image.open('cover.jfif')
img = img.resize((320, 200), Image.ANTIALIAS)
img.save("cover.gif")
