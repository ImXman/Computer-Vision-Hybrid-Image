# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 21:52:29 2019

@author: Yang Xu
"""

import numpy as np
import cv2

import gaussin_filter as gf
import conv_img as conv

img1 = cv2.imread('dog.jpg')
img2 = cv2.imread('cat.jpg')

gk = gf.gaussin_kernal()

smoothed_img = conv.conv(img1,gk)
sharpened_img= conv.sharpening(img2,gk,1)
hybrid_img=conv.supposing(smoothed_img,sharpened_img,ratio=(0.95,0.05))

cv2.namedWindow('image')
cv2.imshow('image',hybrid_img)
cv2.waitKey()

import scipy.misc
scipy.misc.imsave('hybrid.jpg', hybrid_img)
