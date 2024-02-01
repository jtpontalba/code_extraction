﻿using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text.Json;
using System.Threading.Tasks;

namespace GrantApprovalProcess
{
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
        private readonly string openAiCompletionUrl = "https://api.openai.com/v1/completions";
        private readonly string openAiApiKey = Environment.GetEnvironmentVariable("OPENAI_API_KEY");

        public GrantApprovalManager()
        {
            if (!string.IsNullOrEmpty(openAiApiKey))
            {
                httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", openAiApiKey);
            }
        }

        public GrantDecision EvaluateApplication(GrantApplication application)
        {
            if (application.RequestedAmount <= 0)
            {
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
            if (string.IsNullOrEmpty(openAiApiKey))
            {
                Console.WriteLine("OpenAI API key is not set.");
                return;
            }

            try
            {
                var prompt = $"Generate a summary for a grant application decision where " +
                             $"the application ID is {decision.ApplicationId}, " +
                             $"the decision was '{(decision.Approved ? "approved" : "rejected")}', " +
                             $"and the note was: {decision.DecisionNote}.";

                var requestData = new
                {
                    model = "text-davinci-003", // Use an appropriate model
                    prompt = prompt,
                    temperature = 0.7,
                    max_tokens = 60
                };

                var json = JsonSerializer.Serialize(requestData);
                var content = new StringContent(json, System.Text.Encoding.UTF8, "application/json");
                httpClient.DefaultRequestHeaders.Add("Content-Type", "application/json");

                var response = await httpClient.PostAsync(openAiCompletionUrl, content);
                response.EnsureSuccessStatusCode();

                var responseJson = await response.Content.ReadAsStringAsync();
                var completion = JsonSerializer.Deserialize<dynamic>(responseJson);
                Console.WriteLine($"OpenAI Completion: {completion.choices[0].text}");
            }
            catch (HttpRequestException e)
            {
                Console.WriteLine($"Error sending decision to OpenAI: {e.Message}");
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