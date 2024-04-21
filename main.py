from tkinter import ttk, messagebox
import tkinter as tk
import sqlite3
import random
import string
import os

# Database initialization
db_path = 'data/database.sqlite'
if not os.path.exists(db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

conn = sqlite3.connect(db_path)


def initialize_database():
    '''
    This function creates a table in the database if it does not exist

    Returns:
    str: Ok
    '''

    # create table inside executescript function
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS vehicle_data (
            vehicle_No INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_type CHAR(50) NOT NULL,
            vehicle_model CHAR(50),
            License_plate CHAR(10) NOT NULL,
            code_permit CHAR(8) NOT NULL,
            checked_in DATETIME,
            checked_out DATETIME,
            member BOOLEAN,
            FOREIGN KEY (member) REFERENCES members(paid)
        );
        
        CREATE TABLE IF NOT EXISTS members (
            member_No INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            member_name CHAR(50) NOT NULL,
            member_vehicle_model INTEGER NOT NULL,
            member_vehicle_type CHAR(50) NOT NULL,
            member_license_plate CHAR(10) NOT NULL,         
            paid BOOLEAN,
            FOREIGN KEY (member_license_plate) REFERENCES vehicle_data(license_plate)
        );        
        
        
        ''')
    conn.commit()
    
# Create Tkinter window
root = tk.Tk()
root.title("Vehicle Management System")
root.geometry("600x300")

# Create a notebook (tabbed interface)
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)



# Functions for database operations


# Function to generate a random code
def generate_random_code(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Function to perform check-in operation
def check_in(vehicle_type, vehicle_model, license_plate):
    try:
        code_permit = generate_random_code()  # Generate a random code
        command = f'''
        INSERT INTO vehicle_data (code_permit, vehicle_type, vehicle_model, license_plate, checked_in)
        VALUES ('{code_permit}', '{vehicle_type}', {vehicle_model}, '{license_plate}', DATETIME('now'))
        '''
        conn.execute(command)
        conn.commit()
        return "Check In Sucessfully!"
    except sqlite3.Error as e:
        return f"Error inserting data: {e}"
###

###


# Function to perform check-out operation
def check_out(code_permit):
    try:
        command = f'''
        UPDATE vehicle_data
        SET checked_out = DATETIME('now')
        WHERE code_permit = '{code_permit}'
        '''
        conn.execute(command)
        conn.commit()
        return "Check Out Sucessfully!"
    except sqlite3.Error as e:
        return f"Error updating data: {e}"

# Function to perform search operation
def search(license_plate=''):
    if license_plate != '':
        command = f"SELECT * FROM vehicle_data WHERE license_plate = '{license_plate}'"
        result = conn.execute(command)
        return result.fetchone()
    else:
        # command = f"SELECT * FROM vehicle_data"
        # result = conn.execute(command)
        return "Not Found"


# Function to perform subscription operation
def subscription(member_name, member_license_plate, member_vehicle_model, member_vehicle_type, paid):
    try:
        command = f'''
        INSERT INTO members (member_name, member_license_plate, member_vehicle_model, member_vehicle_type, paid)
        VALUES ('{member_name}', '{member_license_plate}', {member_vehicle_model}, '{member_vehicle_type}', {paid})
        '''
        conn.execute(command)
        conn.commit()
        
        # Update the vehicle_data table to set member field to 1 for the corresponding license_id
        command_update_vehicle = f'''
        UPDATE vehicle_data
        SET member = 1
        WHERE license_id = '{member_license_plate}'
        '''
        conn.execute(command_update_vehicle)
        conn.commit()
        
        return "Subscribe Sucessfully!"
    except sqlite3.Error as e:
        return f"Error inserting data: {e}"


### GUI ####



# Create frames for each page
check_in_frame = ttk.Frame(notebook)
check_out_frame = ttk.Frame(notebook)
search_frame = ttk.Frame(notebook)
subscribe_frame = ttk.Frame(notebook)


# Add frames to the notebook with corresponding titles
notebook.add(check_in_frame, text="Check-in Vehicle")
notebook.add(check_out_frame, text="Check-out Vehicle")
notebook.add(search_frame, text="Search Vehicle")
notebook.add(subscribe_frame, text="Subscribe Member")




# Function for check-in page
def check_in_vehicle():
    # Get the selected vehicle type from the dropdown
    vehicle_type = vehicle_type_combobox.get()
    vehicle_model = vehicle_model_entry.get()
    license_plate = license_plate_entry.get()
    result = check_in(vehicle_type, vehicle_model, license_plate)
    messagebox.showinfo("Check-in Status", result)

# Create a dropdown for selecting vehicle type
vehicle_type_label = ttk.Label(check_in_frame, text="Vehicle Type:")
vehicle_type_label.grid(row=0, column=0, padx=5, pady=5)
vehicle_type_combobox = ttk.Combobox(check_in_frame, values=["Car", "Motorbike", "Bicycle"])
vehicle_type_combobox.grid(row=0, column=1, padx=5, pady=5)
vehicle_type_combobox.set("Car")  # Set default value to Car

# Other existing GUI elements for check-in page
vehicle_model_label = ttk.Label(check_in_frame, text="Vehicle Model:")
vehicle_model_label.grid(row=1, column=0, padx=5, pady=5)
vehicle_model_entry = ttk.Entry(check_in_frame)
vehicle_model_entry.grid(row=1, column=1, padx=5, pady=5)

license_plate_label = ttk.Label(check_in_frame, text="License plate:")
license_plate_label.grid(row=2, column=0, padx=5, pady=5)
license_plate_entry = ttk.Entry(check_in_frame)
license_plate_entry.grid(row=2, column=1, padx=5, pady=5)

check_in_button = ttk.Button(check_in_frame, text="Check-in", command=check_in_vehicle)
check_in_button.grid(row=3, columnspan=2, padx=5, pady=5)

# Function for check-out page
def check_out_vehicle():
    code_permit = code_permit_entry.get()
    result = check_out(code_permit)
    messagebox.showinfo("Check-out Status", result)

code_permit_label = ttk.Label(check_out_frame, text="Code Permit:")
code_permit_label.grid(row=0, column=0, padx=5, pady=5)
code_permit_entry = ttk.Entry(check_out_frame)
code_permit_entry.grid(row=0, column=1, padx=5, pady=5)

check_out_button = ttk.Button(check_out_frame, text="Check-out", command=check_out_vehicle)
check_out_button.grid(row=1, columnspan=2, padx=5, pady=5)



# Function for search page
def search_vehicle():
    license_plate = license_plate_search_entry.get()
    result = search(license_plate)
    
    # Create a new window for displaying the search result in a table
    search_result_window = tk.Toplevel(root)
    search_result_window.title("Search Result")
    
    if result == "Not Found":
        # Retrieve all data from the database
        command = "SELECT * FROM vehicle_data"
        all_data = conn.execute(command).fetchall()
        
        # Create a Treeview widget to display all data in a table format
        tree = ttk.Treeview(search_result_window, show="headings")
        tree["columns"] = ("Vehicle No.", "Vehicle Type", "Vehicle Model", "License Plate", "Code_Permit", "Checked In", "Checked Out", "Member")
        tree.heading("Vehicle No.", text="Vehicle No.")
        tree.heading("Vehicle Type", text="Vehicle Type")
        tree.heading("Vehicle Model", text="Vehicle Model")
        tree.heading("License Plate", text="License Plate")
        tree.heading("Code_Permit", text="Code_Permit")
        tree.heading("Checked In", text="Checked In")
        tree.heading("Checked Out", text="Checked Out")
        tree.heading("Member", text="Member")

        # Insert all data into the table
        for row in all_data:
            tree.insert("", "end", values=row[:])  # Skip the first element (index column)
        tree.pack(expand=True, fill="both")
    else:
        # Create a Treeview widget to display the search result in a table format
        tree = ttk.Treeview(search_result_window, show="headings")
        tree["columns"] = ("Vehicle No.", "Vehicle Type", "Vehicle Model", "License Plate", "Code_Permit", "Checked In", "Checked Out", "Member")
        tree.heading("Vehicle No.", text="Vehicle No.")
        tree.heading("Vehicle Type", text="Vehicle Type")
        tree.heading("Vehicle Model", text="Vehicle Model")
        tree.heading("License Plate", text="License Plate")
        tree.heading("Code_Permit", text="Code_Permit")
        tree.heading("Checked In", text="Checked In")
        tree.heading("Checked Out", text="Checked Out")
        tree.heading("Member", text="Member")

        # Insert the search result into the table
        tree.insert("", "end", values=result)
        tree.pack(expand=True, fill="both")
        
# Button    
license_plate_search_label = ttk.Label(search_frame, text="License Plate:")
license_plate_search_label.grid(row=0, column=0, padx=5, pady=5)
license_plate_search_entry = ttk.Entry(search_frame)
license_plate_search_entry.grid(row=0, column=1, padx=5, pady=5)

search_button = ttk.Button(search_frame, text="Search", command=search_vehicle)
search_button.grid(row=1, columnspan=2, padx=5, pady=5)


# Function for subscription page
def subscribe_member():

    member_name = member_name_entry.get()
    member_license_plate = member_license_plate_entry.get()
    member_model = member_model_entry.get()
    member_vehicle_type = member_vehicle_type_combobox.get()  # Get selected vehicle type
    paid = paid_combobox.get()  # Get selected paid status
    result = subscription(member_name, member_license_plate, member_model, member_vehicle_type, paid)
    messagebox.showinfo("Subscription Status", result)

member_name_label = ttk.Label(subscribe_frame, text="Member Name:")
member_name_label.grid(row=0, column=0, padx=5, pady=5)
member_name_entry = ttk.Entry(subscribe_frame)
member_name_entry.grid(row=0, column=1, padx=5, pady=5)

member_license_plate_label = ttk.Label(subscribe_frame, text="Member License Plate:")
member_license_plate_label.grid(row=1, column=0, padx=5, pady=5)
member_license_plate_entry = ttk.Entry(subscribe_frame)
member_license_plate_entry.grid(row=1, column=1, padx=5, pady=5)

member_model_label = ttk.Label(subscribe_frame, text="Member Model:")
member_model_label.grid(row=2, column=0, padx=5, pady=5)
member_model_entry = ttk.Entry(subscribe_frame)
member_model_entry.grid(row=2, column=1, padx=5, pady=5)

member_vehicle_type_label = ttk.Label(subscribe_frame, text="Member Vehicle Type:")
member_vehicle_type_label.grid(row=3, column=0, padx=5, pady=5)
member_vehicle_type_combobox = ttk.Combobox(subscribe_frame, values=["Car", "Motorbike", "Bicycle"])
member_vehicle_type_combobox.grid(row=3, column=1, padx=5, pady=5)
member_vehicle_type_combobox.set("Car")  # Set default value to Car

paid_label = ttk.Label(subscribe_frame, text="Paid (True/False):")
paid_label.grid(row=4, column=0, padx=5, pady=5)
paid_combobox = ttk.Combobox(subscribe_frame, values=["True", "False"])
paid_combobox.grid(row=4, column=1, padx=5, pady=5)
paid_combobox.set("True")  # Set default value to True

subscribe_button = ttk.Button(subscribe_frame, text="Subscribe", command=subscribe_member)
subscribe_button.grid(row=5, columnspan=2, padx=5, pady=5)



# Run Tkinter main loop

if __name__ == '__main__':
    initialize_database()
    root.mainloop()
    print(f'data initialization: Ok')