import datetime
import os
import json
from prettytable import PrettyTable

class State:
    def __init__(self):
        self.data_file = "data_file_expense.json"
        self.data = {}

class Save_and_Load:
    def load(self, shared):
            if os.path.exists(shared.data_file):
                try:
                    with open(shared.data_file, "r", encoding="utf-8") as f:
                        shared.data = json.load(f)
                except (json.JSONDecodeError, FileNotFoundError):
                    print(f"Warning: Could not load {shared.data_file}. Starting with empty file.")
                    shared.data = {}
            else:
                shared.data = {}
    def save(self, shared):
        try:
            with open(shared.data_file, "w", encoding="utf-8") as f:
                json.dump(shared.data, f, indent=2, ensure_ascii=False)
            print(f"Data saved successfully.")
        except Exception as e:
            print(f"Error saving data: {e}")

class Adding:
    def __init__(self, save_and_load):
        self.save_and_load = save_and_load

    def adding_entry(self, shared):  
        today = str(datetime.date.today())
        data = shared.data

        print("Adding a new entry: ")
        print("Please enter the name of the entry.")
        entry_name = input("> ").strip()
        if not entry_name:
            print("Entry's name cannot be empty.")
            return

        print("The price: ")
        entry_price = input("> ").strip()
        if not entry_price:
            print("Price cannot be empty.")
            return

        print(f"""The date: 
            Use this format. YYYY/MM/DD
            Keep enter to set today's date. today: {today}""")
        while True:
            entry_date_string = input("> ").strip()
            checking_format = "%Y-%m-%d"

            if entry_date_string == "":
                entry_date_string = today
            
            try:
                parsed_date = datetime.datetime.strptime(entry_date_string, checking_format)
                entry_date = str(parsed_date.date())
                break
            except ValueError as err:
                print(f"Error: {err}")
                print("Please enter a valid date in this format: 1986-01-25")

        print("Tag(s): ")
        print("You can categorize your entries with tags. Below are some examples.")
        print("Examples: grocery, montly shopping, snacks for kids, investment, BIG SHOPPING, buying stuff, doctor, etc")
        print("Also, all your chosen tags until now:")
        tags = []
        for item in data.values():
            tag = item["Tag(s):"]
            if isinstance(tag, list):
                tags.extend(tag)
            else:
                    tags.append(tag)
        set_tags = list(set(tags))
        print(", ".join(set_tags))

        do = True
        taglist = []
        entry_tag = input("> ").strip().lower()
        taglist.append(entry_tag)

        while do == True:
            more_confirmation = input("Wanna add more tags? (yes or no) ")
            if more_confirmation.lower() in ["y", "yes", "are"]:
                do = True
                print("Adding another tag: ")
                entry_tag = input("> ").strip().lower()
                taglist.append(entry_tag)
            else:
                do = False

        data[entry_name] = {}
        data[entry_name]["Price:"] = entry_price
        data[entry_name]["Date:"] = entry_date
        data[entry_name]["Tag(s):"] = taglist
        self.save_and_load.save(shared)
        print(f"Entry '{entry_name}' added successfully.")
    
    def editing_entries(self, shared):
        data = shared.data

        if not data:
            print("No entries have been recorded yet.")
            return

        print("Editing: ")

        while True:
            print("All your entires until now:")
            table = PrettyTable()
            headers = ["No.", "Name", "Price", "Category", "Date"]
            expense_inventory = []
            total_price = 0
            numeric_prices = []
            found = False

            def format_tags(tags):
                if isinstance(tags, list):
                    return ", ".join(tags)
                return str(tags)

            sorted_items = sorted(data.items(), key=lambda x: datetime.datetime.strptime(x[1]["Date:"], "%Y-%m-%d"))

            for i, (name, details) in enumerate(sorted_items, start=1):
                price_num = int(details["Price:"])
                numeric_prices.append(price_num)

                price_display = f"{price_num:,}"
                tags = details["Tag(s):"]
                formatted_tags = format_tags(tags)
                date = details["Date:"]
                found = True

                expense_inventory.append([i, name, price_display, formatted_tags, date])

            table.title = "All your entries until now (sorted by date)"
            table.field_names = headers
            table.add_rows(expense_inventory)
            total_price = sum(numeric_prices)
            table.add_row(["-----", "-----", "-----", "-----", "-----"])
            table.add_row(["", "TOTAL", f"{total_price:,}", "", ""])
            table.align = "l"
            print()
            print(str(table))
            if not found:
                print("No entires yet.")    
            print()

            print(" Enter the entry's number you want to edit: / (You can type 'quit' to back to main menu.)")
            choice = input("> ").strip()

            if choice.isdigit():
                entry_number = int(choice)
                if 1 <= entry_number <= len(expense_inventory):
                    entry_name = expense_inventory[entry_number - 1]
                else:
                    print("Number is out of range.")
            if choice in ["quit", "q"]:
                print("Back to main menu.")
                break
            else:
                print("Please enter a number.")

            entry_info = data[entry_name[1]]
            name = entry_name[1]
            
            while True:
                print(f"Editing: {name}")
                print(f"Price: {entry_info["Price:"]}")
                print(f"Category: {format_tags(entry_info["Tag(s):"])}")
                print(f"Date added: {entry_info["Date:"]}")
                print()
                print("(While editing you can press Enter to keep the current info.)")
            
                print("Choose what do you want to change.")
                print("1. Name.   2. Price   3. Tag(s)   4. Date   5. Done with editing this")
                user_choice = input("> ").strip()

                if user_choice == "1":
                    new_name = input("New name: ").strip()
                    if new_name != name:
                        if new_name in data:
                            print(f"Entry '{new_name}' already exists.")
                            continue
                        else:
                            entry_data = data[name]
                            data.pop(name)
                            data[new_name] = entry_data
                            name = new_name
                            self.save_and_load.save(shared)
                            print("name edited.")
                            print()
                            continue
                        
                elif user_choice == "2":
                    new_price = input(f"New Price: ").strip()
                    if new_price:
                        entry_info["Price:"] = new_price
                        self.save_and_load.save(shared)
                        print("price edited.")
                        print()
                        continue
                    
                elif user_choice == "3":
                    print("Recent used tags:")
                    tags = []
                    for item in data.values():
                        tag = item["Tag(s):"]
                        if isinstance(tag, list):
                            tags.extend(tag)
                        else:
                            tags.append(tag)
                    set_tags = list(set(tags))
                    print(", ".join(set_tags))
                    print()
                    new_tag = input("New tag: ").strip().lower()
                    do = True
                    taglist = []
                    taglist.append(new_tag)

                    while do == True:
                        more_confirmation = input("Wanna add more tags? (yes or no) ")
                        if more_confirmation.lower() in ["y", "yes", "are"]:
                            do = True
                            print("Adding another tag: ")
                            new_tag = input("> ").strip().lower()
                            taglist.append(new_tag)
                        else:
                            do = False
                    
                    if taglist != entry_info["Tag(s):"]:
                        if taglist == entry_info["Tag(s):"]:
                            print(f"Already exists.")
                            continue
                        else:
                            entry_info["Tag(s):"] = taglist
                            self.save_and_load.save(shared)
                            print("tags edited successfully.")
                            print()
                            continue

                elif user_choice == "4":
                    while True:
                        new_date_str = input("New date: (Keep enter to set the date to today) ").strip()
                        checking_format = "%Y-%m-%d"

                        if new_date_str == "":
                            new_date_str = str(datetime.date.today())
                        
                        try:
                            parsed_date = datetime.datetime.strptime(new_date_str, checking_format)
                            new_date = str(parsed_date.date())
                            break
                        except ValueError as err:
                            print(f"Error: {err}")
                            print("Please enter a valid date in this format: 2020-09-11")
                    
                    if new_date != entry_info["Date:"]:
                        entry_info["Date:"] = new_date
                        self.save_and_load.save(shared)
                        print("date edited successfully.")
                        print()
                        continue
                    else:
                        print("Already it is.")
                        continue

                elif user_choice == "5":
                    break

                else:
                    print("Invalid choice. Please enter 1-5.")
                    continue

