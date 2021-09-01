# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 12:56:34 2020

@author: BASAVARAJ
"""
'''

import os
import numpy as np
import cv2
import natsort
import xlwt
import datetime

np.seterr(over='ignore')
if __name__ == '__main__':
    pass

# folder = "C:/Users/Administrator/Desktop/UnderwaterImageEnhancement/NonPhysical/UCM"
folder = "E:/Project_MLDL_IPCV/UW IE and Super Resolution/Results/Fusion/Zip"

path1 = folder + "/1IFM"
files1 = os.listdir(path1)
files1 =  natsort.natsorted(files1)

path2 = folder + "/1UCM"
files2 = os.listdir(path2)
files2 =  natsort.natsorted(files2)

for i in range(len(files1)):
    file1 = files1[i]
    filepath1 = path1 + "/" + file1
    prefix1 = file1.split('.')[0]
    
    file2 = files2[i]
    filepath2 = path2 + "/" + file2
    prefix2 = file2.split('.')[0]
    if os.path.isfile(filepath2):
        print('********    file   ********',file1)
        # img = cv2.imread('InputImages/' + file)
        img1 = cv2.imread(folder + '/1IFM/' + file1) 
        
        print('********    file   ********',file2)
        # img = cv2.imread('InputImages/' + file)
        img2 = cv2.imread(folder + '/1UCM/' + file2) 
        
       
        # add or blend the images
        new = cv2.addWeighted(img1, 0.5, img2, 0.55, 0.0)
       
        cv2.imwrite(folder+'/Fusion/' +file1, new)
        
'''

import cv2
import os
import datetime
import numpy as np
import natsort

folder='E:/Project_MLDL_IPCV/UW IE and Super Resolution/Results/ALL'
folderout='E:/Project_MLDL_IPCV/UW IE and Super Resolution/Results/ALL/FuseFusionGAN/'
path1 = folder + "/DirectGAN/"
path2 = folder + "/IUFusion/"
files1 = os.listdir(path1)
files2 = os.listdir(path2)
files1=  natsort.natsorted(files1)
files2=  natsort.natsorted(files2)



for i in range(len(files2)):
    file11 = files1[i]
    file22 = files2[i]
    filepath1 = path1 + file11
    filepath2 = path1 + file22
    prefix1 = file11.split('.')[0]
    prefix2 = file22.split('.')[0]
    if os.path.isfile(filepath1):
        print('********    file   ********',file11)
        img1 = cv2.imread(filepath1)
    if os.path.isfile(filepath2):
        print('********    file   ********',file22)
        img2 = cv2.imread(filepath2)
    dst = cv2.addWeighted(img1, 0.5, img2, 0.5, 0.0)
    cv2.imwrite(folderout+ file11, dst)

