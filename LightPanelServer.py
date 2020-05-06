from flask import Flask, request, make_response
import time
import board
import neopixel
import sys
from WS2811Letters import WS2811Letters
import copy

app = Flask(__name__)

num_pixels=50
pixel_pin = board.D18
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(
  pixel_pin, num_pixels, brightness=.1, auto_write=False, pixel_order=ORDER
)

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


@app.route('/')
def hello_world():
  page_string ="""
    <html>
    <body>
      <form action="/set_status" method="post">
        <input type="radio" id="off" name="light_status" value="off">
        <label for="off">Off</label><br>

        <input type="radio" id="on-rainbow" name="light_status" value="on-rainbow">
        <label for="on-rainbow">on-rainbow</label><br>

        <input type="radio" id="on-text" name="light_status" value="on-text">
        <label for="on-text">on-text</label><br>

        <label for="text_to_show">Text to Show:</label><br>
        <input type="text" id="text_to_show" name="text_to_show" value="Test" /><br><br>

        <input type="submit">
      </form>
    </body>
    </html>
    """
  return page_string

@app.route('/off')
def turn_lights_off():
  
  response = make_response("ok",301)
  response.headers['Location'] = '/'
  return response

@app.route('/set_status', methods=['GET', 'POST'])
def handle_form_post():
  light_status = request.form['light_status']
  if light_status == "off":
    pixels.fill((0,0,0))
    pixels.show()
  elif light_status == "on-rainbow":
    rainbow_cycle(.001)
  elif light_status == "on-text":
    text_to_show = request.form['text_to_show']
    for letter in text_to_show:
      blank = copy.deepcopy(WS2811Letters.blank_canvas)
      arr = WS2811Letters.draw_letter_on_array(blank, letter, (0,255,0), 2)
      render_two_dimensional_array(arr)
      time.sleep(.2)

  response = make_response("ok",301)
  response.headers['Location'] = '/'
  return response