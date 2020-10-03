from flask import Flask, request, make_response, jsonify
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

def halloween():
    for i in range(num_pixels):
        pixels[i] = (245,145,44)
    pixels.show()

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

        <input type="radio" id="on-halloween" name="light_status" value="on-halloween">
        <label for="on-halloween">on-halloween</label><br>

        <input type="radio" id="on-text" name="light_status" value="on-text">
        <label for="on-text">on-text</label><br>

        <label for="text_to_show">Text to Show:</label><br>
        <input type="text" id="text_to_show" name="text_to_show" value="Test" /><br><br>

        <label for="scroll_speed">Scroll Speed</label><br>
        <input type="text" id="scroll_speed" name="scroll_speed" value="50" /><br><br>

        <label for="fg_hex">Foreground Color (Hex)</label><br>
        <input type="text" id="fg_hex" name="fg_hex" value="999999" /><br><br>

        <label for="bg_hex">Background Color</label><br>
        <input type="text" id="bg_hex" name="bg_hex" value="001199" /><br><br>

        <input type="submit">
      </form>
    </body>
    </html>
    """
  return page_string

@app.route('/set_status', methods=['GET', 'POST'])
def handle_form_post():
  light_status = request.form['light_status']
  if light_status == "off":
    pixels.fill((0,0,0))
    pixels.show()
  elif light_status == "on-rainbow":
    rainbow_cycle(.001)
  elif light_status == "on-halloween":
    halloween()
  elif light_status == "on-text":
    text_to_show = request.form['text_to_show']
    scroll_speed = int(request.form['scroll_speed'])
    fg_hex = request.form['fg_hex']
    bg_hex = request.form['bg_hex']

    ms_duration_between_frames = (1/scroll_speed) * 5

    foreground_rgb = tuple(int(fg_hex[i:i+2], 16) for i in (0, 2, 4))
    background_rgb = tuple(int(bg_hex[i:i+2], 16) for i in (0, 2, 4))

    message_pixel_buffer = WS2811Letters.render_string_to_pixel_buffer(text_to_show,foreground_rgb,background_rgb)
    message_pixel_buffer_width = len(message_pixel_buffer[0])
    necessary_scroll_increments = message_pixel_buffer_width-10

    for window_scroll_segment in range(necessary_scroll_increments):
      windowed_pixel_buffer = WS2811Letters.render_windowed_pixel_buffer(message_pixel_buffer,window_scroll_segment)
      render_two_dimensional_array(windowed_pixel_buffer)
      time.sleep(ms_duration_between_frames)

    #return jsonify(windowed_pixel_buffer)
    #for letter in text_to_show:
     # blank = copy.deepcopy(WS2811Letters.blank_canvas)
      #arr = WS2811Letters.draw_letter_on_array(blank, letter, (0,255,0), 2)
      #render_two_dimensional_array(arr)
      #time.sleep(.2)

  response = make_response("ok",301)
  response.headers['Location'] = '/'
  response.autocorrect_location_header = False
  return response