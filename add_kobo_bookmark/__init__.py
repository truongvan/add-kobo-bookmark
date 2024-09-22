from aqt import mw
from aqt.utils import showInfo, qconnect
from aqt.qt import *

from .create_note import create_note
from .kobo import read_kobo_data
from .settings import DECK_NAME, NOTE_NAME


def add_kobo_bookmarks() -> None:
    bookmarks = read_kobo_data()
    if bookmarks is None:
        return None
    exited_words = []
    error_words = []
    if mw and mw.col and mw.col.db:
        card_ids = mw.col.find_cards(f"deck:{DECK_NAME} note:{NOTE_NAME}")
        exited_words = [mw.col.get_card(i).note()["Front"] for i in card_ids]

    bookmark_added = 0
    for bookmark in bookmarks:
        if bookmark["Front"] in exited_words:
            continue
        success = create_note(bookmark)
        if success:
            bookmark_added += 1
    if len(error_words) > 0:
        showInfo(f"Added fail: {error_words}")
    showInfo(f"Added: {bookmark_added}")
    return None


action = QAction("Add Kobo Bookmarks", mw)
qconnect(action.triggered, add_kobo_bookmarks)
mw.form.menuTools.addAction(action)
