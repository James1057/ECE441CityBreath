namespace ECE441CityBreath
{
    public partial class MainPage : ContentPage
    {
        int count = 0;

        public MainPage()
        {
            InitializeComponent();
        }

        private void OnCounterClicked(object sender, EventArgs e)
        {
            count++;

            if (count == 1)
                CounterBtn.Text = $"Clicked {count} time";
            else
                CounterBtn.Text = $"Clicked {count} times";

            SemanticScreenReader.Announce(CounterBtn.Text);
        }

        private void OnNavigateButtonClicked(object sender, EventArgs e)
        {
            // Navigate to the new screen when the button is clicked
            Navigation.PushAsync(new NewScreenPage());
        }
    }
}