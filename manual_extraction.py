from UniversalApplication.UniversalApplication import UniversalApplication
from UniversalApplication.Enums import NodeType, RuleActionType
from UniversalApplication.UniversalNode import *
from UniversalApplication.UniversalApplication import UniversalApplication
from UniversalApplication.UniversalExpression import UniversalExpression
from UniversalApplication.Enums import (
    WorkflowType,
    NodeType,
)


uan = UniversalApplication()
flow = uan.addWorkflow(
    key="main_flow",
    name="main",
    id_namespace="workflow",
    flow_type=WorkflowType.Flow
)


# Start Node
node_start = {"id":uan.get_id('Main'),
              "name":"main_start",
               "references":[uan.get_id('try')]}
flow.addNode(NodeType.Start, **node_start)
# print(f"node_dict:{node_start}\n\n")
# print(f"flow: {flow.toDict()}\n\n")
# print(f"node:{node.toDict()}\n\n")
# print(f"uan: {uan.toJSON()}\n\n")

# Intermediate lines
# // Example of user roles
# var adminUser = new User("Admin", UserRole.Administrator);

# // Initialize manager with an administrator user
# GrantApprovalManager manager = new GrantApprovalManager(adminUser);

# // Create a grant application
# var application = new GrantApplication



# Try Block
try_subflow = uan.addWorkflow(
    key="try_block",
    name="try_subflow",
    flow_type=WorkflowType.Subflow,
)
try_node_start = {"id":uan.get_id('main_try_start'),
                  "name":"main_try_start", 
                  "type": NodeType.Start.value,
                  "references":[uan.get_id('try_EvaluateApplication')]}
try_subflow.addNode(NodeType.Start, **try_node_start)

node_1 = {
    "id":uan.get_id('try_EvaluateApplication'),
    "name":"EvaluateApplication", 
    "inputs": [{"name": "application", "type": "GrantApplication"}],
    "references":[uan.get_id("Console.WriteLine($\"Decision for Application \{decision.ApplicationId\}: \{decision.DecisionNote\}\");")]
}
try_subflow.addNode(NodeType.Subflow, **node_1)

node_2 = {
    "id":uan.get_id("Console.WriteLine($\"Decision for Application \{decision.ApplicationId\}: \{decision.DecisionNote\}\");"),
    "name":"console_line", 
    "references":[uan.get_id("FetchBoredActivityAsync")]
}
try_subflow.addNode(NodeType.Unknown, **node_2)

node_3 = {
    "id":uan.get_id("FetchBoredActivityAsync"),
    "name":"FetchBoredActivityAsync", 
    "references": [uan.get_id("try_end_node")]
}
try_subflow.addNode(NodeType.Subflow, **node_3)

try_end_node = {
    "id":uan.get_id("try_end_node"),
    "name":"try_end_node", 
}

try_subflow.addNode(NodeType.End, **try_end_node)

# Try Subflow Node
node_subflow = {
    "id":uan.get_id('try'),
    "name":"try",
    "subflowReferenceId":try_subflow.id}
flow.addNode(NodeType.Subflow, **node_subflow)


# Evaluate Application SubSubflow
eval_subflow = uan.addWorkflow(
    key="evaluate_application",
    name="evaluate_application",
    flow_type=WorkflowType.Subflow,
)
eval_node_start = {"id":uan.get_id('eval_start'),
                  "name":"eval_start", 
                  "type": NodeType.Start.value,
                  "references":None}
eval_subflow.addNode(NodeType.Start, **try_node_start)

eval_node_1 = {"id":uan.get_id('eval_node_1'),
                  "name":"'eval_node_1'", 
                  "type": NodeType.Choice.value,
                  "references":None,
                  "expressions": None,
                  "expressionMap": None}

eval_node_2 = {"id":uan.get_id('eval_node_2'),
                  "name":"'eval_node_2'", 
                  "type": NodeType.Unknown.value,
                  "references":None,
                  "expressions": None,
                  "expressionMap": None}

eval_subflow.addNode(NodeType.Start, **eval_node_1)


print(f"uan: {uan.toJSON()}\n\n")