import os
import json
from typing import Mapping


def load_json_file(path: str) -> Mapping:
    dirname = os.path.dirname(__file__)
    file = open(os.path.join(dirname, path))
    return json.load(file)
