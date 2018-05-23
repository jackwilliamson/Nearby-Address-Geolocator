from Tkinter import *
import tkFont
from Database import update_all_database_addresses, get_addresses_within_location, get_all_database_address, \
    remove_address_from_database
from Database import add_address_to_database
from Address import Address


class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Nearby Address Application")
        master.minsize(width=666, height=450)
        master.resizable(width=False, height=False)
        master.rowconfigure(0, weight=1)
        master.columnconfigure(0, weight=1)

        self.main_screen = Frame(master)
        self.add_address_frame = Frame(master)
        self.find_nearby_frame = Frame(master)
        self.list_nearby_frame = Frame(master)
        self.delete_address_frame = Frame(master)

        self.create_main_frame()
        self.create_add_address_frame()
        self.create_find_nearby_frame()
        self.create_list_nearby_frame()
        self.create_delete_address_frame()

        self.show_main_frame()

    def create_main_frame(self):
        main_screen = self.main_screen

        main_screen.configure(background='blue')

        times16 = tkFont.Font(family='Times', size=16)

        label = Label(main_screen, text="Nearby Address Application", font=times16)

        add_address_button = Button(main_screen, text="Add Address to Database",
                                         command=self.show_add_address_frame, font=times16)

        find_nearby_button = Button(main_screen, text="Find Nearby Addresses from Location",
                                         command=self.show_find_nearby_frame, font=times16)

        reload_db_button = Button(main_screen, text="Reload Database Geolocations",
                                       command=self.update_database, font=times16)

        delete_addr_db_button = Button(main_screen, text="Delete Address from Database",
                                            command=self.show_delete_address_frame, font=times16)

        close_button = Button(main_screen, text="Close", command=self.master.quit)

        main_screen.rowconfigure((0, 4), weight=1)
        main_screen.columnconfigure((0, 1), weight=1)

        label.grid(row=0, column=0, columnspan=2)
        add_address_button.grid(row=1, column=0, sticky='EWNS', ipady=50, padx=5, pady=5)
        find_nearby_button.grid(row=1, column=1, sticky='EWNS', ipady=50, padx=5, pady=5)
        reload_db_button.grid(row=2, column=0, columnspan=1, sticky='EWNS', ipady=50, padx=5, pady=5)
        delete_addr_db_button.grid(row=2, column=1, columnspan=1, sticky='EWNS', ipady=50, padx=5, pady=5)
        close_button.grid(row=3, column=0, columnspan=2, sticky='NS')

    def show_main_frame(self):
        self.main_screen.grid(row=0, column=0, sticky='EWNS')
        self.main_screen.tkraise()

    def create_add_address_frame(self):
        add_address_frame = self.add_address_frame
        explanation = """Input address you want to add to the database in this format:
                Street Address, City, Province Code
                ex. 200 Yorkland Blvd, Toronto, ON"""
        times16 = tkFont.Font(family='Times', size=16)
        label = Label(add_address_frame, text=explanation, font=times16)
        self.address_entry = Entry(add_address_frame)
        confirm_button = Button(add_address_frame, text="Enter", font=times16, command=self.check_add_address)
        cancel_button = Button(add_address_frame, text="Go Back", command=self.show_main_frame)

        add_address_frame.rowconfigure((0, 2), weight=1)
        add_address_frame.columnconfigure((0, 1), weight=1)
        add_address_frame.configure(background='white')
        label.grid(row=0, column=0, columnspan=2, sticky='EWNS')
        self.address_entry.grid(row=1, column=0, columnspan=2, sticky='EWNS')
        confirm_button.grid(row=2, column=0, columnspan=1, sticky='EWNS')
        cancel_button.grid(row=2, column=1, columnspan=1, sticky='EWNS')

    def show_add_address_frame(self):
        self.address_entry.delete(0, END)
        self.add_address_frame.grid(row=0, column=0, sticky='EWNS')
        self.add_address_frame.tkraise()

    def check_add_address(self):
        added_address = self.address_entry.get()
        confirmation = "Are you sure you want to add " + added_address + " to the database?"
        toplevel = Toplevel()
        self.add_address_toplevel = toplevel
        toplevel.title("Confirm Add Address")
        times16 = tkFont.Font(family='Times', size=16)
        label = Label(toplevel, text=confirmation, font=times16)
        confirm_button = Button(toplevel, text="Confirm", font=times16, command=self.confirm_add_address)
        cancel_button = Button(toplevel, text="Cancel", command=self.add_address_toplevel.destroy)

        toplevel.rowconfigure((0, 1), weight=1)
        toplevel.columnconfigure((0, 1), weight=1)
        label.grid(row=0, column=0, columnspan=2, sticky='EWNS')
        confirm_button.grid(row=1, column=0, columnspan=1, sticky='EWNS')
        cancel_button.grid(row=1, column=1, columnspan=1, sticky='EWNS')

    def confirm_add_address(self):
        self.add_address()
        self.add_address_toplevel.destroy()
        self.show_main_frame()

    def add_address(self):
        added_address = self.address_entry.get()
        address = Address(added_address, 0, 0)
        address.get_google_geo_location()
        add_address_to_database(address)


    def create_find_nearby_frame(self):
        find_nearby_frame = self.find_nearby_frame
        explanation = """Input address and distance in kilometres to find nearby locations in the database using this format for addresses:
                        Street Address, City, Province Code
                        ex. 200 Yorkland Blvd, Toronto, ON"""
        times16 = tkFont.Font(family='Times', size=16)
        label = Label(find_nearby_frame, text=explanation, font=times16)
        address_label = Label(find_nearby_frame, text='Address:', font=times16)
        distance_label = Label(find_nearby_frame, text='Distance (km):', font=times16)
        self.find_nearby_address_entry = Entry(find_nearby_frame)
        self.find_nearby_distance_entry = Entry(find_nearby_frame)
        confirm_button = Button(find_nearby_frame, text="Enter", font=times16, command=self.find_nearby_addresses)
        cancel_button = Button(find_nearby_frame, text="Go Back", command=self.show_main_frame)

        find_nearby_frame.rowconfigure((0, 3), weight=1)
        find_nearby_frame.columnconfigure((0, 1), weight=1)
        find_nearby_frame.configure(background='white')
        label.grid(row=0, column=0, columnspan=2, sticky='EWNS')
        address_label.grid(row=1, column=0, columnspan=1, sticky='EWNS')
        self.find_nearby_address_entry.grid(row=1, column=1, columnspan=1, sticky='EWNS')
        distance_label.grid(row=2, column=0, columnspan=1, sticky='EWNS')
        self.find_nearby_distance_entry.grid(row=2, column=1, columnspan=1, sticky='EWNS')
        confirm_button.grid(row=3, column=0, columnspan=1)
        cancel_button.grid(row=3, column=1, columnspan=1)

    def show_find_nearby_frame(self):
        self.find_nearby_address_entry.delete(0, END)
        self.find_nearby_distance_entry.delete(0, END)
        self.find_nearby_frame.grid(row=0, column=0, sticky='EWNS')
        self.find_nearby_frame.tkraise()

    def find_nearby_addresses(self):
        dist = self.find_nearby_distance_entry.get()
        addr = self.find_nearby_address_entry.get()
        acceptable_addr = get_addresses_within_location(addr, dist)
        self.list_label_var.set('Here are all nearby locations to ' + addr)
        self.list_nearby.delete(0, END)
        for address in acceptable_addr:
            list_item = address.streetAddress + "  - " + str(address.dist) + " km"
            self.list_nearby.insert(END, list_item)
        self.list_nearby_frame.grid(row=0, column=0, sticky='EWNS')
        self.list_nearby_frame.tkraise()

    def create_list_nearby_frame(self):
        list_nearby_frame = self.list_nearby_frame
        times16 = tkFont.Font(family='Times', size=16)
        self.list_label_var = StringVar()
        self.list_label_var.set('Here are all nearby locations to ')
        label = Label(list_nearby_frame, textvariable=self.list_label_var, font=times16)
        self.list_nearby = Listbox(list_nearby_frame)
        cancel_button = Button(list_nearby_frame, text="Go Back to Main Screen", command=self.show_main_frame)

        list_nearby_frame.rowconfigure((0, 2), weight=1)
        list_nearby_frame.columnconfigure((0, 0), weight=1)
        list_nearby_frame.configure(background='white')
        label.grid(row=0, column=0, columnspan=1, sticky='EWNS')
        self.list_nearby.grid(row=1, column=0, columnspan=1, sticky='EWNS')
        cancel_button.grid(row=2, column=0, columnspan=1)

    def create_delete_address_frame(self):
        delete_address_frame = self.delete_address_frame
        times16 = tkFont.Font(family='Times', size=16)
        label = Label(delete_address_frame, text="Select an address to delete from the database", font=times16)
        self.delete_list_addr = Listbox(delete_address_frame)
        delete_button = Button(delete_address_frame, text="Delete Selection", command=self.check_delete_address)
        cancel_button = Button(delete_address_frame, text="Go Back to Main Screen", command=self.show_main_frame)

        delete_address_frame.rowconfigure((0, 2), weight=1)
        delete_address_frame.columnconfigure((0, 1), weight=1)
        delete_address_frame.configure(background='white')
        label.grid(row=0, column=0, columnspan=2, sticky='EWNS')
        self.delete_list_addr.grid(row=1, column=0, columnspan=2, sticky='EWNS')
        delete_button.grid(row=2, column=0, columnspan=1)
        cancel_button.grid(row=2, column=1, columnspan=1)

    def show_delete_address_frame(self):
        self.delete_list_addr.delete(0, END)
        self.delete_addresses = get_all_database_address()
        for address in self.delete_addresses:
            list_item = address.streetAddress
            self.delete_list_addr.insert(END, list_item)
        self.delete_address_frame.grid(row=0, column=0, sticky='EWNS')
        self.delete_address_frame.tkraise()

    def check_delete_address(self):
        toplevel = Toplevel()
        self.deletetoplevel = toplevel
        toplevel.title("Delete Address from Database")
        index = map(int, self.delete_list_addr.curselection())[0]
        warning = "Are you sure you want to remove " + self.delete_addresses[index].streetAddress + " from the database?"
        times16 = tkFont.Font(family='Times', size=16)
        label = Label(toplevel, text=warning, font=times16)
        confirm_button = Button(toplevel, text="Confirm", font=times16, command=self.delete_selected_address)
        cancel_button = Button(toplevel, text="Cancel", command=self.deletetoplevel.destroy)

        toplevel.rowconfigure((0, 1), weight=1)
        toplevel.columnconfigure((0, 1), weight=1)
        label.grid(row=0, column=0, columnspan=2, sticky='EWNS')
        confirm_button.grid(row=1, column=0, columnspan=1, sticky='EWNS')
        cancel_button.grid(row=1, column=1, columnspan=1, sticky='EWNS')

    def delete_selected_address(self):
        index = map(int, self.delete_list_addr.curselection())[0]
        remove_address_from_database(self.delete_addresses[index].firebasekey)
        self.delete_list_addr.delete(0, END)
        self.delete_addresses = get_all_database_address()
        for address in self.delete_addresses:
            list_item = address.streetAddress
            self.delete_list_addr.insert(END, list_item)
        self.deletetoplevel.destroy()

    def update_database(self):
        toplevel = Toplevel()
        self.updatetoplevel = toplevel
        toplevel.title("Reload Database Geolocations")
        WARNING = """This searches Google for geolocations for all addresses in the database,
        this is a costly function, do not do unless completely necessary"""
        times16 = tkFont.Font(family='Times', size=16)
        label = Label(toplevel, text=WARNING, font=times16)
        confirm_button = Button(toplevel, text="Confirm", font=times16, command=self.confirm_update)
        cancel_button = Button(toplevel, text="Cancel", command=self.updatetoplevel.destroy)

        toplevel.rowconfigure((0, 1), weight=1)
        toplevel.columnconfigure((0, 1), weight=1)
        label.grid(row=0, column=0, columnspan=2, sticky='EWNS')
        confirm_button.grid(row=1, column=0, columnspan=1, sticky='EWNS')
        cancel_button.grid(row=1, column=1, columnspan=1, sticky='EWNS')

    def confirm_update(self):
        update_all_database_addresses()
        self.updatetoplevel.destroy()

