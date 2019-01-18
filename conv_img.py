# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 21:37:02 2019

@author: Yang Xu
"""

import numpy as np

##output image has the same resolution as the input image.
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

def sharpening(img,kernal,scale_factor):
    
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
