using MySql.Data.MySqlClient;
using System.Diagnostics;
using static System.Net.Mime.MediaTypeNames;
using System.Threading;
using System.Data;
using System;
using System.Threading.Tasks;


namespace ECE441CityBreath
{
    public partial class NewScreenPage : ContentPage
    {
        public NewScreenPage()
        {
            InitializeComponent();
        }
       

        void OnEntryTextChangedUsername(object sender, TextChangedEventArgs e)
        {
            string oldText = e.OldTextValue;
            string newText = e.NewTextValue;
            string myText = entryUserName.Text;

            //myUserName.Text = myText;

        }

        void OnEntryTextChangedPassword(object sender, TextChangedEventArgs e)
        {
            string oldText = e.OldTextValue;
            string newText = e.NewTextValue;
            string myText = entryPassword.Text;

            //myPassword.Text = myText;

        }

        void OnEntryCompleted(object sender, EventArgs e)
        {
            string text = ((Entry)sender).Text;

        }

        private void OnNavigateButtonClicked1(object sender, EventArgs e)
        {
            // Navigate to the new screen when the button is clicked
            Navigation.PushAsync(new MainPage());
        }

        private void OnNavigateButtonClickedLogin(object sender, EventArgs e)
        {
            //Getting the user name and password
            String UserName = entryUserName.Text;
            String PassWord = entryPassword.Text;

            //Testing purpose
            if (UserName == "test")
            {
                Navigation.PushAsync(new DashboardPage());
            }

            //Make the connection
            MySql.Data.MySqlClient.MySqlConnection conn;
            string myConnectionString = DBUtils.GetDBConnection();
            conn = new MySql.Data.MySqlClient.MySqlConnection();
            conn.ConnectionString = myConnectionString;
            Debug.WriteLine(UserName);
            Debug.WriteLine(PassWord);
            String valid = "false";
            try
            {
                conn.Open();
                var stm = "SELECT Username, password FROM Gas.tbl_Users WHERE Username = '" + UserName + "' AND password = '" + PassWord + "' AND Account_Status = 2";
                var cmd = new MySqlCommand(stm, conn);
                MySqlDataReader rdr = cmd.ExecuteReader();
                while (rdr.Read())
                {
                    string username = rdr.IsDBNull(0) ? null : rdr.GetString(0);
                    string password = rdr.IsDBNull(1) ? null : rdr.GetString(1);

                    Debug.WriteLine("{0}, {1}", username, password);
                    valid = "true";
                }
            }
            catch
            {
                //MessageBox.Show("Bad input");
            }

            // Navigate to the new screen when the button is clicked
            if (valid == "true")
            {
                conn.Close();
                Navigation.PushAsync(new DashboardPage());
            }
            //else
            //{
            //    Task.Run(async () =>
            //    {
            //        await Task.Delay(5000); // 5000 milliseconds (5 seconds)

            //        // Code to run after the delay (runs on a separate thread)
            //        // You can't access UI elements directly from here; use the main thread for UI updates if needed
            //    }).Wait();
            //}
            
        }

    }
}