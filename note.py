import argparse
from datetime import datetime

from notes_manager import NotesManager


def main():
    parser = argparse.ArgumentParser(description='Управление заметками')
    parser.add_argument('command', choices=['add', 'edit', 'delete', 'find', 'show'], help='Команда')
    parser.add_argument('--id', help='Идентификатор заметки (только для edit и delete)')
    parser.add_argument('--title', help='Заголовок заметки')
    parser.add_argument('--text', help='Тело заметки')
    parser.add_argument('--sdate', help='Начальная дата для фильтрации списка заметок (формат: ЧЧ:ММ дд.мм.гггг)')
    parser.add_argument('--edate', help='Конечная дата для фильтрации списка заметок (формат: ЧЧ:ММ дд.мм.гггг)')
    parser.add_argument('--word', help='Искомое слово')
    parser.add_argument('--all', action='store_true', help='Вывести все записи')
    parser.add_argument('-a', action='store_true', help='Вывести все записи')
    parser.add_argument('-i', action='store_true', help='Вывести результат в строку')
    args = parser.parse_args()

    notes_manager = NotesManager()

    if args.command == 'add':
        if not args.title:
            print('Не указан заголовок')
            return
        if not args.text:
            print('Не указано тело заметки')
            return
        notes_manager.add_note(args.title, args.text)

    elif args.command == 'edit':
        if not args.id:
            print('Не указан идентификатор заметки')
            return
        title = args.title or None
        text = args.text or None
        notes_manager.edit_note(args.id, title, text)

    elif args.command == 'delete':
        if not args.id:
            print('Не указан идентификатор заметки')
            return
        notes_manager.delete_note(args.id)

    elif args.command == 'find':
        if args.word:
            notes_manager.find(args.word, args.i)
            return

        if not args.sdate:
            print('Введите начальную дату поиска')
            return

        format_string = "%H:%M %d.%m.%Y"
        start_time = 0
        end_time = 0
        if args.sdate:
            try:
                start_time = datetime.strptime(args.sdate, format_string)
                start_time = start_time.replace(second=0, microsecond=0)
                start_time = start_time.timestamp()
            except:
                print('Начальная дата поиска введена не корректно')
                return
        if args.edate:
            try:
                end_time = datetime.strptime(args.edate, format_string)
                end_time = end_time.replace(second=59, microsecond=999999)
                end_time = end_time.timestamp()
            except:
                print('Конечная дата поиска введена не корректно')
                return

        notes_manager.find_by_date(start_time, end_time, args.i)

    elif args.command == 'show':

        if args.all or args.a:
            notes_manager.show_all(args.i)
            return

        if not args.id:
            print('Не указан идентификатор заметки')
            return
        notes_manager.show(args.id, args.i)

if __name__ == '__main__':
    main()

