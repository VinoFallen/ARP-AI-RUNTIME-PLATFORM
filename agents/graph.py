# agents/graph.py
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
import operator
from .nodes.supervisor import supervisor_node
from .nodes.research import research_node
from .nodes.writer import writer_node

class AgentState(TypedDict):
    messages: Annotated[List[dict], operator.add]
    next_agent: str          # which agent runs next
    task: str                # original user task
    research_output: str     # filled by research agent
    final_output: str        # filled by writer agent
    iteration: int           # guard against infinite loops

def build_graph():
    g = StateGraph(AgentState)
 
    g.add_node('supervisor', supervisor_node)
    g.add_node('research',   research_node)
    g.add_node('writer',     writer_node)
 
    g.set_entry_point('supervisor')
 
    # Conditional routing from supervisor
    g.add_conditional_edges('supervisor',
        lambda s: s['next_agent'],
        {'research': 'research', 'writer': 'writer', END: END}
    )
 
    # After research or writing, always check supervisor again
    g.add_edge('research', 'supervisor')
    g.add_edge('writer',   'supervisor')
 
    # Safety: max 5 iterations
    return g.compile()
 
agent_graph = build_graph()
