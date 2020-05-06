import time
import board
import neopixel
import sys
from WS2811Letters import WS2811Letters
import copy

num_pixels=50
pixel_pin = board.D18
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=.1, auto_write=False, pixel_order=ORDER
)

color_wheel_index=1

def render_two_dimensional_array(arr):
    width = 10
    height = 5
    for raw_pix in range(0,width*height):
      row = ( height -1 ) - int(raw_pix/width)
      if row%2 ==0 :
        col = raw_pix % width
      else:
        col = width - (raw_pix % width) -1
      #print(f"raw pixel {raw_pix} sourced from [{row}][{col}]")
      pixels[raw_pix] = arr[row][col]
    pixels.show()

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)



def get_next_rainbow_color():
  global color_wheel_index 
  color_wheel_index+=(255/7)
  return wheel(color_wheel_index % 255)

if False:
  for i in range(0,51):
    print(f"updated {i}")
    pixels[i]=(255,255,255)
    pixels.show()
    a = input("tesT")

def draw_one_letter(letter,offset,color):
  blank = copy.deepcopy(WS2811Letters.blank_canvas)
  arr = WS2811Letters.draw_letter_on_array(blank, letter, color, offset)
  render_two_dimensional_array(arr)
  time.sleep(.2)

while False:
  string = "UPPER lower "
  for l in string:
    c = get_next_rainbow_color()
    draw_one_letter(l,2,c) 

while True:
  #on_a_call()
  rainbow_cycle(.001)
  for j in range(num_pixels):
    pixels.fill((0, 255, 0))
    pixels[j] = (0,0,255)
    pixels.show()
    time.sleep(.01)

