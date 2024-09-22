from aqt import mw
from .settings import DECK_NAME, NOTE_NAME
from anki.notes import Note
from anki.decks import DeckId
from anki.collection import Collection


def create_model(col: Collection):
    models = col.models
    new_model = models.new(NOTE_NAME)
    return new_model


def create_note(note_detail: dict[str, str]) -> bool:
    if mw and mw.col:
        col = mw.col
        out = col.decks.add_normal_deck_with_name(DECK_NAME)
        deck_id = DeckId(out.id)
        model = col.models.by_name(NOTE_NAME)
        if model is None:
            model = create_model(col)
        title = note_detail.pop("Title")
        color = note_detail.pop("Color")
        note = Note(col=col, model=model)
        for key, value in note_detail.items():
            note[key] = value
        if title:
            note.add_tag(title)
        if color:
            note.add_tag(color)
        col.add_note(note, deck_id)
        return True
    return False
