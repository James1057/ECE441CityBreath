import pandas as pd
import pymysql
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

class MySQLTableViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Cleaned Data Viewer")

        #Subtitle
        subtitle_label = tk.Label(root, text="Welcome to the Cleaned Data Viewer. Press 'Fetch Data' for data", font=("Helvetica", 24))
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

    def normalize_sensor_data(self, data):
        # Create DataFrame from the data
        df = pd.DataFrame(data, columns=['HostName_datetimeStart','Hostname','datetime', 'AirSensor1', 'AirSensor2', 'AirSensor3', 'AirSensor4', 'AirSensor5', 'AirSensor6','latitude','longitude','altitude'])

        # Define boundaries for normalization
        boundaries = {
            'AirSensor1': (0, 100),  # Assuming you want to scale the temperature to 0-100 for simplicity
            'AirSensor2': (0, 100),  # Same for humidity
            'AirSensor3': (0, 50000), # Methane ppm
            'AirSensor4': (400, 604), # CO2 ppm
            'AirSensor5': (0, 604),   # PM2.5
            'AirSensor6': (0, 604),   # PM10
        }

        # Normalize each sensor column based on the given boundaries
        scaler = MinMaxScaler(feature_range=(0, 100))
        for sensor, (min_val, max_val) in boundaries.items():
            # Clip the values before scaling
            df[sensor] = df[sensor].clip(lower=min_val, upper=max_val)
            df[sensor] = scaler.fit_transform(df[[sensor]])

        return df


# ... (Other parts of the class remain unchanged)

    def display_latest_run(self, df):
    # Assume the latest run is the first row in the DataFrame
        latest_run = df.iloc[0]

        # Extract the sensor names and their normalized values
        sensor_names = ['AirSensor1', 'AirSensor2', 'AirSensor3', 'AirSensor4', 'AirSensor5', 'AirSensor6']
        sensor_values = [latest_run[sensor] for sensor in sensor_names]

        # Create a bar chart for the latest run
        fig, ax = plt.subplots(figsize=(10, 6))
        # Set up the x-axis positions for the bars
        x_positions = range(len(sensor_names))
        # Plot the bars with the specified linewidth and width covering the full x-axis
        bars = ax.bar(x_positions, sensor_values, color='skyblue', edgecolor='black', linewidth=1, align='edge', width=1)

        for bar, value in zip(bars, sensor_values):
            height = bar.get_height()
            ax.annotate(f'{value:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


        # Define the comfortable ranges for each sensor on a 0-100 scale
        comfortable_ranges = {
            'AirSensor1': (30, 70),
            'AirSensor2': (40, 60),
            'AirSensor3': (20, 80),
            'AirSensor4': (25, 75),
            'AirSensor5': (10, 50),
            'AirSensor6': (10, 50)
        }

        # Highlight the comfortable ranges for each sensor
        for idx, sensor in enumerate(sensor_names):
            low, high = comfortable_ranges[sensor]
            ax.axhspan(low, high, xmin=(idx)/len(sensor_names), xmax=(idx+1)/len(sensor_names), color='green', alpha=0.3)

        # Add labels and title
        ax.set_xlabel('Air Sensors')
        ax.set_ylabel('Normalized Value (0-100)')
        ax.set_title('Latest Run Normalized Sensor Values')
        ax.set_ylim([0, 100])

        # Set the x-axis labels and limits
        ax.set_xticks([i + 0.5 for i in x_positions])  # Center the labels
        ax.set_xticklabels(sensor_names)
        ax.set_xlim([0, len(sensor_names)])  # Set the x-axis limits to match the number of bars

        # Create a custom legend
        handles = [plt.Rectangle((0,0),1,1, color='green', alpha=0.3)]
        labels = ["Comfortable Range"]
        ax.legend(handles, labels, loc='upper left', bbox_to_anchor=(1, 1))

        # Show the plot with a tight layout
        plt.tight_layout()
        plt.show()


    def fetch_and_display(self):
        # Fetch data from the database
        data, columns = self.execute_query()

        # Create DataFrame from the data
        df = pd.DataFrame(data, columns=columns)

        # Store the DataFrame in the class for later use
        self.full_df = df

        # Get unique HostName_datatimeStart values and ensure they are strings
        runs = [str(run) for run in df['HostName_datetimeStart'].unique()]

        # Create a dropdown for selecting the run to display
        self.run_var = tk.StringVar()
        run_dropdown = ttk.Combobox(self.root, textvariable=self.run_var, values=runs)
        run_dropdown.pack()
        run_dropdown.bind("<<ComboboxSelected>>", self.on_run_selected)


    def on_run_selected(self, event):
        try:
            # Get the selected run as a string
            selected_run = self.run_var.get()

            # Filter the DataFrame for the selected run
            run_df = self.full_df[self.full_df['HostName_datetimeStart'].astype(str) == selected_run]

            # If there is data for the selected run, display it
            if not run_df.empty:
                normalized_run_df = self.normalize_sensor_data(run_df)
                self.display_latest_run(normalized_run_df)
            else:
                print("No data found for the selected run.")  # Debug print
        except Exception as e:
            print(f"Error occurred: {e}")  # Print out the exception if one occurs



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

# ... (Keep the main function and the if __name__ == "__main__": part as is)

    

