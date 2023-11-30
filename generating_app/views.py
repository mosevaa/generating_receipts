import jinja2
import pdfkit
import qrcode

from io import BytesIO
from datetime import datetime

from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.views import APIView

from generating_app.models import Item


def generate_pdf(items_from_db, counts):
    environment = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))
    template = environment.get_template('index.html')

    items = []
    full_price = 0
    for item in items_from_db:
        full_price += counts[item.id] * item.price
        items.append(
            {
                'title': item.title,
                'price': item.price,
                'count': counts[item.id],
                'common_price': counts[item.id] * item.price
            }
        )

    rendered_page = template.render(
        items=items,
        date=datetime.now().strftime("%d.%m.%Y %H:%M"),
        full_price=full_price
    )
    output_path = f'media/{int(datetime.now().timestamp())}.pdf'
    pdfkit.from_string(rendered_page,
                       output_path=output_path,
                       css='templates/styles.css',
                       options={"enable-local-file-access": ""})
    return output_path


class ItemView(APIView):
    def post(self, request):
        base_url = "{0}://{1}/".format(request.scheme, request.get_host())

        counts = {}
        for item_id in request.data['item']:
            if item_id not in counts.keys():
                counts[item_id] = 0
            counts[item_id] += 1
        items_from_db = Item.objects.filter(id__in=request.data['item'])

        path = generate_pdf(items_from_db, counts)

        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=4,
            border=0,
        )

        qr.add_data(base_url + path)
        qr.make(fit=True)

        img = qr.make_image()

        buffer = BytesIO()
        img.save(buffer)

        return HttpResponse(buffer.getbuffer(), content_type="image/png")


