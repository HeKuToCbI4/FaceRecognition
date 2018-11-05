import numpy as np
import os
from limits import CWD
import scipy.io
import time
import json
import csv

if __name__ == '__main__':
    data = []
    h5file = scipy.io.loadmat(os.path.join(CWD, 'wiki', 'wiki.mat'))
    wiki = h5file['wiki']
    for name, filename, face_pos in zip(wiki['name'][0][0][0],
                                        wiki['full_path'][0][0][0], wiki['face_location'][0][0][0]):
        face_pos = face_pos[0]
        x, y, h, w = int(face_pos[1]), int(face_pos[3]), int(face_pos[0]), int(face_pos[2])
        data.append({'file_name': filename[0], 'face_position': (x, y, h, w)})
    with open('json_data.json', 'w') as out:
        json.dump(data, out)
