# -*- coding: utf-8 -*-
"""
Created on Sun May  5 09:41:51 2024

@author: chris
"""
import numpy as np
from pylab import imshow, show
from timeit import default_timer as timer
from numba import jit



def mandelbrot_data_point(x, y, max_iteration):

  c = complex(x, y)
  z = 0. + 0.j
  for n in range(max_iteration):
    z = z*z + c
    if (abs(z) >= 2):
      return n
  return max_iteration


def generate_image(x_min, x_max, y_min, y_max, image_data, max_iters, x_pixels, y_pixels):
    
  row = 0
  col = - 1
  for x in np.linspace(x_min, x_max, int(x_pixels)):
      row = 0
      col += 1
      for y in np.linspace(y_min, y_max, int(y_pixels)):
          #Each pixel gets number [0, max_iter] and colored depending on how many iterations that spot reached
          image_data[row, col] = mandelbrot_data_point(x, y, max_iters)      #returns number of iterations (between 0 and max_iter) reached by c=x+iy       
          row += 1


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
def generate_image_numba(x_min, x_max, y_min, y_max, image_data, max_iters, x_pixels, y_pixels):
    
  row = 0
  col = - 1
  for x in np.linspace(x_min, x_max, x_pixels):
  # x in range(x_max) :
      row = 0
      col += 1
      for y in np.linspace(y_min, y_max, y_pixels):
          #Each pixel gets number [0, max_iter] and colored depending on how many iterations that spot reached
          image_data[row, col] = mandelbrot_data_point_nummba(x, y, max_iters)      #returns number of iterations (between 0 and max_iter) reached by c=x+iy       
          row += 1
    
    
x_pixels, y_pixels = 1536, 1024
x_min, x_max, y_min, y_max, max_iters = -2.0, 1.0, -1.0, 1.0, 500
print(f"x_min={x_min:.1f}; x_max={x_max:.1f}; y_min={y_min:.1f}; y_max={y_max:.1f}; max_iters={max_iters}")

trials = 6  
if trials > 1:
    print(f"Averaging over {trials} trials.")
    
dt = np.zeros(trials)           #time elapsed between start and finish to generate image without numba
dt_numba = np.zeros(trials)     #time elapsed between start and finish to generate image with numba

change_max_iters = True
change_xy_ranges = False

for i in range(trials):

    image = np.zeros((y_pixels, x_pixels), dtype = np.uint16)
    image_numba = np.zeros((y_pixels, x_pixels), dtype = np.uint16)
    
    start = timer()     
    generate_image(x_min, x_max, y_min, y_max, image, max_iters, x_pixels, y_pixels) 
    dt[i] = timer() - start
    
    start_numba = timer()
    generate_image_numba(x_min, x_max, y_min, y_max, image, max_iters, x_pixels, y_pixels)  
    dt_numba[i] = timer() - start_numba
    
    print(f"Mandelbrot was created in {dt[i]:.2f} s without numba and {dt_numba[i]:.2f} s with numba. {(dt[i]/dt_numba[i]):.0f}x faster")
    
    if (change_max_iters and i < (trials-1)):
        max_iters += 500
        print(f"\nIncreasing max_iters to {max_iters:.2f}")

    if (change_xy_ranges and i < (trials-1)):
        x_min += (x_max-x_min) / 4
        y_min += (y_max-y_min) / 4
        print(f"\nIncreasing x_min to {x_min:.2f}; y_min to {y_min:.2f}; max_iters to {max_iters:.2f}")

    
if trials > 1:  
    dt_avg = np.average(dt)
    dt_numba_avg = np.average(dt_numba)
    
    print(f"\nOn average, numba increased rate of computaiton by {(dt_avg/dt_numba_avg):.0f}x")

imshow(image)
show()