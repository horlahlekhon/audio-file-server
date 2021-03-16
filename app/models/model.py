from datetime import datetime
from enum import Enum

from app import db

# Alias common DB names
Column = db.Column
Model = db.Model
relationship = db.relationship


class FiletypeEnum(Enum):
    AUDIO_BOOK = "audio_book"
    SONG = "song"
    PODCAST = "podcast"


class AudioBase(db.Model):
    __abstract__ = True

    id = Column(db.Integer, primary_key=True)
    duration = Column(db.Integer, unique=False, index=False)
    uploaded_time = Column(db.DateTime, unique=False, index=False)
    ts_created = Column(db.DateTime, default=datetime.now)
    ts_updated = Column(db.DateTime, onupdate=datetime.now, default=datetime.now)
    file_path = Column(db.String, nullable=True)


    def __init__(self, *args, **kwargs):
        super(AudioBase, self).__init__(*args, **kwargs)


class Song(AudioBase):
    """ User model for storing audio related data """
    name = Column(db.String(100), unique=False, nullable=False)

    def __repr__(self):
        return f"Song(name = {self.name}, duration = {self.duration}, id = {self.id})"


class Podcast(AudioBase):
    name = Column(db.String(100), unique=False, nullable=False)
    host = Column(db.String(100), unique=False, nullable=False)
    participants = Column(db.ARRAY(item_type=db.String(100)))

    def __repr__(self):
        return f"Podcast(name = {self.name}," \
               f" host = {self.host}," \
               f" participants_size = {len(self.participants)})"


class AudioBook(AudioBase):
    __tablename__ = "audio_books"
    title = Column(db.String(100), nullable=False)
    author = Column(db.String(100), nullable=False)
    narrator = Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"AudioBook(title = {self.title}, author = {self.author}, narrator = {self.narrator})"
