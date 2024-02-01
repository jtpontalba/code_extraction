using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text.Json;
using System.Threading.Tasks;

namespace GrantApprovalProcess
{
    // schema
    public class GrantApplication
    {
        public int ApplicationId { get; set; }
        public string ApplicantName { get; set; }
        public decimal RequestedAmount { get; set; }
        public bool IsNonProfit { get; set; }
    }

    // schema
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

    // schema
    public class GrantApprovalManager
    {
        private readonly HttpClient httpClient = new HttpClient();
        private readonly string boredApiUrl = "https://www.boredapi.com/api/activity";
        private readonly string simulatedApiKey = Environment.GetEnvironmentVariable("SIMULATED_API_KEY");


        public GrantApprovalManager()
        {
            if (!string.IsNullOrEmpty(simulatedApiKey))
            {
                httpClient.DefaultRequestHeaders.Add("X-API-KEY", simulatedApiKey);
            }
        }

        // Business logic
        public GrantDecision EvaluateApplication(GrantApplication application)
        {
            // Choice node, with inputs application, with a rule
            if (application.RequestedAmount <= 0)
            {
                // Exception Node
                throw new InvalidGrantApplicationException("Requested amount must be greater than 0.");
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

        public async Task SendDecisionAsync(GrantDecision decision)
        {
            try
            {
                var response = await httpClient.GetAsync(boredApiUrl);
                response.EnsureSuccessStatusCode();

                var responseJson = await response.Content.ReadAsStringAsync();
                var activity = JsonSerializer.Deserialize<dynamic>(responseJson);
                Console.WriteLine($"Simulated api response: {activity}");
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
            GrantApprovalManager manager = new GrantApprovalManager();

            try
            {
                var application = new GrantApplication
                {
                    ApplicationId = 1,
                    ApplicantName = "NonProfit Org",
                    RequestedAmount = 9500,
                    IsNonProfit = true
                };

                var decision = manager.EvaluateApplication(application);
                Console.WriteLine($"Decision for Application {decision.ApplicationId}: {decision.DecisionNote}");

                // Simulating sending decision
                await manager.SendDecisionAsync(decision);
            }
            catch (InvalidGrantApplicationException e)
            {
                Console.WriteLine($"Application error: {e.Message}");
            }
            catch (Exception e)
            {
                Console.WriteLine($"An unexpected error occurred: {e.Message}");
            }
        }
    }
}
