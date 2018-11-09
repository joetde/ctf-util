
from PIL import Image
from pyzbar.pyzbar import ZBarSymbol
from pyzbar.pyzbar import decode
from random import sample

def decode_qr(image):
    return decode(image, symbols=[ZBarSymbol.QRCODE])

#order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
order = [0, 11, 26, 1, 5, 2, 3, 4, 6, 7, 8, 9, 10, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 12, 13]
#order = [0, 3, 5, 1, 2, 4, 16, 6, 8, 7, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]

# All zeroes => 0, 11, 9, 17, 12, 13
# Left squares borders => 5 26 (this order, timing on 26)
# Left squares blanks => 6 15
# Left squares squares => 2 16 25
# Blank left => 3
# Right square borders => 8, 14
# Right square blanks => 1, 18
# Right square square => 4, 22, 23, 24
# Blank right => 7
# Middle = 10, 19, 20, 21

order = [5, 6, 2, 16, 25, 15, 26, 3, 10, 19, 20, 21, 7, 8, 1, 4, 22, 23, 24, 18, 14]
order = [0, 9, 11, 5, 6, 2, 16, 25, 15, 26, 3, 20, 10, 21, 19, 24, 7, 8, 1, 4, 22, 23, 18, 14, 12, 13, 17]

perms = [[0], [9], [11],
         [5], [6, 15], [2, 16, 25], [2, 16, 25], [2, 16, 25], [6, 15], [26], [3],
         [4, 10, 19, 20, 21, 22, 23, 24], [4, 10, 19, 20, 21, 22, 23, 24], [4, 10, 19, 20, 21, 22, 23, 24], [4, 10, 19, 20, 21, 22, 23, 24], [4, 10, 19, 20, 21, 22, 23, 24],
         [7], [8, 14], [1, 18], [4, 22, 23, 24], [4, 22, 23, 24], [4, 22, 23, 24], [1, 18], [8, 14],
         [12], [13], [17]]

def generate_one_perms(perms_array):
    picked = set()
    series = []
    for a in perms_array:
       possibles = [x for x in a if x not in picked]
       if not possibles:
          return None
       new_el = sample(possibles, 1)[0] # TODO filter
       picked.add(new_el)
       series.append(new_el)
    return series

order = generate_one_perms(perms)

def is_left_square_border(band):
    return band[3:12] == [0, 1, 1, 1, 1, 1, 1, 1, 0] and band[18:28] == [0, 1, 1, 1, 1, 1, 1, 1, 1, 0]

def is_left_square_blank(band):
   return band[3:12] == [0, 1, 0, 0, 0, 0, 0, 1, 0] and band[18:28] == [0, 1, 0, 0, 0, 0, 0, 0, 1, 0]

def is_left_square_square(band):
   return band[3:12] == [0, 1, 0, 1, 1, 1, 0, 1, 0] and band[18:28] == [0, 1, 0, 1, 1, 1, 1, 0, 1, 0]

def is_left_square_out_blank(band):
    return band[3:12] == [0, 0, 0, 0, 0, 0, 0, 0, 0] and band[18:28] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def is_right_square_borders(band):
    return band[3:12] == [0, 1, 1, 1, 1, 1, 1, 1, 0] and not is_left_square_border(band)

def is_right_square_blank(band):
    return band[3:12] == [0, 1, 0, 0, 0, 0, 0, 1, 0] and not is_left_square_blank(band)

def is_right_square_square(band):
    return band[3:12] == [0, 1, 0, 1, 1, 1, 0, 1, 0] and not is_left_square_square(band)

def is_right_square_out_blank(band):
    return band[3:12] == [0, 0, 0, 0, 0, 0, 0, 0, 0] and not is_left_square_out_blank(band)

def is_none(band):
    return not is_left_square_border(band) and not is_left_square_blank(band) and not is_left_square_square(band) and not is_left_square_out_blank(band) and not is_right_square_borders(band) and not is_right_square_blank(band) and not is_right_square_square(band) and not is_right_square_out_blank(band)

def generate_from_order(order):
    bands = []
    images = []
    for i in order:
        img = Image.open("%s.png" % i)
        images.append(img)
        band = []
        (width, height) = img.size
        for j in range(height / width):
            bit = 0
            if img.getpixel((1, j * width + 1))[0] == 0:
                bit = 1
            band.append(bit)
        bands.append(band)

    i = 0
    for band in bands:
        #print band, order[i]
        i += 1

    (width, height) = images[0].size
    recv_image = Image.new("RGBA", (width * len(images), height))

    x = 0
    for i in images:
        recv_image.paste(i, (x, 0))
        x += i.width

    #recv_image.show()
    print order
    decoded = decode_qr(recv_image)
    if decoded:
        print decoded
        raise ""
    recv_image.close()

for i in range(100000):
    p = generate_one_perms(perms)
    if p:
        generate_from_order(p)
