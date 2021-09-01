#!/usr/bin/env python
"""
# > Script for measuring quantitative performances in terms of
#    - Structural Similarity Metric (SSIM) 
#    - Peak Signal to Noise Ratio (PSNR)
#    - Underwater Image Quality Measure (UIQM)
# Maintainer: Jahid (email: islam034@umn.edu)
# Interactive Robotics and Vision Lab (http://irvlab.cs.umn.edu/)
"""
## python libs
import os
import numpy as np
from glob import glob
from os.path import join
from ntpath import basename
from PIL import Image
## local libs
from utils.uiqm_utils import getUIQM
from utils.ssm_psnr_utils import getSSIM, getPSNR

import random
import fnmatch
#import numpy as np
from scipy import misc
#from glob import glob
import skimage.transform

def getPaths(data_dir):
    exts = ['*.png','*.PNG','*.jpg','*.JPG', '*.JPEG']
    image_paths = []
    for pattern in exts:
        for d, s, fList in os.walk(data_dir):
            for filename in fList:
                if (fnmatch.fnmatch(filename, pattern)):
                    fname_ = os.path.join(d,filename)
                    image_paths.append(fname_)
    return np.asarray(image_paths)

# measurement in a common dimension
#im_w, im_h = 320, 240 #for SESR
#im_w, im_h = 512, 512 #for SRDRM
im_w, im_h = 160, 120 #for SRDRM

## data paths
#REAL_im_dir = "E:/Project_MLDL_IPCV/UW IE and Super Resolution/Implementation/SR/DSESR/data/sample_test_ufo/lrd/"  # real/input im-dir with {f.ext}
#GEN_im_dir  = "E:/Project_MLDL_IPCV/UW IE and Super Resolution/Implementation/SR/DSESR/data/output/keras_out/"  # generated im-dir with {f_SESR/EN.ext}
#GTr_im_dir  = "E:/Project_MLDL_IPCV/UW IE and Super Resolution/Implementation/SR/DSESR/data/sample_test_ufo/hr/"  # ground truth im-dir with {f.ext}

#GEN_im_dir  = "E:/Project_MLDL_IPCV/UW IE and Super Resolution/Results/4SRUCM/"  # generated im-dir with {f_SESR/EN.ext}
#GTr_im_dir  = "E:/Project_MLDL_IPCV/UW IE and Super Resolution/Results/GTR512/"  # ground truth im-dir with {f.ext}

GEN_im_dir  ="E:/Project_MLDL_IPCV/UW IE and Super Resolution/Implementation/SR/TTSR/4xOutput/"
GTr_im_dir  = "E:/Project_MLDL_IPCV/UW IE and Super Resolution/Implementation/SR/TTSR/4xRef/"

## mesures uqim for all images in a directory
def measure_UIQMs(dir_name, file_ext=None):
    """
      # measured in RGB
      Assumes:
        * dir_name contain generated images 
        * to evaluate on all images: file_ext = None 
        * to evaluate images that ends with "_SESR.png" or "_En.png"  
            * use file_ext = "_SESR.png" or "_En.png" 
    """
    paths = sorted(glob(join(dir_name, "*.*")))
    if file_ext:
        paths = [p for p in paths if p.endswith(file_ext)]
    uqims = []
    for img_path in paths:
        im = Image.open(img_path).resize((im_w, im_h))
        uqims.append(getUIQM(np.array(im)))
    return np.array(uqims)


def measure_SSIM(gtr_dir, gen_dir):
    """
      # measured in RGB
      Assumes:
        * gtr_dir contain ground-truths {filename.ext}
        * gen_dir contain generated images {filename_SESR.png} 
    """
    #gtr_paths = sorted(glob(join(gtr_dir, "*.*")))
    #gen_paths = sorted(glob(join(gen_dir, "*.*")))
    gtr_paths, gen_paths = getPaths(gtr_dir), getPaths(gen_dir)
    ssims = []
    for gtr_path in gtr_paths:
        fname = basename(gtr_path).split('.')[0]
        #gen_path = join(gen_dir, fname + '_SESR.png') # for SESR
        #gen_path = join(gen_dir, fname + '_gen.jpg') # for SRDRM
        gen_path = join(gen_dir, fname + '.jpg') # for TTSR
        #gen_path = join(gen_dir, fname + '_En.png') # enhancement
        if gen_path in gen_paths:
            r_im = Image.open(gtr_path).resize((im_w, im_h))
            g_im = Image.open(gen_path).resize((im_w, im_h))
            # get ssim on RGB channels (SOTA norm)
            ssim = getSSIM(np.array(r_im), np.array(g_im))
            ssims.append(ssim)
    return np.array(ssims)


def measure_PSNR(gtr_dir, gen_dir):
    """
      # measured in lightness channel 
      Assumes:
        * gtr_dir contain ground-truths {filename.ext}
        * gen_dir contain generated images {filename_SESR.png}
    """
    #gtr_paths = sorted(glob(join(gtr_dir, "*.*")))
    #gen_paths = sorted(glob(join(gen_dir, "*.*")))
    gtr_paths, gen_paths = getPaths(gtr_dir), getPaths(gen_dir)
    psnrs = []
    for gtr_path in gtr_paths:
        fname = basename(gtr_path).split('.')[0]
        #gen_path = join(gen_dir, fname + '_SESR.png') # for SESR
        #gen_path = join(gen_dir, fname + '_gen.jpg') # for SRDRM
        gen_path = join(gen_dir, fname + '.jpg') # for TTSR
        #gen_path = join(gen_dir, fname + '_En.png') # enhancement
        if gen_path in gen_paths:
            r_im = Image.open(gtr_path).resize((im_w, im_h))
            g_im = Image.open(gen_path).resize((im_w, im_h))
            # get psnt on L channel (SOTA norm)
            r_im = r_im.convert("L"); g_im = g_im.convert("L")
            psnr = getPSNR(np.array(r_im), np.array(g_im))
            psnrs.append(psnr)
    return np.array(psnrs)

### compute SSIM and PSNR
SSIM_measures = measure_SSIM(GTr_im_dir, GEN_im_dir)
PSNR_measures = measure_PSNR(GTr_im_dir, GEN_im_dir)
print ("SSIM >> Mean: {0} std: {1}".format(np.mean(SSIM_measures), np.std(SSIM_measures)))
print ("PSNR >> Mean: {0} std: {1}".format(np.mean(PSNR_measures), np.std(PSNR_measures)))

### compute and compare UIQMs
#gen_uqims = measure_UIQMs(GEN_im_dir, file_ext="_En.png")  # or file_ext="_SESR.png"
#gen_uqims = measure_UIQMs(GEN_im_dir, file_ext="_SESR.png") # for SESR
#gen_uqims = measure_UIQMs(GEN_im_dir, file_ext="_gen.jpg")  # for srdrm
gen_uqims = measure_UIQMs(GEN_im_dir, file_ext=".jpg")  # for TTSR
print ("Generated UQIM >> Mean: {0} std: {1}".format(np.mean(gen_uqims), np.std(gen_uqims)))


