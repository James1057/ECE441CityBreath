import pandas as pd
import pymysql
import tkinter as tk
from tkinter import ttk

class MySQLTableViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Raw Data Viewer")

        #Subtitle
        subtitle_label = tk.Label(root, text="Welcome to the Raw Data Viewer. Press 'Fetch Data' for data", font=("Helvetica", 24))
        subtitle_label.pack(pady=10)


        # MySQL connection details
        self.host = "104.194.104.247"
        self.user = "Admin"
        self.password = "I6xH#w92K"
        self.database = "Gas"

        # MySQL query
        self.query = "SELECT * FROM tbl_Data"

        # Create a Treeview widget
        
        self.tree = ttk.Treeview(root, show="headings")
        self.tree["columns"] = ()


        # Add a scrollbar
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Button to fetch and display data
        fetch_button = tk.Button(root, text="Fetch Data", command=self.fetch_and_display)
        fetch_button.pack(pady=10)

    def execute_query(self):
        connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cursor = connection.cursor()
        cursor.execute(self.query)
        result = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        connection.close()
        return result, columns

    def fetch_and_display(self):
        data, columns = self.execute_query()

        # Update Treeview columns
        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=100)

        # Insert data into Treeview
        self.tree.delete(*self.tree.get_children())
        for row in data:
            self.tree.insert("", "end", values=row)

        # Pack Treeview
        self.tree.pack(expand=True, fill="both")

def main():
    root = tk.Tk()

    #root.attributes('-fullscreen', True)
    root.geometry("1200x600")

    app = MySQLTableViewer(root)

    # Bind the Escape key to exit full-screen mode
    #root.bind('<Escape>', lambda event: root.attributes('-fullscreen', False))

    root.mainloop()

if __name__ == "__main__":
    main()
