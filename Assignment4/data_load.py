import skimage.io as io
import numpy as np
import matplotlib.pyplot as plt


def data_load():
    in_dir = 'image\\gray/*.jpg'
    re_dir = 'image\\onehot'
    input_coll = io.ImageCollection(in_dir)
    onehot_coll = []
    for i in range(len(input_coll)):
        onehot_coll.append(np.load(re_dir + '\\' + np.str(i) + '.npy'))
    result = np.array(onehot_coll)
    training_data = zip(input_coll[:7], result[:7])
    validation_data = zip(input_coll[8], result[8])
    test_data = zip(input_coll[9], result[9])
    # print(input_coll.shape)
    # io.imshow_collection(input_coll, cmap='Greys_r')
    # io.show()
    return training_data, validation_data, test_data


def load_dictionary():
    dic = {}
    for r in range(1, 5):
        for g in range(1, 5):
            for b in range(1, 5):
                categ = 16 * (r - 1) + 4 * (g - 1) + b
                dic[categ] = (64 * r - 1 - 32, 64 * g - 1 - 32, 64 * b - 1 - 32)
    return dic


tra, val, test = data_load()
data, result = zip(*tra)
data = np.array(data)
result = np.array(result)
for i in range(data.shape[0]):
    print(data[i].shape, result[i].shape)