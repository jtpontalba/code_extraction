from UniversalApplication.UniversalApplication import UniversalApplication
from UniversalApplication.Enums import NodeType, RuleActionType
from UniversalApplication.UniversalNode import *
from UniversalApplication.UniversalApplication import UniversalApplication
from UniversalApplication.Enums import (
    WorkflowType,
    NodeType,
)
from UniversalApplication.UniversalExpression import *


uan = UniversalApplication()
flow = uan.addWorkflow(
    key="main_flow", name="main", id_namespace="workflow", flow_type=WorkflowType.Flow
)


# Start Node
node_start = {
    "id": uan.get_id("Main"),
    "name": "main_start",
    "references": [uan.get_id("try")],
}
flow.addNode(NodeType.Start, **node_start)


# Evaluate Application SubSubflow
eval_subflow = uan.addWorkflow(
    key="evaluate_application",
    name="evaluate_application",
    flow_type=WorkflowType.Subflow,
)
eval_node_start = {
    "id": uan.get_id("eval_start"),
    "name": "eval_start",
    "references": [uan.get_id("eval_choice_node_1")],
}

eval_choice_node_1 = {
    "id": uan.get_id("eval_choice_node_1"),
    "name": "eval_choice_node_1",
    "references": [uan.get_id("eval_ex_node"), uan.get_id("eval_choice_node_2")],
    "expressions": [],
    "expressionMap": [
        {
            "expressionId": None,
            "referenceId": None,
        },
        {
            "expressionId": uan.get_id("ex_path"),
            "referenceId": uan.get_id("eval_ex_node"),
        },
        {
            "expressionId": uan.get_id("choice_path"),
            "referenceId": uan.get_id("eval_choice_node_2"),
        },
    ],
}

eval_ex_node = {
    "id": uan.get_id("eval_ex_node"),
    "name": "InvalidOperationExceptio",
    "expressions": [],
    "expressionMap": [],
}

eval_choice_node_2 = {
    "id": uan.get_id("eval_choice_node_2"),
    "name": "eval_choice_node_2",
    "references": [uan.get_id("eval_node_1"), uan.get_id("eval_node_3")],
    "expressions": [],
    "expressionMap": [
        {"expressionId": None, "referenceId": None},
        {
            "expressionId": uan.get_id("choice2_path1"),
            "referenceId": uan.get_id("eval_node_1"),
        },
        {
            "expressionId": uan.get_id("choice2_path2"),
            "referenceId": uan.get_id("eval_node_3"),
        },
    ],
}

eval_node_1 = {
    "id": uan.get_id("eval_node_1"),
    "name": "decision.Approved = true;",
    "expressions": [],
    "references": [uan.get_id("eval_node_2")],
}

eval_node_2 = {
    "id": uan.get_id("eval_node_2"),
    "name": 'decision.DecisionNote = "Approved for funding";',
    "references": [uan.get_id("eval_end_node")],
}

eval_end_node = {
    "id": uan.get_id("eval_end_node"),
    "name": "eval_end_node",
}

eval_node_3 = {
    "id": uan.get_id("eval_node_3"),
    "name": "decision.Approved = false;",
    "references": [uan.get_id("eval_node_4")],
}

eval_node_4 = {
    "id": uan.get_id("eval_node_4"),
    "name": 'decision.DecisionNote = "Rejected: Criteria not met";',
    "references": [uan.get_id("eval_end_node")],
}

eval_subflow.addNode(NodeType.Start, **eval_node_start)
eval_subflow.addNode(NodeType.Choice, **eval_choice_node_1)
eval_subflow.addNode(NodeType.Exception, **eval_ex_node)
eval_subflow.addNode(NodeType.Choice, **eval_choice_node_2)
eval_subflow.addNode(NodeType.Unknown, **eval_node_1)
eval_subflow.addNode(NodeType.Unknown, **eval_node_2)
eval_subflow.addNode(NodeType.End, **eval_end_node)
eval_subflow.addNode(NodeType.Unknown, **eval_node_3)
eval_subflow.addNode(NodeType.Unknown, **eval_node_4)

# FetchBoredActivityAsync
http_subflow = uan.addWorkflow(
    key="fetch_bored_activity_async",
    name="FetchBoredActivityAsync",
    flow_type=WorkflowType.Subflow,
)

http_flow_start = {
    "id": uan.get_id("http_start"),
    "name": "http_start",
    "references": [uan.get_id("http_call")],
}

