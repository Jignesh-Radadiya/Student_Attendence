from PIL import Image, ImageTk
import tkinter as tk
from datetime import datetime
from tkcalendar import DateEntry
import mysql.connector
from tkinter import *
from tkinter import ttk

window = tk.Tk()
window.iconbitmap('aaa.ico')
window.title("Attendance System")
window.geometry("512x512")

bg=PhotoImage(file='ccc.png')

labelll=Label(window,image=bg)
labelll.place(x=0,y=0)

# img4=open(r"C:\Users\devang\Desktop\jQuery\python\unnamed.png")
# img4=img4.resize((400,450),Image.ANTIALIAS)
# window.phtImg4=ImageTk.PhotoImage(img4)


# f_label=Label(window,image=window.phtImg4)
# f_label.place(x=0,y=0,width=400,height=450)


# Create a photoimage object of the image in the path
# image1 = Image.open(r"C:\Users\devang\Desktop\jQuery\python\unnamed.png")
# test = ImageTk.PhotoImage(image1)

# label1 = tk.Label(image=test)
# label1.image = test

# # Position image
# label1.place(x=0, y=0,width=400,height=450)

students = {'Devang': '01', 'Jignesh': '02',
            'Purvis': '03', 'Vishwaraj': '04', 
            'Parth': '05','Krish': '06','Yashraj': '07','Dip': '08','Divyesh': '09','Sahil': '10'}
present_students = []
subjects = ['OS', 'Python', 'Java', 'WP', 'NEN']
selected_subject = tk.StringVar()
selected_date = None

title_label = tk.Label(window, text="Attendance System", font=("Arial", 20,'bold'),bg='pink',fg='black')
title_label.pack()

dt_frame = tk.Frame(window)
dt_frame.pack(pady=10)

date_label = tk.Label(dt_frame, text="Date", font=("Arial", 12,'bold'),bg='pink',fg='black')
date_label.pack(side="left")

date_picker = DateEntry(
    dt_frame, width=12, background='green', foreground='white', borderwidth=2)
date_picker.pack(side="left")

subject_label = tk.Label(window, text="Select subject", font=("Arial", 12,'bold'),bg='pink',fg='black')
subject_label.pack(pady=10)

subject_frame = tk.Frame(window)
subject_frame.pack()

for subject in subjects:
    subject_checkbox = tk.Checkbutton(
        subject_frame, text=subject, variable=selected_subject, onvalue=subject, offvalue="", font=("Arial", 12,'bold'),bg='orange',fg='black')
    subject_checkbox.pack(side="left")

students_frame = tk.Frame(window)
students_frame.pack()

buttons_frame = tk.Frame(window)
buttons_frame.pack()

present_label = tk.Label(
    students_frame, text="Take Attendance", font=("Arial", 12,'bold'),bg='pink',fg='black')
present_label.pack()

present_listbox = tk.Listbox(students_frame, selectmode="multiple", height=5, font=("Calibri", 10,'bold'),bg='black',fg='yellow')
present_listbox.pack(side="left")

absent_listbox = tk.Listbox(students_frame, selectmode="multiple", height=5, font=("Calibri", 10,'bold'),bg='cyan',fg='black')
absent_listbox.pack(side="right")

for student in students:
    absent_listbox.insert(tk.END, f"{student} ({students[student]})")

present_button = tk.Button(
    buttons_frame, text="Mark Present", command=lambda: mark_present(),font=("Times New Roman", 12,'bold'),bg='green',fg='white')
present_button.pack(side="left")

# absent_button = tk.Button(
#     buttons_frame, text="Mark Absent", command=lambda: mark_absent())
# absent_button.pack(side="right")

submit_button = tk.Button(window, text="Submit", command=lambda: submit(),font=("Times New Roman", 12,'bold'),bg='blue',fg='white')
submit_button.pack(pady=10)

def mark_present():
    global present_students
    for student in absent_listbox.curselection():
        name = absent_listbox.get(student)
        present_listbox.insert(tk.END, name)
        absent_listbox.delete(student)
        present_students.append(name)

def mark_absent():
    global present_students
    for student in present_listbox.curselection():
        name = present_listbox.get(student)
        absent_listbox.insert(tk.END, name)
        present_listbox.delete(student)
        present_students.remove(name)

def submit():
    global selected_subject, selected_date, present_students
    subject = selected_subject.get()
    if not subject:
        tk.messagebox.showerror("Error", "Please select a subject")
        return
    selected_date = date_picker.get_date().strftime("%Y-%m-%d")
    filename = f"attendance_{subject}_{selected_date}.txt"

    with open(filename, "w") as f:
        for student in present_students:
            f.write(student + "\n")

    # Connect to the database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="py"
    )

    mycursor = mydb.cursor()

    # Create table if it doesn't exist
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS attendance (id INT AUTO_INCREMENT PRIMARY KEY, sname VARCHAR(255), subject VARCHAR(255), date DATE)")

# Insert data into the table
    subject = selected_subject.get()
    date = selected_date

    for student in present_students:
        sql = "INSERT INTO attendance (sname, subject, date) VALUES (%s, %s, %s)"
        val = (student.split(" ")[0], subject, date)
        mycursor.execute(sql, val)

# Commit changes to the database
    mydb.commit()

# Close database connection
    mydb.close()

window.mainloop()
