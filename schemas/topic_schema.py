from pydantic import BaseModel, Field

class Topic(BaseModel):
    title: str = Field(description="The main title of the topic")
    hook: str = Field(description="A catchy hook to grab the audience's attention")
    mechanism: str = Field(description="A brief explanation of how it works under the hood")
    metaphor: str = Field(description="A visual or relatable metaphor for the concept")
    complexity: int = Field(description="Complexity rating from 1 to 10")
    
    # Internal routing suggestions
    recommended_format: str = Field(description="Suggested video format: single_voice, dual_voice, or voiceless_diagram")
