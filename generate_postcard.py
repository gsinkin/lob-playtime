import os
import json
import urllib2
import logging
from cStringIO import StringIO

from PIL import Image
import lob
from reportlab.lib import utils
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

logger = logging.getLogger()
lob.api_key = os.environ["LOB_API_KEY"]
GIPHY_API_KEY = os.environ["GIPHY_API_KEY"]


def get_random_image():
    logger.debug("Getting random image")
    request = urllib2.Request(
        "https://api.giphy.com/v1/gifs/random?api_key={0}"
        "&tag=&rating=PG-13".format(GIPHY_API_KEY))
    response = urllib2.urlopen(request).read()
    loaded = json.loads(response)
    image_data = loaded["data"]
    return {
        "image_io": StringIO(
            urllib2.urlopen(image_data["image_original_url"]).read()
        ),
        "width": image_data["image_width"],
        "height": image_data["image_height"],
    }


def generate_pdf(image_width=2.25 * inch):
    image = get_random_image()
    logger.debug("Generating pdf")
    result = StringIO()
    height, width = (4.25 * inch, 6.25 * inch)
    pdf_canvas = canvas.Canvas(result, pagesize=(width, height))
    pil_image = Image.open(image["image_io"])
    image["image_io"].seek(0)
    img = utils.ImageReader(image["image_io"])
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    pdf_canvas.drawInlineImage(
        pil_image, 0.25 * inch, 0.25 * inch,
        width=image_width, height=(image_width * aspect))
    pdf_canvas.showPage()
    pdf_canvas.save()
    result.seek(0)
    return result


def generate_postcard(front_pdf, back_pdf):
    logger.debug("Generating postcard")
    postcard = lob.Postcard.create(
        to_address={
            'name': 'Kate Cryan',
            'address_line1': '346 51st St',
            'address_city': 'Oakland',
            'address_state': 'CA',
            'address_zip': '94609',
            'address_country': 'US'
        },
        from_address={
            'name': 'Gabe Sinkin',
            'address_line1': '346 51st St',
            'address_city': 'Oakland',
            'address_state': 'CA',
            'address_zip': '94609',
            'address_country': 'US'
        },
        front=front_pdf,
        back=back_pdf,
    )
    return postcard


def make_postcard():
    front_pdf = generate_pdf(image_width=5 * inch)
    back_pdf = generate_pdf()
    postcard = generate_postcard(front_pdf, back_pdf)
    print postcard


if __name__ == "__main__":
    make_postcard()