http_flow_n1 = {
    "id": uan.get_id("http_call"),
    "name": "var response = await httpClient.GetAsync(boredApiUrl);",
    "references": [uan.get_id("response.EnsureSuccessStatusCode();")],
    "externalConnectionId": uan.get_id("https://www.boredapi.com/api/activity"),
}

http_flow_n2 = {
    "id": uan.get_id("response.EnsureSuccessStatusCode();"),
    "name": "response.EnsureSuccessStatusCode();",
    "references": [
        uan.get_id("var responseJson = await response.Content.ReadAsStringAsync();")
    ],
}

http_flow_n3 = {
    "id": uan.get_id("var responseJson = await response.Content.ReadAsStringAsync();"),
    "name": "var responseJson = await response.Content.ReadAsStringAsync();",
    "references": [
        uan.get_id("var activity = JsonSerializer.Deserialize<dynamic>(responseJson);")
    ],
}

http_flow_n4 = {
    "id": uan.get_id(
        "var activity = JsonSerializer.Deserialize<dynamic>(responseJson);"
    ),
    "name": "var activity = JsonSerializer.Deserialize<dynamic>(responseJson);",
    "references": [
        uan.get_id('Console.WriteLine($"Suggested Activity: \{activity\}");')
    ],
}

http_flow_n5 = {
    "id": uan.get_id('Console.WriteLine($"Suggested Activity: \{activity\}");'),
    "name": 'Console.WriteLine($"Suggested Activity: \{activity\}");',
    "references": [uan.get_id("choice_http")],
}

http_flow_n6 = {
    "id": uan.get_id(
        'Console.WriteLine($"Error fetching activity from Bored API: \{e.Message\}");'
    ),
    "name": "HttpRequestException",
}

http_flow_n7 = {
    "id": uan.get_id('Console.WriteLine($"Unexpected error: \{e.Message\}");'),
    "name": "Exception",
}

http_flow_choice = {
    "id": uan.get_id("choice_http"),
    "name": "Try",
    "references": [],
    "expressions": [],
    "expressionMap": [
        {"expressionId": None, "referenceId": None},
        {
            "expressionId": uan.get_id("http_choice_path1"),
            "referenceId": uan.get_id("http_end"),
        },
        {
            "expressionId": uan.get_id("http_choice_path2"),
            "referenceId": uan.get_id(
                'Console.WriteLine($"Error fetching activity from Bored API: \{e.Message\}");'
            ),
        },
        {
            "expressionId": uan.get_id("http_choice_path3"),
            "referenceId": uan.get_id(
                'Console.WriteLine($"Unexpected error: \{e.Message\}");'
            ),
        },
    ],
}

http_end = {"id": uan.get_id("http_end"), "name": "http_end"}

http_subflow.addNode(NodeType.Start, **http_flow_start)
http_subflow.addNode(NodeType.HTTP_Request, **http_flow_n1)
http_subflow.addNode(NodeType.Unknown, **http_flow_n2)
http_subflow.addNode(NodeType.Unknown, **http_flow_n3)
http_subflow.addNode(NodeType.Unknown, **http_flow_n4)
http_subflow.addNode(NodeType.Unknown, **http_flow_n5)
http_subflow.addNode(NodeType.Choice, **http_flow_choice)
http_subflow.addNode(NodeType.End, **http_end)
http_subflow.addNode(NodeType.Exception, **http_flow_n6)
http_subflow.addNode(NodeType.Exception, **http_flow_n7)


# Try Block
try_subflow = uan.addWorkflow(
    key="try_block",
    name="try_subflow",
    flow_type=WorkflowType.Subflow,
)
try_node_start = {
    "id": uan.get_id("main_try_start"),
    "name": "main_try_start",
    "type": NodeType.Start.value,
    "references": [uan.get_id("try_EvaluateApplication")],
}
try_subflow.addNode(NodeType.Start, **try_node_start)

node_1 = {
    "id": uan.get_id("try_EvaluateApplication"),
    "name": "EvaluateApplication",
    "inputs": [{"name": "application", "type": "GrantApplication"}],
    "references": [
        uan.get_id(
            'Console.WriteLine($"Decision for Application \{decision.ApplicationId\}: \{decision.DecisionNote\}");'
        )
    ],
    "subflowReferenceId": eval_subflow.id,
}
try_subflow.addNode(NodeType.Subflow, **node_1)

node_2 = {
    "id": uan.get_id(
        'Console.WriteLine($"Decision for Application \{decision.ApplicationId\}: \{decision.DecisionNote\}");'
    ),
    "name": "console_line",
    "references": [uan.get_id("FetchBoredActivityAsync")],
}
try_subflow.addNode(NodeType.Unknown, **node_2)

