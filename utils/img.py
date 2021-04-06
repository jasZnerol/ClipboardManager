from PIL import Image, ImageFilter, ImageEnhance
from clipboard.gui.config import default_values

def merge_images(images : list):
  images = [make_shadow(Image.open(x), 5, 10, [5,5]).resize(default_values["image_size"], Image.ANTIALIAS) for x in images][::-1]
  # All images have the same size
  # If n := len(images) then we take a n-th of each image (cut vertically) and merge those together
  width, height = 101, 128#(default_values["image_size"])
  new_image = Image.new("RGB", default_values["image_size"])

  x_offset = 0
  for i, img in enumerate(images):
    cropped_img = img.crop((0, 0, int(width / len(images)), height))
    new_image.paste(img, (x_offset, 0))
    x_offset = x_offset + cropped_img.size[0]
  return new_image


def path_to_html_image(image):
  pass

def make_shadow(image, iterations, border, offset, background_colour=(255,255,255), shadow_colour=(0,0,0)):
  # image: base image to give a drop shadow
  # iterations: number of times to apply the blur filter to the shadow
  # border: border to give the image to leave space for the shadow
  # offset: offset of the shadow as [x,y]
  # background_cOlour: colour of the background
  # shadow_colour: colour of the drop shadow
  
  #Calculate the size of the shadow's image
  full_width  = image.size[0] + abs(offset[0]) + 2*border
  full_height = image.size[1] + abs(offset[1]) + 2*border
  
  #Create the shadow's image. Match the parent image's mode.
  shadow = Image.new(image.mode, (full_width, full_height), background_colour)
  
  # Place the shadow, with the required offset
  shadow_left = border + max(offset[0], 0) #if <0, push the rest of the image right
  shadow_top  = border + max(offset[1], 0) #if <0, push the rest of the image down
  #Paste in the constant colour
  shadow_colour= (0,0,0)
  shadow = shadow.convert()
  shadow.paste(shadow_colour,
    box=(shadow_left, shadow_top,
    shadow_left + image.size[0],
    shadow_top  + image.size[1]))
  
  # Apply the BLUR filter repeatedly
  for i in range(iterations):
    shadow = shadow.filter(ImageFilter.BLUR)

  # Paste the original image on top of the shadow 
  img_left = border - min(offset[0], 0) #if the shadow offset was <0, push right
  img_top  = border - min(offset[1], 0) #if the shadow offset was <0, push down
  shadow.paste(image, (img_left, img_top))
  return shadow.crop((border, border, full_width - border, full_height - border))
