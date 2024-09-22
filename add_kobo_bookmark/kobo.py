import sqlite3
from pathlib import Path
import re
from .settings import KOBO_DB
from aqt.utils import showWarning

COLORS = ["Yellow", "Pink", "Blue", "Green"]


def volumne_id_to_book_title(volumne_id: str):
    file_path = Path(volumne_id)
    title, *_ = (
        file_path.name.split("_")
        if "_" in file_path.name
        else file_path.name.split("-")
    )
    title = title.strip().lower()
    title = re.sub(r"[^\w\d\s]", "", title)
    title = title.replace(" ", "-")
    return title


def map_color(number: int):
    return COLORS[number]


def read_kobo_data():
    try:
        connection = sqlite3.connect(KOBO_DB)
        connection.text_factory = lambda x: str(x, "utf-8")
    except sqlite3.OperationalError as e:
        showWarning(str(e))
        return None

    cur = connection.cursor()
    query = cur.execute(
        """SELECT VolumeID,Color,Text,Annotation FROM Bookmark WHERE Type IN ("highlight", "note")"""
    )
    result = query.fetchall()
    return [
        {
            "Front": row[2],
            "Back": row[3],
            "Title": volumne_id_to_book_title(row[0]),
            "Color": map_color(row[1]),
        }
        for row in result
    ]
