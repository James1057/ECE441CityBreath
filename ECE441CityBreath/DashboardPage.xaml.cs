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
                string exeFileName = "RawDataTable.exe";
                string exeFilePath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Resources", "Scripts", exeFileName);
                Process.Start(exeFilePath);
            }
            catch (Exception ex)
            {
                // Handle exceptions
                Console.WriteLine($"Error: {ex.Message}");
            }
        }

        private void NavigateToCleanedDataPage(object sender, EventArgs e)
        {
            // Navigate to the Cleaned Data Page screen when the button is clicked
            Navigation.PushAsync(new CleanedDataPage());

        }
    }    
}
