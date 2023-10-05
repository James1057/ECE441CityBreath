using static System.Net.Mime.MediaTypeNames;

namespace ECE441CityBreath
{
    public partial class NewScreenPage : ContentPage
    {
        public NewScreenPage()
        {
            InitializeComponent();
        }
       

        void OnEntryTextChanged(object sender, TextChangedEventArgs e)
        {
            string oldText = e.OldTextValue;
            string newText = e.NewTextValue;
            string myText = entry.Text;

            myLabel.Text = myText;

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

    }
}