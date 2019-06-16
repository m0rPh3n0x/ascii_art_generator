import PIL.Image
import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(edgeitems=200, linewidth=400)

scale70 = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"' + "^`'. "
scale10 = " .:-=+*#%@"[::-1]
width = 120
scale = 10
use_histogram_equalization = True
use_max_threshold = True
threshold = 180
filename = "gen_01.png"
ascii_art_filename = "{}_ascii_art_{}_{}_{}.txt".format(filename.replace(".png", ""), scale, use_histogram_equalization, use_max_threshold)

im = PIL.Image.open(filename).convert('L')
original_w, original_h = im.size
height = int(round(width / original_w * original_h, 0))
im = im.resize((width, height))

A = np.array(im)
if use_histogram_equalization:
    p = np.zeros(256)
    C = np.zeros(256)
    n = width * height
    for i in range(256):
        p[i] = np.sum((A == i).astype('int')) / n
        C[i] = int(round(np.sum(p) * 255, 0))
    A2 = np.zeros(A.shape)
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            A2[i, j] = C[A[i, j]]

if use_max_threshold:
    A2[np.where(A2 > threshold)] = 255

# visualization of equalization and threshold:
plt.subplot(121)
plt.imshow(A, cmap='gray')
plt.subplot(122)
plt.imshow(A2, cmap='gray')
plt.show()


step = int(np.ceil(255 / scale))
if use_histogram_equalization:
    ascii_art = A2 // step
else:
    ascii_art = A // step

ascii_art = ascii_art.astype('int')
with open(ascii_art_filename, 'w', encoding='utf-8') as file:
    for i in range(ascii_art.shape[0]):
        for j in range(ascii_art.shape[1]):
            if scale == 10:
                file.write(scale10[ascii_art[i, j]])
            elif scale == 70:
                file.write(scale70[ascii_art[i, j]])
        if i != ascii_art.shape[0] - 1:
            file.write("\n")
