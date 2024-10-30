from operator import mod
from aqt import mw
from .settings import DECK_NAME, NOTE_NAME
from anki.notes import Note
from anki.decks import DeckId
from anki.collection import Collection
from aqt.utils import showInfo


def get_note_type(col: Collection):
    models = col.models
    note_type = models.by_name(NOTE_NAME)
    if note_type is None:
        showInfo(f"Can't find {NOTE_NAME} model")
        raise Exception(f"Can't find {NOTE_NAME} model")
    return note_type


def create_note(note_detail: dict[str, str]) -> bool:
    if mw and mw.col:
        col = mw.col
        out = col.decks.add_normal_deck_with_name(DECK_NAME)
        deck_id = DeckId(out.id)
        note_type = get_note_type(col)
        title = note_detail.pop("Title")
        color = note_detail.pop("Color")
        note = Note(col=col, model=note_type)
        for key, value in note_detail.items():
            note[key] = value
        if title:
            note.add_tag(title)
        if color:
            note.add_tag(color)
        col.add_note(note, deck_id)
        return True
    return False
