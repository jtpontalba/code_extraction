# Grant Approval .NET App

## Changing Grant Application Criteria

```
...
ApplicationId = 1,
ApplicantName = "FakeNonProfit",
RequestedAmount = 9500,
IsNonProfit = true
```

## Running the app
Set fake api key in terminal
```
$ set SIMULATED_API_KEY="testing123"
```
In the project directory run the following:
```
$ dotnet build     
```

```
4 dotnet run
```

## Expected Output
```
Decision for Application 1: Approved for funding
Simulated api response: {"activity":"Wash your car","type":"busywork","participants":1,"price":0.05,"link":"","key":"1017771","accessibility":0.15}
```
