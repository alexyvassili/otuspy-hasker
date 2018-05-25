from django.core.files.images import get_image_dimensions
from easy_thumbnails.files import get_thumbnailer
from io import BytesIO
from PIL import Image


def crop_square(image_field, img_type):
    # width, height = get_image_dimensions(image)

    # thumbnailer = get_thumbnailer(image)
    # thumbnail_options = {
    #     'crop': 'smart',
    #     'upscale': True,
    #     'size': (square_len, square_len)
    # }
    image_file = BytesIO(image_field.read())
    image = Image.open(image_file)
    width, height = image.size  # Get dimensions
    print('Dimensions', width, height)
    square_len = min(width, height)
    left = 0
    top = 0
    right = square_len
    bottom = square_len
    image = image.crop((left, top, right, bottom))
    image_file = BytesIO()
    image.save(image_file, img_type, quality=90)
    return image_file
