using System.Diagnostics;
using System;
using Microsoft.Maui.Controls;

namespace ECE441CityBreath
{
    public partial class CleanedDataPage : ContentPage
    {
        public CleanedDataPage()
        {
            InitializeComponent();
        }

        private void HistogramPlot(object sender, EventArgs e)
        {
            // Navigate to the Raw Data screen when the button is clicked
            //Navigation.PushAsync(new RawDataPage()); 
            try
            {
                string exeFileName = "CleanedData.exe";
                string exeFilePath1 = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Resources", "Scripts", exeFileName);
                Process.Start(exeFilePath1);
            }
            catch (Exception ex)
            {
                // Handle exceptions
                Console.WriteLine($"Error: {ex.Message}");
            }
        }
        private void LinePlot(object sender, EventArgs e)
        {
            try
            {
                string exeFileName = "Lineplots.exe";
                string exeFilePath2 = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Resources", "Scripts", exeFileName);
                Process.Start(exeFilePath2);
            }
            catch (Exception ex)
            {
                // Handle exceptions
                Console.WriteLine($"Error: {ex.Message}");
            }
        }
    }
}

