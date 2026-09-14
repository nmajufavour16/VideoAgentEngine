from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class DesignSystem(BaseModel):
    mode: Literal["light", "dark", "contrast"]
    background: str
    text_primary: str
    accent_color: str
    font_family: str = "Inter, sans-serif"

class SceneUI(BaseModel):
    headline: Optional[str] = None
    sub_badge: Optional[str] = None
    diagram_type: Optional[str] = None
    left_node: Optional[str] = None
    right_node: Optional[str] = None
    action_type: Optional[str] = None
    highlight_words: List[str] = []

class Scene(BaseModel):
    scene_id: int
    layout_type: Literal["title_hook", "split_screen", "metric_comparison", "flow_diagram", "rule_takeaway"]
    speaker: Literal["Lead", "Expert", "Narrator", "None"]
    voice_id: Optional[str] = None
    spoken_text: Optional[str] = None
    display_text: Optional[str] = None
    ui_elements: SceneUI
    duration_frames: Optional[int] = None
    audio_file_path: Optional[str] = None

class Entity(BaseModel):
    id: str
    icon: str
    label: str

class TimelineStep(BaseModel):
    step_id: int
    source_entity: str
    target_entity: str
    action: Literal["flow", "delete", "encrypt", "transform", "highlight"]
    visual_effect: Literal["pulse", "shatter", "dissolve", "highlight"]
    kinetic_text: str

class VideoPayload(BaseModel):
    title: str
    topic_badge: str
    format: Literal["single_voice", "dual_voice", "voiceless_diagram"]
    design_system: DesignSystem
    scenes: Optional[List[Scene]] = None
    entities: Optional[List[Entity]] = None
    timeline: Optional[List[TimelineStep]] = None
