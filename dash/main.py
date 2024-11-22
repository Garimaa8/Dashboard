import tkinter as tk
from tkinter.ttk import *
from tkinter import ttk
from PIL import ImageTk, Image
import mysql.connector
from tkinter import messagebox
import random
import sys
import matplotlib.pyplot as plt
import numpy as np
import language_tool_python
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


tool = language_tool_python.LanguageTool('en-US')

root = tk.Tk()
root.title("ABC International school")
root.geometry("810x450")
root.geometry("+330+200")
# window.configure(bg="#BF3EFF")

im = Image.open("schl_logo.png")
im = im.resize((404, 445))
img = ImageTk.PhotoImage(im)
img1 = tk.Label(root, image=img)
img1.place(x=0, y=0)

label1 = tk.Label(root, text="STUDENT LOGIN", )
label1.config(font=("Courier", 42,"bold"))
label1.place(x=445, y=65)

name_label = tk.Label(root, text='Name', font=('calibre', 12, 'bold'))
name_entry = tk.Entry(root, font=('calibre', 12, 'normal'))
id_label = tk.Label(root, text='Student ID', font=('calibre', 12, 'bold'))
id_entry = tk.Entry(root, font=('calibre', 12, 'normal'), show='*')
name_label.grid(row=0, column=0)
name_label.place(x=520, y=170)
name_entry.grid(row=1, column=0)
name_entry.place(x=520, y=190)
id_label.grid(row=3, column=0)
id_label.place(x=520, y=250)
id_entry.grid(row=5, column=0)
id_entry.place(x=520, y=270)

