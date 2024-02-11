using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text.Json;
using System.Threading.Tasks;

namespace GrantApprovalProcess
{
    // Role definition
    public enum UserRole
    {
        Administrator,
        Reviewer,
        Applicant
    }

    // Domain Object definition
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

    // Domain Object definition
    public class GrantApplication
    {
        public int ApplicationId { get; set; }
        public string ApplicantName { get; set; }
        public decimal RequestedAmount { get; set; }
        public bool IsNonProfit { get; set; }
    }

    // Domain Object definition
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

    // Actual Role
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
        // Business logic #1 
        public GrantDecision EvaluateApplication(GrantApplication application)
        {
            // Choice Node with Rule Evaluation
            if (currentUser.Role != UserRole.Administrator && currentUser.Role != UserRole.Reviewer)
            {
                // Exception Node
                throw new InvalidOperationException("Insufficient permissions to evaluate applications.");
            }

            var decision = new GrantDecision { ApplicationId = application.ApplicationId };

            // Choice Node with rule evaluation with domain inputs Application
            if (application.RequestedAmount <= 10000 && application.IsNonProfit)
            {
                decision.Approved = true;
                decision.DecisionNote = "Approved for funding";
            }
            // default path 
            else
            {
                decision.Approved = false;
                decision.DecisionNote = "Rejected: Criteria not met";
            }

            return decision;
        }

        // Business Logic #2 another workflow or subflow?
        public async Task FetchBoredActivityAsync()
        {
            // start node
            try
            {
                // node
                var response = await httpClient.GetAsync(boredApiUrl);

                // Step Nodes/Expressions
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
    // Main Logic
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
