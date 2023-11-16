using Microsoft.Maui.Controls;
using System;
using System.Net.Sockets;
using System.Text;
using System;
using System.Net.Sockets;
using System.Text;

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
