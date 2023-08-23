from datetime import datetime as dt
import re
import ast


def print_remaining_time(_appointment_info_list, _current_date, _type):
    event_title = _appointment_info_list.pop(-1)
    if _type == "birthday":
        birthday = dt(_appointment_info_list[0], _appointment_info_list[1], _appointment_info_list[2]).date()
        month = _appointment_info_list[1]
        day = _appointment_info_list[2]
        year = dt.now().year if month > dt.now().month or (month == dt.now().month and day >= dt.now().day) else dt.now().year + 1
        remaining = dt(year, month, day).date() - dt.now().date()
        if remaining.days == 0:
            print(f"{event_title}’s birthday is today. He (she) turns {year - birthday.year} years old.\n")
        else:
            print(f"{event_title}’s birthday is in {remaining.days} days. He (she) turns {year - birthday.year} years old.\n")
    elif _type == "note":
        appointment_date = dt(*_appointment_info_list)
        print(f'Before the event note "{event_title}" remains: ', end="")
        d = appointment_date - _current_date
        print(f"{d.days} day(s), {d.seconds // 60 // 60} hour(s) and {d.seconds // 60%60} minute(s).")


def get_event_inputs_and_write(_current_date, _add):
    notes = open("notes.txt", "a")
    for n in range(_add):
        _data = check_datetime_input(input(f"Enter date and time of note #{n + 1} (in format «YYYY-MM-DD HH:MM»):\n"))
        _data.append(input(f"Enter text of note #{n + 1}:\n"))
        notes.write(str(_data) + "\n")
    notes.close()
    print("Notes added!")
    return _data


def check_datetime_input(datetime_input):
    while True:
        data = []
        try:
            unformatted_data = re.split(" ", datetime_input.replace("-", " "))
            if len(unformatted_data) > 4 or ":" not in unformatted_data[-1]:
                raise Exception
            for e in unformatted_data[:-1]:
                data.append(int(e))
            for e in unformatted_data[-1].split(":"):
                data.append(int(e))

            if data[1] not in range(1, 13):
                print("Incorrect month value. The month should be in 01-12")
            elif data[3] not in range(0, 24):
                print("Incorrect hour value. The hour should be in 00-23.")
            elif data[4] not in range(0, 60):
                print("Incorrect minute value. The minutes should be in 00-59.")
            else:
                return data
        except Exception:
            print("Incorrect format. Please try again (use the format «YYYY-MM-DD HH:MM»)")


def check_date(date_input):
    while True:
        data = []
        try:
            unformatted_data = re.split("-", date_input)
            if len(unformatted_data) > 3:
                raise Exception
            for e in unformatted_data:
                data.append(int(e))
            if data[1] not in range(1, 13):
                print("Incorrect month value. The month should be in 01-12")
            else:
                return data
        except Exception:
            print("Incorrect format. Please try again (use the format «YYYY-MM-DD»)")
        appointment_input = input("Please try again:")


def check_notes(_current_date, notes, _type, text):
    notes = open(notes, "r")
    count = 0
    l = []
    text_list = []
    replaceable = ["[", "]", "'", "\n"]
    for line in notes:
        if text in line:
            count += 1
            info = line
            for x in replaceable:
                info = info.replace(x, "")
            info = info.split(", ")
            text_1 = info.pop(-1)
            text_list.append(text_1)
            info = list(map(int, info))
            info.append(text_1)
            l.append(info)
    if count > 0:
        print(f'Found {count} note(s) that contain "{text}":')
    else:
        print("No such note found. Try again:")
    for el in l:
        print_remaining_time(el, _current_date, _type)
    notes.close()
    return count if count == 0 else text_list


def delete_appointment(delete_text):
    while True:
        count = 0
        appointment = delete_text
        notes = open("notes.txt", "r")
        string = str(notes.read()).split("\n")
        for line in string:
            if appointment in line:
                count += 1
                line_list = ast.literal_eval(line)
                # string.remove(line)

                choice = input(f'Are you sure you want to delete "{line_list[-1]}"?')
                if choice == "yes":
                    string.remove(line)
                    print("Note deletedd!")
                elif choice == "no":
                    print("Deletion canceled.")
        notes.close()
        notes = open("notes.txt", "w")
        for element in string:
            notes.write(str(element) + "\n")
        notes.close()
        if count == 0:
            print("No notes with such text were found. Try again:")
            continue
        break


