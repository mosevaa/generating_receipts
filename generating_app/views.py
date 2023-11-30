import jinja2
import pdfkit

from datetime import datetime
from rest_framework.response import Response
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
    pdfkit.from_string(rendered_page,
                       output_path=f'media\\{int(datetime.now().timestamp())}.pdf',
                       css='templates\\styles.css',
                       options={"enable-local-file-access": ""})


class ItemView(APIView):
    def post(self, request):
        counts = {}
        for item_id in request.data['item']:
            if item_id not in counts.keys():
                counts[item_id] = 0
            counts[item_id] += 1
        items_from_db = Item.objects.filter(id__in=request.data['item'])

        generate_pdf(items_from_db, counts)
        return Response([])

