from PIL import Image
 
# creating a image object
im = Image.open('scripts/AVLetters2_imgs/sp1_A1/1.jpg')
im = im.convert("L")
px = im.load()
print (px[4, 4])