def del_birthday(text_or_date, delete="True"):
    text = text_or_date
    while True:
        count = 0
        notes = open("b_notes.txt", "r")
        string = str(notes.read()).split("\n")
        for line in string:
            if text in line:
                count += 1
                line_list = ast.literal_eval(line)
                print_remaining_time(list(line_list), dt.now(), "birthday")
                if delete == "True":
                    choice = input(f'Are you sure you want to delete "{line_list[-1]}"?\n')
                    if choice == "yes":
                        string.remove(line)
                        print("Birthdate deleted!")
                    elif choice == "no":
                        print("Deletion canceled.")
        notes.close()

        notes = open("b_notes.txt", "w")
        for element in string:
            notes.write(str(element) + "\n")
        notes.close()
        if count == 0:
            text = input("No such person found. Try again:")
            continue
        break


def add_birthday(_b_add):
    notes = open("b_notes.txt", "a")
    for n in range(_b_add):
        text = input(f"Enter the name of #{n + 1}:")
        data = check_date(input(f"Enter the date of birth of #{n + 1} (in format «YYYY-MM-DD»):\n"))
        data.append(text)
        notes.write(str(data) + "\n")
    notes.close()
    print("Birthdates added")


def search_date_in_notes(_current_date, notes="both"):
    n_count = 0
    b_count = 0
    n_del_list = []
    b_del_list = []
    if notes == "both":
        string = input("Enter date (in format «YYYY-MM-DD»):\n").split("-")
        search_date = list(map(int, string))
        notes_list = ["notes.txt", "b_notes.txt"]
    else:
        notes_list = notes
    for n in range(2):
        if n == 0 or (n_count or b_count):
            for note_file in notes_list:
                notes = open(note_file, "r")
                for line in notes:
                    if "[" in line:
                        l = ast.literal_eval(line)
                        if note_file == "notes.txt":
                            if search_date[:3] == l[:3]:
                                n_count += 1
                                if n == 1:
                                    n_del_list.append(list(l))
                                    print_remaining_time(l, _current_date, "note")
                        elif note_file == "b_notes.txt":
                            if search_date[1:3] == l[1:3]:
                                b_count += 1
                                if n == 1:
                                    b_del_list.append(list(l))
                                    print_remaining_time(l, _current_date, "birthday")

                notes.close()
            if n == 0:
                print(f"Found {n_count} note(s) and {b_count} date(s) of birth on this date:\n")

    return n_del_list, b_del_list


def menu():
    current_date = dt.now()
    print("Current date and time:\n" + str(str(current_date)[:16]))
    while True:
        while True:
            choice = input("\nEnter the command (add, view, delete, exit):\n")
            if choice not in ["add", "view", "delete", "exit"]:
                print("This command is not in the menu\n")
            else:
                break
        if choice == "add":
            while True:
                sub_choice = input("\nWhat do you want to add (note, birthday)?\n")
                if sub_choice not in ["note", "birthday"]:
                    print("This command is not valid")
                else:
                    if sub_choice == "note":
                        add = int(input("\nHow many notes do you want to add?\n"))
                        get_event_inputs_and_write(current_date, add)
                        pass
                    elif sub_choice == "birthday":
                        b_add = int(input("\nHow many dates of birth do you want to add?\n"))
                        add_birthday(b_add)
                        pass
                    break
        elif choice in ["view", "delete"]:
            print("lol")
            while True:
                sub_choice = input(f"\nWhat do you want to {choice} (date, note, name)?\n")
                if sub_choice not in ["date", "note", "name"]:
                    print("This command is not valid")
                    continue
                else:
                    if sub_choice == "date":
                        delete_list = search_date_in_notes(current_date)
                        if choice == "delete":
                            if delete_list[0]:
                                for el in delete_list[0]:
                                    delete_appointment(el[-1])
                            if delete_list[1]:
                                for ele in delete_list[1]:
                                    del_birthday(str(ele))
                    elif sub_choice == "note":
                        text = input("\nEnter text of note:\n")
                        while True:
                            x = check_notes(dt.now(), "notes.txt", "note", text)
                            if x == 0:
                                text = input()
                            else:
                                if choice == "delete":
                                    for el in x:
                                        delete_appointment(el)
                                break

                    elif sub_choice == "name":
                        text = input("Enter name:\n")
                        if choice == "view":
                            del_birthday(text, delete="False")
                        if choice == "delete":
                            del_birthday(text)

                    break
        elif choice == "exit":
            exit()


menu()
