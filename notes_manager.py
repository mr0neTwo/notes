from datetime import datetime
from db.database import Database


class NotesManager:
    def __init__(self):
        self.db = Database()

    def add_note(self, title, text):
        timestamp = datetime.now().timestamp()
        data = {
            'date': timestamp,
            'title': title,
            'text': text
        }
        self.db.notes.add(data)

    def edit_note(self, note_id, title=None, text=None):
        data = {'id': note_id}
        if title is not None:
            data['title'] = title
        if text is not None:
            data['text'] = text
        self.db.notes.edit(data)

    def delete_note(self, note_id):
        self.db.notes.deleted(str(note_id))

    def show_all(self, inline=False):
        self._print(self.db.notes.read_all(), inline)

    def show(self, note_id, inline=False):
        self._print([self.db.notes.read(note_id)], inline)

    def find(self, search_word, inline=False):
        notes = self.db.notes.read_all()
        result = []
        for note in notes:
            if search_word in note['title'] or search_word in note['text']:
                result.append(note)
        self._print(result, inline)

    def find_by_date(self, start, end=None, inline=False):
        notes = self.db.notes.read_all()
        result = []
        for note in notes:
            timestamp = float(note['date'])
            is_more_start = timestamp >= start
            is_less_end = not end or timestamp <= end
            if is_more_start and is_less_end:
                result.append(note)
        self._print(result, inline)

    def _print(self, notes, inline=False):
        if inline:
            for note in notes:
                time = datetime.fromtimestamp(float(note['date'])).strftime("%H:%M %d.%m.%Y")
                print(f'{note["id"]} {time} -- {note["title"]}: {note["text"]}')
        else:
            for note in notes:
                print()
                print('=' * 3 + f' Note {note["id"]} ' + '=' * 40)
                print(f'Date: {datetime.fromtimestamp(float(note["date"])).strftime("%H:%M %d.%m.%Y")}')
                print(f'Title: {note["title"]}')
                print(f'Note: {note["text"]}')


if __name__ == "__main__":
    nm = NotesManager()
    # nm.add_note('title4', 'text4')
    # nm.add_note('title5', 'text5')
    # nm.add_note('title6', 'text6')
    nm.delete_note('3')
    nm.edit_note('7', text='ooo')

    format_string = "%H:%M %d.%m.%Y"
    start_time = datetime.strptime('13:19 29.06.2023', format_string)
    start_time = start_time.replace(second=0, microsecond=0)
    start_time = start_time.timestamp()
    end_time = datetime.strptime('13:21 29.06.2023', format_string)
    end_time = end_time.replace(second=59, microsecond=999999)
    end_time = end_time.timestamp()


    nm.find_by_date(start_time, end_time, inline=True)