node_3 = {
    "id": uan.get_id("FetchBoredActivityAsync"),
    "name": "FetchBoredActivityAsync",
    "references": [uan.get_id("try_end_node")],
    "subflowReferenceId": http_subflow.id,
}
try_subflow.addNode(NodeType.Subflow, **node_3)

try_end_node = {
    "id": uan.get_id("try_end_node"),
    "name": "try_end_node",
}

try_subflow.addNode(NodeType.End, **try_end_node)

# Try Subflow Node
node_subflow = {
    "id": uan.get_id("try"),
    "name": "try",
    "subflowReferenceId": try_subflow.id,
    "references": [uan.get_id("main_choice")],
}
flow.addNode(NodeType.Subflow, **node_subflow)

# Add remaining nodes to main flow
main_choice = {
    "id": uan.get_id("main_choice"),
    "name": "try",
    "references": [
        uan.get_id("main_end"),
        uan.get_id("main_node_1"),
        uan.get_id("main_node_2"),
        uan.get_id("main_node_3"),
    ],
    "expressionMap": [
        {
            "expressionId": uan.get_id("main_choice_path_1"),
            "referenceId": uan.get_id("main_end"),
        },
        {
            "expressionId": uan.get_id("main_choice_path_2"),
            "referenceId": uan.get_id("main_node_1"),
        },
        {
            "expressionId": uan.get_id("main_choice_path_3"),
            "referenceId": uan.get_id("main_node_2"),
        },
        {
            "expressionId": uan.get_id("main_choice_path_4"),
            "referenceId": uan.get_id("main_node_3"),
        },
        {"expressionId": None, "referenceId": None},
    ],
}

main_end = {
    "id": uan.get_id("main_end"),
    "name": "main_end",
}

main_node_1 = {
    "id": uan.get_id("main_node_1"),
    "name": "InvalidGrantApplicationException",
}

main_node_2 = {
    "id": uan.get_id("main_node_2"),
    "name": "InvalidOperationException",
}

main_node_3 = {
    "id": uan.get_id("main_node_3"),
    "name": "Exception",
}

flow.addNode(NodeType.Choice, **main_choice)
flow.addNode(NodeType.End, **main_end)
flow.addNode(NodeType.Exception, **main_node_1)
flow.addNode(NodeType.Exception, **main_node_2)
flow.addNode(NodeType.Exception, **main_node_3)


# Adding Expressions

# main flow
ue_main_flow_choice_p1 = UniversalExpression(
    id=uan.get_id("main_choice_path_2"),
    operation="InvalidGrantApplicationException == True",
    value="InvalidGrantApplicationException == True",
)
ue_main_flow_choice_p2 = UniversalExpression(
    id=uan.get_id("main_choice_path_3"),
    operation="InvalidOperationException == True​",
    value="InvalidOperationException == True​",
)
ue_main_flow_choice_p3 = UniversalExpression(
    id=uan.get_id("main_choice_path_4"),
    operation="Exception == True​",
    value="Exception == True​",
)
uan.expressions.append(ue_main_flow_choice_p1)
uan.expressions.append(ue_main_flow_choice_p2)
uan.expressions.append(ue_main_flow_choice_p3)

# evaluate_application subflow
ue_evaluate_application_inputs_1 = {"inputs": [{"name": "currentUser", "type": "User"}]}
ue_evaluate_application_1 = UniversalExpression(
    id=uan.get_id("ex_path"),
    inputs=ue_evaluate_application_inputs_1["inputs"],
    operation="currentUser.Role != UserRole.Administrator && currentUser.Role != UserRole.Reviewer == True​​",
    value="currentUser.Role != UserRole.Administrator && currentUser.Role != UserRole.Reviewer == True​​",
)

ue_evaluate_application_inputs_2 = {
    "inputs": [{"name": "application", "type": "GrantApplication"}]
}
ue_evaluate_application_2 = UniversalExpression(
    id=uan.get_id("choice_path"),
    inputs=ue_evaluate_application_inputs_2["inputs"],
    operation="application.RequestedAmount <= 10000 && application.IsNonProfit​​​",
    value="application.RequestedAmount <= 10000 && application.IsNonProfit​​​",
)

uan.expressions.append(ue_evaluate_application_1)
uan.expressions.append(ue_evaluate_application_2)

print(f"uan: {uan.toJSON()}")
import json

with open(r"D:\RhinoAI\code_extraction\Program_manual_extraction.json", "w") as f:
    json.dump(uan.toDict(), f)
