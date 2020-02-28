import matplotlib.pyplot as plt
import skimage.io as io
from skimage import data_dir
import numpy as np


def rgb_to_gray(img):
    return np.dot(img[..., :3], [0.21, 0.72, 0.07])


def one_hot_transform(img):
    dic = {}
    for r in range(1, 5):
        for g in range(1, 5):
            for b in range(1, 5):
                categ = 16*(r-1)+4*(g-1)+b
                dic[categ] = (64*r-1-32, 64*g-1-32, 64*b-1-32)
                # dic[categ] = (64 * r - 1, 64 * g - 1, 64 * b - 1)
    # print(np.array(img[..., 0]).shape)
    new_img = np.zeros(img.shape, dtype=int)
    onehot_img = np.zeros((img.shape[0], img.shape[1]), dtype=int)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            pixel = img[i, j]
            p_r = (pixel[0] // 64) + 1
            p_g = (pixel[1] // 64) + 1
            p_b = (pixel[2] // 64) + 1
            categ = 16*(p_r-1)+4*(p_g-1)+p_b
            # print('before', pixel)
            new_img[i, j] = dic[categ]
            onehot_img[i, j] = categ
            # print(type(new_img[i, j, 0]))
            # print('after:', list(dic[categ]))
    return new_img, onehot_img


dir_str = 'image/*.jpg'
gry_str = 'image\\gray'
class_str = 'image\\classify'
onehot_str = 'image\\onehot'
coll = io.ImageCollection(dir_str)
io.imshow_collection(coll)
io.show()

# for i in range(len(coll)):
#     new_img, onehot_img = one_hot_transform(coll[i])
#     np.save(onehot_str + '/' + np.str(i), onehot_img)
#     io.imsave(class_str + '/' + np.str(i) + '.jpg', new_img)
#     io.imshow(new_img)
#     io.show()

# for i in range(len(coll)):
#     gry = rgb_to_gray(coll[i])
#     io.imsave(gry_str + '/' + np.str(i) + '.jpg', gry)
#     io.imshow(gry, cmap='Greys_r')
#     io.show()
