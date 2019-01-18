# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 20:31:54 2019

@author: Yang Xu
"""

import numpy as np
import cv2

img1 = cv2.imread('dog.jpg')
img2 = cv2.imread('cat.jpg')

print(img1.shape)
print(img2.shape)

print(img1.dtype)
print(img1[0,4])

print(img2.dtype)
print(img2[0,4])

#def normalize_img(img):
    
#    img = (img-img.min())/(img.max()-img.min())
    
#    return img

def gaussin_kernal(size=(29,29),sigma=7):
    x, y =size[0],size[1]
    x, y = np.mgrid[-(x//2):(x//2)+1, -(y//2):(y//2)+1]
    g = np.exp(-((x/sigma)**2+(y/sigma)**2)/2)
    return g/g.sum()

def conv(img,kernal):
    
    n,m,d=img.shape
    a,b=kernal.shape
    
    pad1 = int((a-1)/2)
    pad2 = int((b-1)/2)
    
    pixel = np.zeros((n+(a-1),m+(b-1),d))
    for i in range(d):
        
        pixel[pad1:pad1+n,pad2:pad2+m,i] = img[:,:,i]
    
    smooth_img=np.zeros((n,m,d))
    
    for k in range(d):
        for i in range(n):
            for j in range(m):
            
                smooth_img[i,j,k]=np.multiply(kernal,pixel[i:i+pad1*2+1,j:j+pad2*2+1,k]).sum()
    
    smooth_img=smooth_img.astype(np.uint8)
            
    return smooth_img

def sharpen(img,kernal,scale_factor):
    
    smooth_img=conv(img,kernal)
    
    sharpen_img= img-scale_factor*smooth_img
    
    sharpen_img=sharpen_img.astype(np.uint8)
    
    return sharpen_img

def supposing(smooth_img,sharpen_img,ratio=(0.95,0.05)):
    
    r1=ratio[0]
    r2=ratio[1]
    
    supposed_img=smooth_img*r1+sharpen_img*r2
    
    supposed_img=supposed_img.astype(np.uint8)
    
    return supposed_img

cv2.namedWindow('image')
cv2.imshow('image',sm)
cv2.waitKey()

import scipy.misc
scipy.misc.imsave('hybrid.jpg', img2)