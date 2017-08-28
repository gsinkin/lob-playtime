import os
from cStringIO import StringIO

import lob
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

lob.api_key = os.environ["LOB_API_KEY"]


def generate_pdf():
    result = StringIO()
    height, width = (4.25 * inch, 6.25 * inch)
    pdf_canvas = canvas.Canvas(result, pagesize=(width, height))
    pdf_canvas.setFont("Helvetica-Bold", 16)
    pdf_canvas.drawString(100, 100, "Hello World")
    pdf_canvas.showPage()
    pdf_canvas.save()
    result.seek(0)
    return result


def generate_postcard(front_pdf, back_pdf):
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
    front_pdf = generate_pdf()
    back_pdf = generate_pdf()
    postcard = generate_postcard(front_pdf, back_pdf)
    print postcard


if __name__ == "__main__":
    make_postcard()
