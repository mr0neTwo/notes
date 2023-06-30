from db.tables.table import Table


class Database:

    def __init__(self):
        self.data_folder = 'db/files/'
        self.notes = Table(self._file_name('notes'), ['date', 'title', 'text'])

    def _file_name(self, name):
        return f'{self.data_folder}{name}.csv'
