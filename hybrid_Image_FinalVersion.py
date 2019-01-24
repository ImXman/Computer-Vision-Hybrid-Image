# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 20:31:54 2019

@author: Yang Xu
"""
import sys
import numpy as np
import cv2
import scipy.misc

##argument 1 and 2 are the path where the images are
##argument 3 and 4 indicate the filter size
##argument 5 is sigma of filter
##argument 6 is the scale factor for image sharpening
##argument 7 and 8 indicate the ratio to balance low and high pass images
##argument 9 indicates if grayscale or rbg
img1_path=str(sys.argv[1])
img2_path=str(sys.argv[2])
fs_x =int(sys.argv[3])
fs_y =int(sys.argv[4])
sig = float(sys.argv[5])
sf = float(sys.argv[6])
r1 = float(sys.argv[7])
r2 = float(sys.argv[8])

if int(sys.argv[9])==0:
    grayscale = True
else:
    grayscale = False

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

def convGray(img,kernal):
    
    n,m=img.shape
    a,b=kernal.shape
    
    pad1 = int((a-1)/2)
    pad2 = int((b-1)/2)
    
    pixel = np.zeros((n+(a-1),m+(b-1)))
        
    pixel[pad1:pad1+n,pad2:pad2+m] = img[:,:]
    
    smooth_img=np.zeros((n,m))
    
    for i in range(n):
        for j in range(m):
            
            smooth_img[i,j]=np.multiply(kernal,pixel[i:i+pad1*2+1,j:j+pad2*2+1]).sum()
    
    smooth_img=smooth_img.astype(np.uint8)
            
    return smooth_img

def sharpen(img,kernal,scale_factor):
    
    if grayscale:
        smooth_img=convGray(img,kernal)
    else:
        smooth_img=conv(img,kernal)
    
    sharpen_img= img-scale_factor*smooth_img
    
    sharpen_img=sharpen_img.astype(np.uint8)
    
    return sharpen_img

def imposing(smooth_img,sharpen_img,ratio=(0.95,0.05)):
    
    r1=ratio[0]
    r2=ratio[1]
    
    imposed_img=smooth_img*r1+sharpen_img*r2
    
    imposed_img=imposed_img.astype(np.uint8)
    
    return imposed_img


def main():
    
    if grayscale:
        img1 = cv2.imread(img1_path,0)
        img2 = cv2.imread(img2_path,0)

        gk = gaussin_kernal(size=(fs_x,fs_y),sigma=sig)

        smoothed_img = convGray(img1,gk)
        sharpened_img= sharpen(img2,gk,sf)
        hybrid_img=imposing(smoothed_img,sharpened_img,ratio=(r1,r2))
    
    else:
        img1 = cv2.imread(img1_path)
        img2 = cv2.imread(img2_path)

        gk = gaussin_kernal(size=(fs_x,fs_y),sigma=sig)

        smoothed_img = conv(img1,gk)
        sharpened_img= sharpen(img2,gk,sf)
        hybrid_img=imposing(smoothed_img,sharpened_img,ratio=(r1,r2))
    #cv2.namedWindow('image')
    #cv2.imshow('image',hybrid_img)
    #cv2.waitKey()

    scipy.misc.imsave('low_pass.jpg',smoothed_img)
    scipy.misc.imsave('high_pass.jpg',sharpened_img)
    scipy.misc.imsave('hybrid.jpg', hybrid_img)

if __name__ == '__main__':
    main()
    