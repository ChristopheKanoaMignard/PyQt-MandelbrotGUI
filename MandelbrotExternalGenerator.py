# -*- coding: utf-8 -*-
"""
Created on Mon May 13 15:39:45 2024

@author: chris
"""
import numpy as np
from timeit import default_timer as timer
from numba import jit


@jit
def mandelbrot_data_point_nummba(x, y, max_iteration):

  c = complex(x, y)
  z = 0. + 0.j
  for n in range(max_iteration):
    z = z*z + c
    if (abs(z) >= 2):
      return n
  return max_iteration

@jit
def generate_image_numba(x_min, x_max, y_min, y_max, max_iters, x_pixels, y_pixels):
    
    image = np.zeros((x_pixels, y_pixels), dtype = np.uint16)
    row = 0
    col = -1
    for x in np.linspace(x_min, x_max, x_pixels):
        # x in range(x_max) :
        row = 0
        col += 1
        for y in np.linspace(y_min, y_max, y_pixels):
            #Each pixel gets number [0, max_iter] and colored depending on how many iterations that spot reached
            image[col, row] = mandelbrot_data_point_nummba(x, y, max_iters)      #returns number of iterations (between 0 and max_iter) reached by c=x+iy       
            row += 1
    return image