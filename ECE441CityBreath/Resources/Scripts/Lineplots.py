import pandas as pd
import pymysql
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import tkinter as tk
from tkinter import ttk

class Lineplots:
    def __init__(self, root):
        self.root = root
        self.root.title("Sensor Data Viewer")

        #Subtitle
        subtitle_label = tk.Label(root, text="Select a run and a sensor, then press 'Fetch Data' to view the data", font=("Helvetica", 16))
        subtitle_label.pack(pady=10)

        # MySQL connection details
        self.host = "104.194.104.247"
        self.user = "Admin"
        self.password = "I6xH#w92K"
        self.database = "Gas"
        
        # Initial data fetch to populate the runs dropdown
        self.runs_df = self.fetch_data_from_db()
        
        # Dropdown for run selection
        self.run_var = tk.StringVar(root)
        self.runs = self.runs_df['HostName_datetimeStart'].unique().tolist()
        self.run_dropdown = ttk.Combobox(root, textvariable=self.run_var, values=self.runs)
        self.run_dropdown.pack()

        # Dropdown for sensor selection
        self.sensor_var = tk.StringVar(root)
        self.sensors = ['AirSensor1', 'AirSensor2', 'AirSensor3', 'AirSensor4', 'AirSensor5', 'AirSensor6']
        self.sensor_dropdown = ttk.Combobox(root, textvariable=self.sensor_var, values=self.sensors)
        self.sensor_dropdown.pack()

        # Button to fetch and display data
        fetch_button = tk.Button(root, text="Fetch Data", command=self.fetch_and_display)
        fetch_button.pack(pady=10)

    def fetch_data_from_db(self):
        # Fetch all runs initially to populate the dropdown, adjust query as needed
        query = "SELECT DISTINCT HostName_datetimeStart FROM tbl_Data"
        connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        try:
            df = pd.read_sql_query(query, connection)
        finally:
            connection.close()
        return df

    def fetch_and_display(self):
        selected_run = self.run_var.get()
        selected_sensor = self.sensor_var.get()
        if selected_run and selected_sensor:
            self.plot_run_data(selected_run, selected_sensor)

    def plot_run_data(self, selected_run, selected_sensor):
        query = f"SELECT datetime, {selected_sensor} FROM tbl_Data WHERE HostName_datetimeStart = '{selected_run}'"
        connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        try:
            df = pd.read_sql_query(query, connection)
        finally:
            connection.close()
        
        # Convert the 'datetime' column to datetime
        df['datetime'] = pd.to_datetime(df['datetime'])
        
        # Plot
        plt.figure(figsize=(10, 5))
        plt.plot(df['datetime'], df[selected_sensor], label=selected_sensor, marker='o')
        plt.title(f'{selected_sensor} Readings for Run {selected_run}')
        plt.xlabel('Time')
        plt.ylabel('Sensor Value')
        plt.gca().xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
        plt.legend()
        plt.tight_layout()
        plt.show()


def main():
    root = tk.Tk()
    root.geometry("400x300")
    app = Lineplots(root)
    root.mainloop()

if __name__ == "__main__":
    main()
