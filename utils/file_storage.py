import json
import os
from datetime import datetime


def save_json(data, folder="output", filename=None):

    os.makedirs(folder, exist_ok=True)

    if filename is None:

        filename = f"school_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    path = os.path.join(folder, filename)

    with open(path, "w", encoding="utf-8") as f:

        json.dump(data, f, ensure_ascii=False, indent=4)

    return path