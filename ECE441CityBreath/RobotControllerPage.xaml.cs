using Microsoft.Maui.Controls;
using System;
using System.Net.Sockets;
using System.Text;
using System;
using System.Net.Sockets;
using System.Text;
using Button = Microsoft.Maui.Controls.Button;

namespace ECE441CityBreath
{
    public partial class RobotControllerPage : ContentPage
    {
        public RobotControllerPage()
        {
            InitializeComponent();

            // Create a WebView control
            webView = new WebView
            {
                VerticalOptions = LayoutOptions.FillAndExpand,
                HorizontalOptions = LayoutOptions.FillAndExpand,
                Source = new UrlWebViewSource
                {
                    Url = "http://104.194.104.247:5000/",
                },
            };

            HamburgerButton = new Microsoft.Maui.Controls.Button
            {
                Text = "≡",
                VerticalOptions = LayoutOptions.Start,
                HorizontalOptions = LayoutOptions.Start,
            };
            HamburgerButton.Clicked += OnHamburgerButtonClicked;

            // Create a StackLayout for the slide menu
            SlideMenu = new StackLayout
            {
                WidthRequest = 0, // Initially hidden
                //BackgroundColor = Color.LightGray,
                Children =
                {
                    new Microsoft.Maui.Controls.Button { Text = "Close menu", Command = new Command(() => HandleMenuOptionClick("Option 1")) },
                    new Button { Text = "Option 2", Command = new Command(() => HandleMenuOptionClick("Option 2")) },
                    // Add more menu options as needed
                },
            };

            var arrowControllersGrid = new Grid
            {
                VerticalOptions = LayoutOptions.End,
                HorizontalOptions = LayoutOptions.End,
                WidthRequest = 200,
                HeightRequest = 150,
                RowDefinitions =
                {
                    new RowDefinition { Height = GridLength.Star },
                    new RowDefinition { Height = GridLength.Star }
                },
                ColumnDefinitions =
                {
                    new ColumnDefinition { Width = GridLength.Star },
                    new ColumnDefinition { Width = GridLength.Star },
                    new ColumnDefinition { Width = GridLength.Star }
                }
            };

            // Up Button
            var upButton = new Button
            {
                Text = "↑",
            };
            upButton.Pressed += OnForward;
            Grid.SetRow(upButton, 0);
            Grid.SetColumn(upButton, 1);
            arrowControllersGrid.Children.Add(upButton);

            // Left Button
            var leftButton = new Button
            {
                Text = "←",
            };
            leftButton.Pressed += OnLeft;
            Grid.SetRow(leftButton, 1);
            Grid.SetColumn(leftButton, 0);
            arrowControllersGrid.Children.Add(leftButton);

            // Right Button
            var rightButton = new Button
            {
                Text = "→",
            };
            rightButton.Pressed += OnRight;
            Grid.SetRow(rightButton, 1);
            Grid.SetColumn(rightButton, 2);
            arrowControllersGrid.Children.Add(rightButton);

            // Down Button
            var downButton = new Button
            {
                Text = "↓",
            };
            downButton.Pressed += OnBackward;
            Grid.SetRow(downButton, 1);
            Grid.SetColumn(downButton, 1);
            arrowControllersGrid.Children.Add(downButton);

            // Quit Button
            var quitButton = new Button
            {
                Text = "Quit",
            };
            quitButton.Pressed += OnQuit;
            Grid.SetRow(quitButton, 0);
            Grid.SetColumn(quitButton, 2);
            arrowControllersGrid.Children.Add(quitButton);

            // Stand Button
            var standButton = new Button
            {
                Text = "Stand",
            };
            standButton.Pressed += OnStand;
            Grid.SetRow(standButton, 0);
            Grid.SetColumn(standButton, 0);
            arrowControllersGrid.Children.Add(standButton);

            // Add the WebView to the content of the page
            Content = new StackLayout
            {
                Children = { HamburgerButton, SlideMenu, webView, arrowControllersGrid },
            };
        }

       

        private void HandleMenuOptionClick(string option)
        {
            // Handle the menu option click
            // You can perform actions based on the selected option
            // For example, close the menu and perform some action
            SlideMenu.WidthRequest = 0;
            if (option == "Option 1")
                SlideMenu.WidthRequest = 0;


            // Add your logic here based on the selected option
            // You may want to send data or perform other actions
            // TransmitData(DBUtils.GetIP(), DBUtils.GetPort(), option);
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

        private void OnLeft(object sender, EventArgs e)
        {
            // Open the menu
            // Set the IP address and port to connect to
            TransmitData(DBUtils.GetIP(), DBUtils.GetPort(), "a");
        }
        private void OnRight(object sender, EventArgs e)
        {
            // Open the menu
            // Set the IP address and port to connect to
            TransmitData(DBUtils.GetIP(), DBUtils.GetPort(), "d");
        }

        private void OnForward(object sender, EventArgs e)
        {
            // Open the menu
            // Set the IP address and port to connect to
            TransmitData(DBUtils.GetIP(), DBUtils.GetPort(), "w");
        }

        private void OnBackward(object sender, EventArgs e)
        {
            // Open the menu
            // Set the IP address and port to connect to
            TransmitData(DBUtils.GetIP(), DBUtils.GetPort(), "s");
        }

        private void OnQuit(object sender, EventArgs e)
        {
            // Open the menu
            // Set the IP address and port to connect to
            
            TransmitData(DBUtils.GetIP(), DBUtils.GetPort(), "q");
        }

        private void OnStand(object sender, EventArgs e)
        {
            // Open the menu
            // Set the IP address and port to connect to
            TransmitData(DBUtils.GetIP(), DBUtils.GetPort(), "e");
        }

        static void TransmitData(string ipAddress, int port, string data, bool closeConnection = true)
        {
            TcpClient tcpClient = null;
            NetworkStream networkStream = null;

            try
            {
                // Create a TcpClient
                tcpClient = new TcpClient();

                // Connect to the server
                tcpClient.Connect(ipAddress, port);
                Console.WriteLine($"Connected to {ipAddress}:{port}");

                // Get the network stream from the client
                networkStream = tcpClient.GetStream();

                // Send the data to the server
                byte[] dataBuffer = Encoding.ASCII.GetBytes(data);
                networkStream.Write(dataBuffer, 0, dataBuffer.Length);

                Console.WriteLine("Data transmitted.");

            }
            catch (Exception ex)
            {
                Console.WriteLine($"An error occurred: {ex.Message}");
            }
            finally
            {
                // Close the network stream and TcpClient in the finally block to ensure they are always closed
                if (networkStream != null)
                    networkStream.Close();

                if (tcpClient != null)
                    tcpClient.Close();

                Console.WriteLine("Connection closed.");
            }
        }
    }
}
