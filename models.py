from pydantic import BaseModel


class AlfredItem(BaseModel):
    title: str
    subtitle: str
    arg: str
    autocomplete: str
    valid: bool


class Anime(BaseModel):
    name: str
    source: str
    date: str
    url: str


class Series(BaseModel):
    name: str
    url: str

    def to_alfred_record(self):
        return {'title': self.name, 'subtitle': self.url, 'arg': self.url}


class Episode(BaseModel):
    name: str
    source: str
    date: str
    url: str

    def to_alfred_record(self):
        return {'title': self.name, 'subtitle': f'{self.source} - {self.date}', 'arg': self.url}


class Player(BaseModel):
    server: str
    link: str
    url: str

    def to_alfred_record(self):
        return {'title': self.server, 'subtitle': self.link, 'arg': self.url}