class Show:
    def __init__(self, save_and_load):
        self.save_and_load = save_and_load

    def show(self, shared):
        if not shared.data:
            print("No entries yet. Create some and check back again.")
            return

    def menu(self, shared):
        while True:
            print()
            print()
            print("Choose how to view the expenses.")
            print("1. Show recorded expenses for today")
            print("2. Show recorded expenses for current month.")
            print("3. All the expenses until now")
            print("4. Show for selected day")
            print("5. Show for selected time span")
            print("6. Show for filtered tags")
            print("7. Back to main menu")

            choice = input("> ").strip()
            
            if choice == "1":
                self.show_today(shared)
            elif choice == "2": 
                self.show_current_month(shared)
            elif choice == "3": 
                self.show_all(shared)
            elif choice == "4": 
                self.show_selected_day(shared)
            elif choice == "5":
                self.show_filtered_time(shared)
            elif choice == "6":
                self.show_filtered_tags(shared)
            elif choice == "7": 
                return
            else:
                print("Invalid choice. Try again.")

    def show_all(self, shared):
        data = shared.data
        table = PrettyTable()
        headers = ["Name", "Price", "Category", "Date"]
        expense_inventory = []
        total_price = 0
        numeric_prices = []
        found = False

        def format_tags(tags):
            if isinstance(tags, list):
                return ", ".join(tags)
            return str(tags)

        for entry in data:
            name = entry
            price_num = int(data[entry]["Price:"])
            numeric_prices.append(price_num)

            price_display = f"{price_num:,}"
            tags = data[entry]["Tag(s):"]
            formatted_tags = format_tags(tags)
            date = data[entry]["Date:"]
            found = True

            expense_inventory.append([name, price_display, formatted_tags, date])

        expense_inventory.sort(key=lambda x: int(x[1].replace(",", "")), reverse=True)

        table.title = "All your expenses until now"
        table.field_names = headers
        table.add_rows(expense_inventory)
        total_price = sum(numeric_prices)
        table.add_row(["-----", "-----", "-----", "-----"])
        table.add_row(["TOTAL", f"{total_price:,}", "", ""])
        table.align = "l"
        print()
        print(str(table))
        if not found:
            print("No entires yet.")    
        print()
    
    def show_today(self, shared):
        data = shared.data
        today_date = str(datetime.date.today())
        table = PrettyTable()
        headers = ["Name", "Price", "Category"]
        expense_inventory = []
        total_price = 0
        numeric_prices = []
        found = False

        def format_tags(tags):
            if isinstance(tags, list):
                return ", ".join(tags)
            return str(tags)

        for entry in data:
            if data[entry]["Date:"] == today_date:
                name = entry
                price_num = int(data[entry]["Price:"])
                numeric_prices.append(price_num)

                price_display = f"{price_num:,}"
                tags = data[entry]["Tag(s):"]
                formatted_tags = format_tags(tags)
                found = True

                expense_inventory.append([name, price_display, formatted_tags])

        expense_inventory.sort(key=lambda x: int(x[1].replace(",", "")), reverse=True)

        table.title = f"All your expenses for today - {today_date}"
        table.field_names = headers
        table.add_rows(expense_inventory)
        total_price = sum(numeric_prices)
        table.add_row(["-----", "-----", "-----"])
        table.add_row(["TOTAL", f"{total_price:,}", ""])
        table.align = "l"
        print()
        print(str(table))
        if not found:
            print("No entires yet.")
        print()

    def show_current_month(self, shared):
        data = shared.data
        current_month = str(datetime.date.today().month)
        if current_month == "1":
            current_month = "01"
        elif current_month == "2":
            current_month = "02"
        elif current_month == "3":
            current_month = "03"
        elif current_month == "4":
            current_month = "04"
        elif current_month == "5":
            current_month = "05"
        elif current_month == "6":
            current_month = "06"
        elif current_month == "7":
            current_month = "07"
        elif current_month == "8":
            current_month = "08"
        elif current_month == "9":
            current_month = "09"

        current_year = str(datetime.date.today().year)
        pattern = f"{current_year}-{current_month}"

        str_current_month = ""
        if current_month == "01":
            str_current_month = "Jan"
        elif current_month == "02":
            str_current_month = "Feb"
        elif current_month == "03":
            str_current_month = "Mar"
        elif current_month == "04":
            str_current_month = "Apr"
        elif current_month == "05":
            str_current_month = "May"
        elif current_month == "06":
            str_current_month = "Jun"
        elif current_month == "07":
            str_current_month = "Jul"
        elif current_month == "08":
            str_current_month = "Aug"
        elif current_month == "09":
            str_current_month = "Sep"
        elif current_month == "10":
            str_current_month = "Oct"
        elif current_month == "11":
            str_current_month = "Nov"
        elif current_month == "12":
            str_current_month = "Dec"

        table = PrettyTable()
        headers = ["Name", "Price", "Category", "Date"]
        expense_inventory = []
        total_price = 0
        numeric_prices = []
        found = False

        def format_tags(tags):
            if isinstance(tags, list):
                return ", ".join(tags)
            return str(tags)

        if pattern in str(data):
            for entry in data:
                if pattern in data[entry]["Date:"]:
                    name = entry
                    price_num = int(data[entry]["Price:"])
                    numeric_prices.append(price_num)

                    price_display = f"{price_num:,}"
                    tags = data[entry]["Tag(s):"]
                    formatted_tags = format_tags(tags)
                    date = data[entry]["Date:"]
                    found = True

                    expense_inventory.append([name, price_display, formatted_tags, date])

        expense_inventory.sort(key=lambda x: int(x[1].replace(",", "")), reverse=True)

        table.title = f"Expenses for {current_year}, {str_current_month}"
        table.field_names = headers
        table.add_rows(expense_inventory)
        total_price = sum(numeric_prices)
        table.add_row(["-----", "-----", "-----", "-----"])
        table.add_row(["TOTAL", f"{total_price:,}", "", ""])
        table.align = "l"
        print()
        print(str(table))
        if not found:
            print("No entires yet.")
        print()
        
    def show_selected_day(self, shared):
        data = shared.data

        print("All the dates that have entries until now:")
        all_dates = []
        for entry in data:
            all_dates.append(data[entry]["Date:"])
        sorted_dates = sorted(set(all_dates), key=lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))
        if not sorted_dates:
            print("There are no entries for now.")
            print("Backing to menu.")
            return
        else:
            print(", ".join(sorted_dates))

        print("Enter a date you want to see its entires. (keep in mind to use format YYYY-MM-DD)")
        while True:
            wanted_date_string = input("> ").strip()
            checking_format = "%Y-%m-%d"

            try:
                parsed_date = datetime.datetime.strptime(wanted_date_string, checking_format)
                wanted_date = str(parsed_date.date())
                break
            except ValueError as err:
                print(f"Error: {err}")
                print("Please enter a valid date in this format: 2001-12-10")
                
        table = PrettyTable()
        headers = ["Name", "Price", "Category"]
        expense_inventory = []
        total_price = 0
        numeric_prices = []
        found = False

        def format_tags(tags):
            if isinstance(tags, list):
                return ", ".join(tags)
            return str(tags)

        if wanted_date in str(data):
            for entry in data:
                if data[entry]["Date:"] == wanted_date:
                    name = entry
                    price_num = int(data[entry]["Price:"])
                    numeric_prices.append(price_num)

                    price_display = f"{price_num:,}"
                    tags = data[entry]["Tag(s):"]
                    formatted_tags = format_tags(tags)
                    found = True

                    expense_inventory.append([name, price_display, formatted_tags])

        expense_inventory.sort(key=lambda x: int(x[1].replace(",", "")), reverse=True)

        table.title = f"Entries for {wanted_date}"
        table.field_names = headers
        table.add_rows(expense_inventory)
        total_price = sum(numeric_prices)
        table.add_row(["-----", "-----", "-----"])
        table.add_row(["TOTAL", f"{total_price:,}", ""])
        table.align = "l"
        print()
        print(str(table))
        if not found:
            print("No entires yet.")
        print()

    def show_filtered_time(self, shared):
        data = shared.data

        if not data:
            print("No entries yet.")
            return
        
        while True:
            print("Don't forget the format: YYYY-MM-DD")
            print("Setting the start date: ")
            start_date_string = input("> ").strip()
            checking_format = "%Y-%m-%d"

            try:
                parsed_date_start = datetime.datetime.strptime(start_date_string, checking_format)
                start_date = str(parsed_date_start.date())
                break
            except ValueError as err:
                print(f"Error: {err}")
                print("Please enter a valid date in this format: 2015-04-21")

        while True:
            print("Setting the end date: ")
            end_date_string = input("> ").strip()
            checking_format = "%Y-%m-%d"
            try:
                parsed_date_end = datetime.datetime.strptime(end_date_string, checking_format)
                end_date = str(parsed_date_end.date())
                break
            except ValueError as err:
                print(f"Error: {err}")
                print("Please enter a valid date in this format: 2017-12-29")
        
        def date_range(data, start_date_str, end_date_str):
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")

            filtered_data = {}

            for key, value in data.items():
                item_date = datetime.datetime.strptime(value["Date:"], "%Y-%m-%d")

                if start_date <= item_date <= end_date:
                    filtered_data[key] = value
            
            return filtered_data

        def print_filtered_data(filtered_data):
            found = True

            if not filtered_data:
                print("No data found in the specified date range.")
                found = False
                return
            
            table = PrettyTable()
            headers = ["Name", "Price", "Category", "Date:"]
            expense_inventory = []
            total_price = 0
            numeric_prices = []

            def format_tags(tags):
                if isinstance(tags, list):
                    return ", ".join(tags)
                return str(tags)
            
            if found == True:
                for entry in filtered_data:
                    name = entry
                    price_num = int(filtered_data[entry]["Price:"])
                    numeric_prices.append(price_num)
                    price_display = f"{price_num:,}"
                    tags = filtered_data[entry]["Tag(s):"]
                    date = filtered_data[entry]["Date:"]
                    formatted_tags = format_tags(tags)

                    expense_inventory.append([name, price_display, formatted_tags, date])
                
            expense_inventory.sort(key=lambda x: int(x[1].replace(",", "")), reverse=True)

            table.title = f"Entries from {start_date} through {end_date}"
            table.field_names = headers
            table.add_rows(expense_inventory)
            total_price = sum(numeric_prices)
            table.add_row(["-----", "-----", "-----", "-----"])
            table.add_row(["TOTAL", f"{total_price:,}", "", ""])
            table.align = "l"
            print()
            print(str(table))
            if not found:
                print("No data found in the specified date range.")
            print()

        filtered = date_range(data, start_date, end_date)
        print_filtered_data(filtered)

    def show_filtered_tags(self, shared):
        data = shared.data

        if not data:
            print("No entries yet.")
            return

        print("All your chosen tags until now: ")
        tags = []
        for item in data.values():
            tag = item["Tag(s):"]
            if isinstance(tag, list):
                tags.extend(tag)
            else:
                    tags.append(tag)
        set_tags = list(set(tags))
        print(", ".join(set_tags))

        do = True
        tag = input("> ").strip().lower()
        tags_chosen = []
        tags_chosen.append(tag)

        while do == True:
            more_confirmation = input("Wanna add more tags? (yes or no) ")
            if more_confirmation.lower() in ["y", "yes", "are"]:
                do = True
                print("Adding another tag: ")
                tag = input("> ").strip().lower()
                tags_chosen.append(tag)
            else:
                do = False

        def tag_found(data, tags_chosen):
            filtered_data = {}
            for key, value in data.items():
                if value["Tag(s):"] in tags_chosen:
                    filtered_data[key] = value
            return filtered_data

        def print_filtered_data(filtered_data):
            found = True

            if not filtered_data:
                print("No data found in the specified tags chosen")
                found = False
                return
            
            table = PrettyTable()
            headers = ["Name", "Price", "Category", "Date:"]
            expense_inventory = []
            total_price = 0
            numeric_prices = []

            def format_tags(tags):
                if isinstance(tags, list):
                    return ", ".join(tags)
                return str(tags)
            
            if found == True:
                for entry in filtered_data:
                    name = entry
                    price_num = int(filtered_data[entry]["Price:"])
                    numeric_prices.append(price_num)
                    price_display = f"{price_num:,}"
                    tags = filtered_data[entry]["Tag(s):"]
                    date = filtered_data[entry]["Date:"]
                    formatted_tags = format_tags(tags)

                    expense_inventory.append([name, price_display, formatted_tags, date])
            
            expense_inventory.sort(key=lambda x: int(x[1].replace(",", "")), reverse=True)

            table.title = f"Entries pertaining to category(s): {", ".join(tags_chosen)}"
            table.field_names = headers
            table.add_rows(expense_inventory)
            total_price = sum(numeric_prices)
            table.add_row(["-----", "-----", "-----", "-----"])
            table.add_row(["TOTALs", f"{total_price:,}", "", ""])
            table.align = "l"
            print()
            print(str(table))
            if not found:
                print("No data found in the specified date range.")

        filtered = tag_found(data, tags_chosen)
        print_filtered_data(filtered)
        print()

class Main():
    def __init__(self):
        self.shared = State()
        self.save_and_load = Save_and_Load()
        self.adding_entry = Adding(self.save_and_load)
        self.show = Show(self.save_and_load)
        self.edit = Adding(self.save_and_load)

        self.save_and_load.load(self.shared)

    def performing_the_program(self):
        print("Welcome to Mom's Expense Recorder App")

        while True:
            print("Menu:")
            print("1. Add new entry")
            print("2. Show records")
            print("3. Edit an entry")
            print("4. Quit")

            print("Enter a number.")
            user_choice = str(input("> ").strip())

            if user_choice:
                if user_choice == "1":
                    self.adding_entry.adding_entry(self.shared)
                elif user_choice == "2":
                    self.show.menu(self.shared)
                elif user_choice == "3":
                    self.edit.editing_entries(self.shared)
                elif user_choice == "4":
                    print("Are you sure you want to quit the program? (YES/NO)")
                    confirm = input("> ").lower()
                    if confirm in ["yes", "y", "Y", "YES", "yeah", "Yes"]:
                        print("OK. Closing program :>")
                        break
                    else:
                        print()
                else:
                    print("Invalid choice. Please try again.")

if __name__ == "__main__":
    app = Main()
    app.performing_the_program()
