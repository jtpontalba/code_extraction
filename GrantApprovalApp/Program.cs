using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text.Json;
using System.Threading.Tasks;

namespace GrantApprovalProcess
{
    public enum UserRole
    {
        Administrator,
        Reviewer,
        Applicant
    }

    public class User
    {
        public string Name { get; set; }
        public UserRole Role { get; set; }

        public User(string name, UserRole role)
        {
            Name = name;
            Role = role;
        }
    }

    public class GrantApplication
    {
        public int ApplicationId { get; set; }
        public string ApplicantName { get; set; }
        public decimal RequestedAmount { get; set; }
        public bool IsNonProfit { get; set; }
    }

    public class GrantDecision
    {
        public int ApplicationId { get; set; }
        public bool Approved { get; set; }
        public string DecisionNote { get; set; }
    }

    public class InvalidGrantApplicationException : Exception
    {
        public InvalidGrantApplicationException(string message) : base(message)
        {
        }
    }

    public class GrantApprovalManager
    {
        private readonly HttpClient httpClient = new HttpClient();
        private readonly string boredApiUrl = "https://www.boredapi.com/api/activity";
        private User currentUser;

        public GrantApprovalManager(User user)
        {
            currentUser = user;
            var simulatedApiKey = Environment.GetEnvironmentVariable("SIMULATED_API_KEY");
            if (!string.IsNullOrEmpty(simulatedApiKey))
            {
                httpClient.DefaultRequestHeaders.Add("X-API-KEY", simulatedApiKey);
            }
        }

        public GrantDecision EvaluateApplication(GrantApplication application)
        {
            if (currentUser.Role != UserRole.Administrator && currentUser.Role != UserRole.Reviewer)
            {
                throw new InvalidOperationException("Insufficient permissions to evaluate applications.");
            }

            var decision = new GrantDecision { ApplicationId = application.ApplicationId };

            if (application.RequestedAmount <= 10000 && application.IsNonProfit)
            {
                decision.Approved = true;
                decision.DecisionNote = "Approved for funding";
            }
            else
            {
                decision.Approved = false;
                decision.DecisionNote = "Rejected: Criteria not met";
            }

            return decision;
        }

        public async Task FetchBoredActivityAsync()
        {
            try
            {
                var response = await httpClient.GetAsync(boredApiUrl);
                response.EnsureSuccessStatusCode();

                var responseJson = await response.Content.ReadAsStringAsync();
                var activity = JsonSerializer.Deserialize<dynamic>(responseJson);
                Console.WriteLine($"Suggested Activity: {activity}");
            }
            catch (HttpRequestException e)
            {
                Console.WriteLine($"Error fetching activity from Bored API: {e.Message}");
            }
            catch (Exception e)
            {
                Console.WriteLine($"Unexpected error: {e.Message}");
            }
        }
    }

    class Program
    {
        static async Task Main(string[] args)
        {
            // Example of user roles
            var adminUser = new User("Admin", UserRole.Administrator);

            // Initialize manager with an administrator user
            GrantApprovalManager manager = new GrantApprovalManager(adminUser);

            // Create a grant application
            var application = new GrantApplication
            {
                ApplicationId = 1,
                ApplicantName = "NonProfit Org",
                RequestedAmount = 9500,
                IsNonProfit = true
            };

            // Evaluate the application
            try
            {
                var decision = manager.EvaluateApplication(application);
                Console.WriteLine($"Decision for Application {decision.ApplicationId}: {decision.DecisionNote}");

                // Fetch a suggested activity
                await manager.FetchBoredActivityAsync();
            }
            catch (InvalidGrantApplicationException e)
            {
                Console.WriteLine($"Application error: {e.Message}");
            }
            catch (InvalidOperationException e)
            {
                Console.WriteLine(e.Message); // For insufficient permissions
            }
            catch (Exception e)
            {
                Console.WriteLine($"An unexpected error occurred: {e.Message}");
            }
        }
    }
}
