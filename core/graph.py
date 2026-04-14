from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import retrieve_knowledge, generate_draft, review_draft

def should_continue(state: AgentState):
    if state["is_pass"] or state["iteration"] >= 3:
        return "end"
    return "rewrite"

def build_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("researcher", retrieve_knowledge)
    workflow.add_node("writer", generate_draft)
    workflow.add_node("reviewer", review_draft)
    
    workflow.set_entry_point("researcher")
    workflow.add_edge("researcher", "writer")
    workflow.add_edge("writer", "reviewer")
    
    workflow.add_conditional_edges(
        "reviewer",
        should_continue,
        {
            "end": END,
            "rewrite": "writer"
        }
    )
    
    return workflow.compile()

agent_app = build_graph()