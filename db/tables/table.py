import csv
import os


class Table:
    def __init__(self, filename, fieldnames):
        self.filename = filename
        self.fieldnames = ['id'] + fieldnames

    def read(self, row_id):

        if not self._is_file_exist:
            return None

        with open(self.filename, 'r') as csvfile:

            reader = csv.DictReader(csvfile, delimiter=';')

            for row in reader:
                if row['id'] == row_id:
                    return row

    def read_all(self):

        if not self._is_file_exist:
            return None

        with open(self.filename, 'r') as csvfile:

            reader = csv.DictReader(csvfile, delimiter=';')

            result = []

            for row in reader:
                result.append(row)

        return result

    def add(self, data):

        if not os.path.exists(self.filename):
            self._write_field_names()
            current_id = 0
        else:
            current_id = self._get_current_id()

        with open(self.filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=self.fieldnames)
            data['id'] = current_id
            writer.writerow(data)

    def edit(self, data):

        rows = []
        was_edit = False

        with open(self.filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                if row['id'] == data['id']:
                    for key, value in data.items():
                       row[key] = value
                    was_edit = True
                rows.append(row)

        if was_edit:
            with open(self.filename, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=self.fieldnames)
                writer.writeheader()
                writer.writerows(rows)

    def deleted(self, row_id):

        rows = []
        record_deleted = False

        with open(self.filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                if row['id'] != row_id:
                    rows.append(row)
                else:
                    record_deleted = True

        if record_deleted:
            with open(self.filename, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=self.fieldnames)
                writer.writeheader()
                writer.writerows(rows)

    def _write_field_names(self):
        with open(self.filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=self.fieldnames)
            writer.writeheader()

    def _is_file_exist(self):
        return os.path.exists(self.filename)

    def _get_current_id(self):
        with open(self.filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            current_id = 0
            for row in reader:
                current_id = row['id']
            current_id = int(current_id) + 1
        return current_id
