# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 21:35:09 2019

@author: Yang Xu
"""

import numpy as np

def gaussin_kernal(size=(29,29),sigma=7):
    x, y =size[0],size[1]
    x, y = np.mgrid[-(x//2):(x//2)+1, -(y//2):(y//2)+1]
    g = np.exp(-((x/sigma)**2+(y/sigma)**2)/2)
    return g/g.sum()
