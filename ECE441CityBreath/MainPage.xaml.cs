namespace ECE441CityBreath
{
    public partial class MainPage : ContentPage
    {
        int count = 0;

        public MainPage()
        {
            InitializeComponent();
        }

        private void OnNavigateButtonClicked(object sender, EventArgs e)
        {
            // Navigate to the new screen when the button is clicked
            Navigation.PushAsync(new NewScreenPage());
        }

        private void QuitApplication(object sender, EventArgs e)
        {
            Application.Current.Quit();
        }


    }
}