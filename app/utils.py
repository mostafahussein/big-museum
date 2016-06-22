from app import app


def get_fulness(keys):
    keys = set(keys)
    counter = 0

    for k in app.config['XML_FULNESS_KEYS']:
        if k in keys:
            counter += 1

    return int(counter / len(app.config['XML_FULNESS_KEYS']) * 100)
