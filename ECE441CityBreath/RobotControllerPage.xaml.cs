using Microsoft.Maui.Controls;
using System;

namespace ECE441CityBreath
{
    public partial class RobotControllerPage : ContentPage
    {
        public RobotControllerPage()
        {
            InitializeComponent();
        }

        private void OnMainGridTapped(object sender, EventArgs e)
        {
            if (SlideMenu.WidthRequest > 0)
            {
                // Close the menu
                SlideMenu.WidthRequest = 0;
            }
        }

        private void OnHamburgerButtonClicked(object sender, EventArgs e)
        {
            // Open the menu
            SlideMenu.WidthRequest = 200; // Adjust the width as per your requirement
        }
    }
}
