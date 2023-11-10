using System.Diagnostics;
using System;
using Microsoft.Maui.Controls;

namespace ECE441CityBreath
{
    public partial class DashboardPage : ContentPage
    {
        public DashboardPage()
        {
            InitializeComponent();
        }

        private void NavigateToRobotControllerPage(object sender, EventArgs e)
        {
            // Navigate to the Robot Controller screen when the button is clicked
            Navigation.PushAsync(new RobotControllerPage());
        }

        private void NavigateToRawDataPage(object sender, EventArgs e)
        {
            // Navigate to the Raw Data screen when the button is clicked
            //Navigation.PushAsync(new RawDataPage()); 
            try
            {
                string exeFilePath = @"C:\FilesForProject\RawDataTable.exe"; // Replace with the actual path to your .exe file
                Process.Start(exeFilePath);
            }
            catch (Exception ex)
            {
                // Handle any exceptions that may occur when starting the process
                Console.WriteLine($"Error: {ex.Message}");
            }
        }

        private void NavigateToCleanedDataPage(object sender, EventArgs e)
        {
            // Navigate to the Cleaned Data screen when the button is clicked
            Navigation.PushAsync(new CleanedDataPage()); 
        }
    }
}
