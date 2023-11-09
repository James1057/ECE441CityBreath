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
            Navigation.PushAsync(new RawDataPage()); 
        }

        private void NavigateToCleanedDataPage(object sender, EventArgs e)
        {
            // Navigate to the Cleaned Data screen when the button is clicked
            Navigation.PushAsync(new CleanedDataPage()); 
        }
    }
}
