namespace ECE441CityBreath
{
    public partial class NewScreenPage : ContentPage
    {
        public NewScreenPage()
        {
            InitializeComponent();
        }

        private void OnNavigateButtonClicked1(object sender, EventArgs e)
        {
            // Navigate to the new screen when the button is clicked
            Navigation.PushAsync(new MainPage());
        }

    }
}