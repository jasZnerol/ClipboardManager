from PIL import Image, ImageDraw
from clipboard.gui.config import default_values

def merge_images(images : list):
  images = [Image.open(x).resize(default_values["image_size"], Image.ANTIALIAS) for x in images][::-1]
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

# images = [Image.open(x).resize((101, 128), Image.ANTIALIAS ) for x in  ["test1.png", "test2.jpg", "test3.jpg"]]
# img = merge_images(images)
# img.show()