import json
import os
from datetime import datetime


def save_json(data, folder="output", filename="file_data.json"):



    path = os.path.join(folder, filename)

    with open(path, "w", encoding="utf-8") as f:

        json.dump(data, f, ensure_ascii=False, indent=4)

    return path