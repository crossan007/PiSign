class WS2811Letters:
  r= (0,255,0)
  b = (0,0,0)

  blank_canvas = [
    [b,b,b,b,b,b,b,b,b,b],
    [b,b,b,b,b,b,b,b,b,b],
    [b,b,b,b,b,b,b,b,b,b],
    [b,b,b,b,b,b,b,b,b,b],
    [b,b,b,b,b,b,b,b,b,b]
  ]


  @staticmethod
  def get_letter_pixel_array(letter):
    if letter in WS2811Letters.letters:
      l = WS2811Letters.letters[letter]
    elif letter.upper() in WS2811Letters.letters:
      l = WS2811Letters.letters[letter.upper()]
    elif letter.lower() in WS2811Letters.letters:
      l = WS2811Letters.letters[letter.lower()]
    return l

  @staticmethod
  def draw_letter_on_array(arr, letter, color, offset_x):
    i_offset = 0
    l = WS2811Letters.get_letter_pixel_array(letter)

    for i in range(len(l)):
      for y in range(len(l[i])):
        arr[i+i_offset][y+offset_x] = color if l[i][y] else (0,0,0)
    return arr
  
  @staticmethod
  def render_string_to_pixel_buffer(message,foreground_color,background_color):
    pixel_buffer_height = 5
    pixel_buffer_width = 0
    margin_right = 1

    for c in message:
      pixel_buffer_width += len(WS2811Letters.get_letter_pixel_array(c)[0]) + margin_right
  
    pixel_buffer = [[background_color for x in range(pixel_buffer_width)] for y in range(pixel_buffer_height)]

    offset_x = 0
    for c in message:
      WS2811Letters.draw_letter_on_array(pixel_buffer, c, foreground_color, offset_x)
      offset_x += len(WS2811Letters.get_letter_pixel_array(c)[0]) + margin_right
    
    return pixel_buffer

  @staticmethod
  def render_windowed_pixel_buffer(pixel_buffer, offset_x):
    pixel_buffer_height = 5
    pixel_buffer_width = 10
    new_pixel_buffer = [[[0] for x in range(pixel_buffer_width)] for y in range(pixel_buffer_height)]

    for r in range(pixel_buffer_height):
      for c in range(pixel_buffer_width):
        new_pixel_buffer[r][c] = pixel_buffer[r][c+offset_x]
    return new_pixel_buffer

  letters = {}

  letters['A'] = [
    [1,1,1],
    [1,0,1],
    [1,1,1],
    [1,0,1],
    [1,0,1]
  ]

  letters['a'] = [
    [0,1,1,0],
    [0,0,0,1],
    [0,1,1,1],
    [1,0,0,1],
    [0,1,1,1]
  ]

  letters['B'] = [
    [1,1,0],
    [1,0,1],
    [1,1,1],
    [1,0,1],
    [1,1,0]
  ]

  letters['C'] = [
    [1,1,1],
    [1,0,0],
    [1,0,0],
    [1,0,0],
    [1,1,1]
  ]

  letters['D'] = [
    [1,1,0],
    [1,0,1],
    [1,0,1],
    [1,0,1],
    [1,1,0]
  ]

  letters['e'] = [
    [0,1,0],
    [1,0,1],
    [1,1,1],
    [1,0,0],
    [0,1,0]
  ]

  letters['E'] = [
    [1,1,1],
    [1,0,0],
    [1,1,1],
    [1,0,0],
    [1,1,1]
  ]

  letters['F'] = [
    [1,1,1],
    [1,0,0],
    [1,1,1],
    [1,0,0],
    [1,0,0]
  ]

  letters['g'] = [
    [0,1,1,0],
    [0,0,0,1],
    [0,1,1,1],
    [1,0,0,1],
    [0,1,1,1]
  ]

  letters['G'] = [
    [0,1,1,1],
    [1,0,0,0],
    [1,0,1,1],
    [1,0,0,1],
    [0,1,1,1]
  ]

  letters['H'] = [
    [1,0,1],
    [1,0,1],
    [1,1,1],
    [1,0,1],
    [1,0,1]
  ]

  letters['I'] = [
    [1,1,1],
    [0,1,0],
    [0,1,0],
    [0,1,0],
    [1,1,1]
  ]

  letters['J'] = [
    [0,0,1],
    [0,0,1],
    [0,0,1],
    [1,0,1],
    [1,1,1]
  ]

  letters['K'] = [
    [1,0,0],
    [1,0,1],
    [1,1,0],
    [1,1,0],
    [1,0,1]
  ]

  letters['L'] = [
    [1,0,0],
    [1,0,0],
    [1,0,0],
    [1,0,0],
    [1,1,1]
  ]

  letters['l'] = [
    [0,0,0],
    [1,0,0],
    [1,0,0],
    [1,0,0],
    [0,1,1]
  ]

  letters['M'] = [
    [0,0,0,0,0],
    [0,1,0,1,0],
    [1,0,1,0,1],
    [1,0,1,0,1],
    [1,0,1,0,1]
  ]

  letters['n'] = [
    [0,0,0,0],
    [0,1,1,0],
    [1,0,0,1],
    [1,0,0,1],
    [1,0,0,1]
  ]

  letters['N'] = [
    [1,0,0,0,1],
    [1,1,0,0,1],
    [1,0,1,0,1],
    [1,0,0,1,1],
    [1,0,0,0,1]
  ]

  letters['O'] = [
    [0,1,1,0],
    [1,0,0,1],
    [1,0,0,1],
    [1,0,0,1],
    [0,1,1,0]
  ]

  letters['o'] = [
    [0,0,0,0],
    [0,1,1,0],
    [1,0,0,1],
    [1,0,0,1],
    [0,1,1,0]
  ]

  letters['P'] = [
    [1,1,1],
    [1,0,1],
    [1,1,1],
    [1,0,0],
    [1,0,0]
  ]

  letters['p'] = [
    [0,1,0],
    [1,0,1],
    [1,1,1],
    [1,0,0],
    [1,0,0]
  ]

  letters['Q'] = [
    [0,1,1,0],
    [1,0,0,1],
    [1,0,0,1],
    [1,0,1,0],
    [0,1,0,1]
  ]

  letters['R'] = [
    [1,1,1,1],
    [1,0,0,1],
    [1,1,1,1],
    [1,0,1,0],
    [1,0,0,1]
  ]

  letters['S'] = [
    [0,1,1,1],
    [1,0,0,0],
    [0,1,1,0],
    [0,0,0,1],
    [1,1,1,0]
  ]

  letters['T'] = [
    [1,1,1],
    [0,1,0],
    [0,1,0],
    [0,1,0],
    [0,1,0]
  ]

  letters['U'] = [
    [1,0,0,1],
    [1,0,0,1],
    [1,0,0,1],
    [1,0,0,1],
    [1,1,1,1]
  ]

  letters['V'] = [
    [1,0,1],
    [1,0,1],
    [1,0,1],
    [1,0,1],
    [0,1,0]
  ]

  letters['W'] = [
    [1,0,1,0,1],
    [1,0,1,0,1],
    [1,0,1,0,1],
    [1,0,1,0,1],
    [0,1,0,1,0]
  ]

  letters['w'] = [
    [0,0,0,0,0],
    [1,0,1,0,1],
    [1,0,1,0,1],
    [1,0,1,0,1],
    [0,1,0,1,0]
  ]

  letters['X'] = [
    [0,0,0,0],
    [1,0,0,1],
    [0,1,1,0],
    [0,1,1,0],
    [1,0,0,1]
  ]

  letters['Y'] = [
    [1,0,0,0,1],
    [0,1,0,1,0],
    [0,0,1,0,0],
    [0,0,1,0,0],
    [0,0,1,0,0]
  ]

  letters['Z'] = [
    [1,1,1,1],
    [0,0,1,0],
    [0,1,0,0],
    [1,0,0,0],
    [1,1,1,1]
  ]


  letters[' '] = [
    [0,0,0],
    [0,0,0],
    [0,0,0],
    [0,0,0],
    [0,0,0]
  ]