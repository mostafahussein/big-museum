import xml.etree.ElementTree as etree

import celery

from app.utils import get_fulness


@celery.task(bind=True)
def parse_xml(self, filename):
    try:
        tree = etree.parse(filename)
    except etree.ParseError:
        return {'status': False, 'message': 'Invalid file type'}

    items = tree.getroot()

    if items.tag != 'Items':
        return {'status': False, 'message': 'Invalid file structure'}

    current_item = 0
    fulness = []

    for item in items:
        if item.tag == 'Item':
            fulness.append(get_fulness([el.tag for el in item if el.text.strip() != '']))
            current_item += 1
            self.update_state(state='PROGRESS', meta={'status': True, 'current': current_item})

    return {'status': True, 'current': current_item, 'fulness': sum(fulness)/current_item}
