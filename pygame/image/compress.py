from PIL import Image
Image.MAX_IMAGE_PIXELS = 1000000000

# 1665 × 116594
im = Image.open('/Users/h/Downloads/123/20180903-1871/snapshot.png')
print(im.format, im.size, im.mode)
w, h = im.size
out = im.resize((int(0.5*w), int(0.5*h)), Image.ANTIALIAS)
out.save('snapshot.png')
print("end")