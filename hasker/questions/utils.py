from io import BytesIO
from PIL import Image
from django.core.mail import send_mail
from django.template.loader import render_to_string

from hasker.secrets import HASKER_SERVICE_MAIL

def crop_square(image_field, img_type):
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


def send_answer_mail(to, username, post_id, question_title):
    subject = 'Hasker: New answer on your question'

    message = render_to_string('questions/new_answer_mail.html', {'username': username,
                                                                  'question_id': post_id,
                                                                  'question_title': question_title,
                                                                  })
    send_mail(
        subject,
        message,
        HASKER_SERVICE_MAIL,
        [to,],
        fail_silently=True,
    )
