from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    topic: str
    tone: str
    context: str           
    draft: str             
    feedback: str          
    iteration: Annotated[int, operator.add] 
    is_pass: bool          