# Function to handle main page
def main_pg():
    global get_n
    get_n = name_entry.get()
    get_n = get_n.title()
    get_id= id_entry.get()
    mydb = mysql.connector.connect(host='127.0.0.1', user='root', password='garimasql', database='student_in')
    cursor = mydb.cursor(buffered=True)
    cursor.execute("SELECT student_id FROM student WHERE name = %s", (get_n,))
    s = ""
    for i in cursor:
        i = str(i)
        s += i
    s = s[1:5]
    if s == get_id:
        root.destroy()

        def main_window():
            win = tk.Tk()
            win.geometry("1500x800")
            win.title("ABC International School")
            win.configure(bg="#B2DFEE")

            shadow = tk.Label(win, width=145, height=42, bg="#9AC0CD")
            shadow.place(x=55, y=45)
            scrn = tk.Label(win, width=145, height=42)
            scrn.place(relx=0.5, rely=0.5, anchor="center")

            # Logo
            logo_i = Image.open("schl_logo.png")
            logo_i = logo_i.resize((160, 100))
            logo_i1 = ImageTk.PhotoImage(logo_i)
            logo = tk.Label(win, width=170, height=140, image=logo_i1)
            logo.place(x=1176, y=60)

            # Random image
            mydb = mysql.connector.connect(host='127.0.0.1', user='root', password='garimasql', database='student_in')
            cursor = mydb.cursor(buffered=True)
            SQ = "SELECT Gender FROM student WHERE name = %s"
            cursor.execute(SQ, (get_n,))
            g=""
            for i in cursor:
                i=str(i)
                g+=i
            g=g[2:3]

            if g=='F':
                r=random.randint(1,5)
                im = Image.open(f"girl/{r}.png")
                im = im.resize((220, 160))
                img = ImageTk.PhotoImage(im)
                img_label = tk.Label(win, width=200, height=160, image=img)
                img_label.place(x=90, y=135)

            elif g=='M':
                r=random.randint(1,5)
                im = Image.open(f"boy/{r}.png")
                im = im.resize((220, 160))
                img = ImageTk.PhotoImage(im)
                img_label = tk.Label(win, width=200, height=160, image=img)
                img_label.place(x=90, y=135)

            # Database connection and query
            mydb = mysql.connector.connect(host='127.0.0.1', user='root', password='garimasql', database='student_in')
            cursor = mydb.cursor(buffered=True)

            try:
                SQ = "SELECT * FROM student WHERE name = %s"
                cursor.execute(SQ, (get_n,))
                student_data = cursor.fetchone()

                if student_data:
                    name_label = tk.Label(win, height=2,
                                          text=student_data[0])  # Assuming the name is in the second column
                    name_label.config(font=("Courier", 30, "bold"))
                    name_label.place(x=370, y=130)
                else:
                    messagebox.showinfo("Error", f"No record found for {get_n}")

            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", str(e))
            finally:
                cursor.close()
                mydb.close()

            mydb = mysql.connector.connect(host='127.0.0.1', user='root', password='garimasql', database='student_in')
            cursor = mydb.cursor(buffered=True)
            SQ = "SELECT class FROM student WHERE name = %s"
            cursor.execute(SQ, (get_n,))
            cls_label = tk.Label(win, height=2,
                                 text=f"Class: {student_data[1]}")  # Assuming class is in the third column
            cls_label.config(font=("Courier", 30, "bold"))
            cls_label.place(x=370, y=180)

            mydb = mysql.connector.connect(host='127.0.0.1', user='root', password='garimasql', database='student_in')
            cursor = mydb.cursor(buffered=True)
            SQ = "SELECT gender FROM student WHERE name = %s"
            cursor.execute(SQ, (get_n,))
            cls_label = tk.Label(win, height=2,
                                 text=f"Gender: {student_data[7]}")  # Assuming class is in the third column
            cls_label.config(font=("Courier", 30, "bold"))
            cls_label.place(x=370, y=230)

            mydb = mysql.connector.connect(host='127.0.0.1', user='root', password='garimasql', database='student_in')
            cursor = mydb.cursor(buffered=True)
            SQ = "SELECT contact_no FROM student WHERE name = %s"
            cursor.execute(SQ, (get_n,))
            cls_label = tk.Label(win, height=2,
                                 text=f"Contact no: {student_data[6]}")  # Assuming class is in the third column
            cls_label.config(font=("Courier", 30, "bold"))
            cls_label.place(x=370, y=280)

            mydb = mysql.connector.connect(host='127.0.0.1', user='root', password='garimasql', database='student_in')
            cursor = mydb.cursor(buffered=True)
            SQ = "SELECT mothers_name FROM student WHERE name = %s"
            cursor.execute(SQ, (get_n,))
            cls_label = tk.Label(win, height=2,
                                 text=f"Mother's name : {student_data[3]}")  # Assuming class is in the third column
            cls_label.config(font=("Courier", 30, "bold"))
            cls_label.place(x=370, y=330)

            mydb = mysql.connector.connect(host='127.0.0.1', user='root', password='garimasql', database='student_in')
            cursor = mydb.cursor(buffered=True)
            SQ = "SELECT fathers_name FROM student WHERE name = %s"
            cursor.execute(SQ, (get_n,))
            cls_label = tk.Label(win, height=2, text=f"Father's name : {student_data[4]}")
            cls_label.config(font=("Courier", 30, "bold"))
            cls_label.place(x=370, y=380)

            mydb = mysql.connector.connect(host='127.0.0.1', user='root', password='garimasql', database='student_in')
            cursor = mydb.cursor(buffered=True)
            SQ = "SELECT transport FROM student WHERE name = %s"
            cursor.execute(SQ, (get_n,))
            cls_label = tk.Label(win, height=2, text=f"Transport : {student_data[5]}")
            cls_label.config(font=("Courier", 30, "bold"))
            cls_label.place(x=370, y=430)

            mydb = mysql.connector.connect(host='127.0.0.1', user='root', password='garimasql', database='student_in')
            cursor = mydb.cursor(buffered=True)
            SQ = "SELECT student_id FROM student WHERE name = %s"
            cursor.execute(SQ, (get_n,))
            cls_label = tk.Label(win, height=2, text=f"Student ID : {student_data[2]}")
            cls_label.config(font=("Courier", 30, "bold"))
            cls_label.place(x=370, y=480)

            mrks = tk.Label(win, height=2, text="Marks : ")
            mrks.config(font=("Courier", 20, "bold"))
            mrks.place(x=1230, y=230)

            def maths():
                import matplotlib.pyplot as plt
                import numpy as np
                import mysql.connector

                # Connect to MySQL database
                mydb = mysql.connector.connect(
                    host='127.0.0.1',
                    user='root',
                    password='garimasql',
                    database='student_in'
                )

                cursor = mydb.cursor(buffered=True)

                # Fetch marks from the database
                l = []
                SQ = "SELECT maths FROM performance"
                cursor.execute(SQ)
                for i in cursor:
                    l.append(i[0])  # Flatten tuple to extract the value

                ypoints = np.array(l)  # Convert to NumPy array

                # Fetch student names
                l1 = []
                SQ = """
                    SELECT student.name 
                    FROM student 
                    INNER JOIN performance ON student.student_id = performance.student_id
                    """
                cursor.execute(SQ)
                for i in cursor:
                    l1.append(i[0])  # Flatten tuple to extract the name

                # Plotting
                plt.figure(figsize=(10, 6))
                plt.plot(ypoints, marker='o', label="Math Marks")  # Plot ypoints with markers

                # Add labels
                plt.ylabel("Marks")
                plt.xlabel("Students")
                plt.title("Math Performance of Students")

                # Set custom x-axis labels (student names)
                plt.xticks(ticks=range(len(l1)), labels=l1, rotation=45)

                # Add legend
                plt.legend()

                # Show plot
                plt.tight_layout()
                plt.show()

            math = tk.Radiobutton(win, text="Maths", command=maths)
            math.config(font=("Courier", 20))
            math.place(x=1225, y=280)

            def english():
                import matplotlib.pyplot as plt
                import numpy as np
                import mysql.connector

                # Connect to MySQL database
                mydb = mysql.connector.connect(
                    host='127.0.0.1',
                    user='root',
                    password='garimasql',
                    database='student_in'
                )

                cursor = mydb.cursor(buffered=True)

                # Fetch marks from the database
                l = []
                SQ = "SELECT eng FROM performance"
                cursor.execute(SQ)
                for i in cursor:
                    l.append(i[0])  # Flatten tuple to extract the value

                ypoints = np.array(l)  # Convert to NumPy array

                # Fetch student names
                l1 = []
                SQ = """
                    SELECT student.name 
                    FROM student 
                    INNER JOIN performance ON student.student_id = performance.student_id
                    """
                cursor.execute(SQ)
                for i in cursor:
                    l1.append(i[0])  # Flatten tuple to extract the name

                # Plotting
                plt.figure(figsize=(10, 6))
                plt.plot(ypoints, marker='o', label="English Marks")  # Plot ypoints with markers

                # Add labels
                plt.ylabel("Marks")
                plt.xlabel("Students")
                plt.title("English Performance of Students")

                # Set custom x-axis labels (student names)
                plt.xticks(ticks=range(len(l1)), labels=l1, rotation=45)

                # Add legend
                plt.legend()

                # Show plot
                plt.tight_layout()
                plt.show()

            eng = tk.Radiobutton(win, text="English", command=english)
            eng.config(font=("Courier", 20))
            eng.place(x=1225, y=310)

            def hindi():
                import matplotlib.pyplot as plt
                import numpy as np
                import mysql.connector

                # Connect to MySQL database
                mydb = mysql.connector.connect(
                    host='127.0.0.1',
                    user='root',
                    password='garimasql',
                    database='student_in'
                )

                cursor = mydb.cursor(buffered=True)

                # Fetch marks from the database
                l = []
                SQ = "SELECT hindi FROM performance"
                cursor.execute(SQ)
                for i in cursor:
                    l.append(i[0])  # Flatten tuple to extract the value

                ypoints = np.array(l)  # Convert to NumPy array

                # Fetch student names
                l1 = []
                SQ = """
                    SELECT student.name 
                    FROM student 
                    INNER JOIN performance ON student.student_id = performance.student_id
                    """
                cursor.execute(SQ)
                for i in cursor:
                    l1.append(i[0])  # Flatten tuple to extract the name

                # Plotting
                plt.figure(figsize=(10, 6))
                plt.plot(ypoints, marker='o', label="Hindi Marks")  # Plot ypoints with markers

                # Add labels
                plt.ylabel("Marks")
                plt.xlabel("Students")
                plt.title("Hindi Performance of Students")

                # Set custom x-axis labels (student names)
                plt.xticks(ticks=range(len(l1)), labels=l1, rotation=45)

                # Add legend
                plt.legend()

                # Show plot
                plt.tight_layout()
                plt.show()

            hin = tk.Radiobutton(win, text="Hindi", command=hindi)
            hin.config(font=("Courier", 20))
            hin.place(x=1225, y=340)

            def sst():
                import matplotlib.pyplot as plt
                import numpy as np
                import mysql.connector

                # Connect to MySQL database
                mydb = mysql.connector.connect(
                    host='127.0.0.1',
                    user='root',
                    password='garimasql',
                    database='student_in'
                )

                cursor = mydb.cursor(buffered=True)

                # Fetch marks from the database
                l = []
                SQ = "SELECT sst FROM performance"
                cursor.execute(SQ)
                for i in cursor:
                    l.append(i[0])  # Flatten tuple to extract the value

                ypoints = np.array(l)  # Convert to NumPy array

                # Fetch student names
                l1 = []
                SQ = """
                    SELECT student.name 
                    FROM student 
                    INNER JOIN performance ON student.student_id = performance.student_id
                    """
                cursor.execute(SQ)
                for i in cursor:
                    l1.append(i[0])  # Flatten tuple to extract the name

                # Plotting
                plt.figure(figsize=(10, 6))
                plt.plot(ypoints, marker='o', label="SST Marks")  # Plot ypoints with markers
                plt.ylabel("Marks")
                plt.xlabel("Students")
                plt.title("SST Performance of Students")
                plt.xticks(ticks=range(len(l1)), labels=l1, rotation=45)

                # Add legend
                plt.legend()

                # Show plot
                plt.tight_layout()
                plt.show()

            ss = tk.Radiobutton(win, text="SST", command=sst)
            ss.config(font=("Courier", 20))
            ss.place(x=1225, y=370)

            def science():
                import matplotlib.pyplot as plt
                import numpy as np
                import mysql.connector

                # Connect to MySQL database
                mydb = mysql.connector.connect(
                    host='127.0.0.1',
                    user='root',
                    password='garimasql',
                    database='student_in'
                )

                cursor = mydb.cursor(buffered=True)

                # Fetch marks from the database
                l = []
                SQ = "SELECT science FROM performance"
                cursor.execute(SQ)
                for i in cursor:
                    l.append(i[0])  # Flatten tuple to extract the value

                ypoints = np.array(l)  # Convert to NumPy array

                # Fetch student names
                l1 = []
                SQ = """
                    SELECT student.name 
                    FROM student 
                    INNER JOIN performance ON student.student_id = performance.student_id
                    """
                cursor.execute(SQ)
                for i in cursor:
                    l1.append(i[0])  # Flatten tuple to extract the name

                # Plotting
                plt.figure(figsize=(10, 6))
                plt.plot(ypoints, marker='o', label="Science Marks")  # Plot ypoints with markers
                plt.ylabel("Marks")
                plt.xlabel("Students")
                plt.title("Science Performance of Students")
                plt.xticks(ticks=range(len(l1)), labels=l1, rotation=45)
                plt.legend()

                # Show plot
                plt.tight_layout()
                plt.show()

            sci = tk.Radiobutton(win, text="Science", command=science)
            sci.config(font=("Courier", 20))
            sci.place(x=1225, y=400)

            #ATTENDANCE
            mydb = mysql.connector.connect(host='127.0.0.1', user='root', password='garimasql', database='student_in')
            cursor = mydb.cursor(buffered=True)

            SQ = "SELECT attendance FROM student where student_id=%s"
            cursor.execute(SQ, (get_id,))
            a = ""
            for i in cursor:
                i = str(i)
            a = i[1:3]
            a = int(a)

            def create_gauge(value, min_value=0, max_value=100, title="Attendance"):
                norm_value = (value - min_value) / (max_value - min_value)

                theta = np.linspace(0, np.pi, 100)  # Half-circle
                radius = 1

                # Create the plot
                fig, ax = plt.subplots(figsize=(2, 4), subplot_kw={'projection': 'polar'})
                ax.set_theta_offset(np.pi / 2)  # Start at 12 o'clock
                ax.set_theta_direction(-1)  # Clockwise

                # Add the background gauge sections
                ax.bar(
                    theta,
                    np.full_like(theta, radius),
                    width=np.pi / len(theta),
                    color=["green" if t <= norm_value * np.pi else "lightgray" for t in theta],
                    edgecolor="black",
                )

                needle_theta = norm_value * np.pi
                ax.plot([needle_theta, needle_theta], [0, radius], color='red', lw=3)

                # Add the value label
                ax.text(0, -0.3, f"{value}%", ha='center', va='center', fontsize=16, transform=ax.transAxes)
                ax.text(0.5, 1.1, title, fontsize=18, ha='center', transform=ax.transAxes)
                ax.set_frame_on(False)
                ax.set_xticks([])
                ax.set_yticks([])

                return fig

            # Create the gauge chart
            fig = create_gauge(value=a, min_value=0, max_value=100, title="Attendance")

            # Embed the gauge chart in the Tkinter window using FigureCanvasTkAgg
            canvas = FigureCanvasTkAgg(fig, master=win)  # Ensure the figure is passed as 'fig'
            canvas.draw()
            canvas.get_tk_widget().place(x=97,y=320)

            #Assignment checker
            def assign():
                as_win= tk.Tk()
                as_win.title("Assignment Checker")
                as_win.geometry("900x750")
                as_win.geometry("+330+200")
                as_win.configure(bg="#B2DFEE")

                txt=tk.Label(as_win,text="Hey, Enter your assignment below ⬇ ")
                txt.config(font=("Courier", 26,"bold"),bg="#B2DFEE")
                txt.place(x=15,y=20)
                enter=tk.Text(as_win, width=72,height=26,font=("Arial", 20))
                enter.place(x=15, y=80)

                def check_text():
                    text = enter.get("1.0", "end-1c")
                    matches = tool.check(text)

                    if matches:
                        mistake=tk.Tk()
                        mistake.title("Mistakes")
                        mistake.geometry("810x420")
                        mistake.geometry("+330+200")
                        mistake.config(bg="#B2DFEE")

                        mis_lab=tk.Label(mistake,text="Mistakes found")
                        mis_lab.config(font=("Courier", 26,"bold"),bg="#B2DFEE")
                        mis_lab.place(x=15,y=15)
                        result_text = tk.Text(mistake, height=31, width=50)

                        for match in matches:
                            result_text.insert("end", f"Error: {match.message}\n")
                            result_text.insert("end",f"Context: {text[match.offset:match.offset + match.errorLength]}\n")
                            result_text.insert("end", f"Suggested Correction: {match.replacements}\n\n")
                        result_text.config(font=("Courier", 30))
                        result_text.place(x=20,y=60)
                        mistake.mainloop()
                check = tk.Button(as_win, text="CHECK", width=7, height=1,command=check_text)
                check.config(font=("Courier", 26, "bold"))
                check.place(x=720, y=21)

                as_win.mainloop()

            #Recommendations
            def recommend():
                rec = tk.Tk()
                rec.title("Recommendations")
                rec.geometry("860x500")
                rec.geometry("+330+200")

                rec_lab = tk.Label(rec, text="Recommendations as per user preferences ⇩")
                rec_lab.config(font=("Courier", 30, "bold"))
                rec_lab.place(x=20, y=20)

                # Step 1: Read the data
                file_path = '/Users/garimagrover/PycharmProjects/dash/courses.xlsx'  # Path to the file
                data = pd.read_excel(file_path)
                d = data.head()  # First 5 rows of the data (you can adjust as needed)

                # Step 2: Preprocess the data (check for null values, etc.)
                data = data.dropna(subset=['Description'])  # Drop rows with missing descriptions

                tfidf = TfidfVectorizer(stop_words='english')
                tfidf_matrix = tfidf.fit_transform(data['Description'])

                cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

                # Step 5: Function to get recommendations
                def get_recommendations(course_index, cosine_sim=cosine_sim):
                    # Get pairwise similarity scores for all courses with the given course
                    sim_scores = list(enumerate(cosine_sim[course_index]))

                    # Sort the courses based on similarity score in descending order
                    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

                    # Get the top 5 most similar courses (excluding the input course itself)
                    sim_scores = sim_scores[1:6]

                    # Get the indices of the most similar courses
                    course_indices = [i[0] for i in sim_scores]

                    # Return the top 5 most similar courses
                    return data.iloc[course_indices][['Name', 'Description']]

                # Step 6: Testing the recommendation system
                course_name = "maths"  # Example course name you want recommendations for

                # Find the index of the course
                if course_name in data['Name'].values:
                    course_index = data[data['Name'] == course_name].index[0]

                    # Get recommendations
                    recommended_courses = get_recommendations(course_index)

                    # Create Treeview widget to display recommendations in tabular format
                    tree = ttk.Treeview(rec, columns=('Course Name', 'Description'), show='headings', height=5)
                    tree.heading('Course Name', text='Course Name')
                    tree.heading('Description', text='Description')

                    tree.column('Course Name', width=400, anchor="w")
                    tree.column('Description', width=600, anchor="w")

                    for _, row in recommended_courses.iterrows():
                        tree.insert('', 'end', values=(row['Name'], row['Description']))

                    tree.place(x=20, y=80)

                # Create Treeview to display first few rows of the data (`d`)
                tree_data = ttk.Treeview(rec, columns=('Course Name', 'Description'), show='headings', height=5)
                tree_data.heading('Course Name', text='Course Name')
                tree_data.heading('Description', text='Description')

                for _, row in d.iterrows():
                    tree_data.insert('', 'end', values=(row['Name'], row['Description']))

                tree_data.place(x=20, y=250)

                rec.mainloop()

            assignment = tk.Button(win,text="Assignment Checker", width=15,height=2, command=assign)
            assignment.place(x=1219, y=458)

            recommendation = tk.Button(win, text="Course Recommendation", width=18, height=2, command=recommend)
            recommendation.place(x=1198, y=528)

            win.mainloop()
        main_window()
    else:
        messagebox.showinfo(message="Wrong login credentials ❌")


sub_btn = tk.Button(root, text='Proceed', height=2,width=7,command=main_pg)
sub_btn.grid(row=6, column=0)
sub_btn.place(x=570, y=337)

root.mainloop()
