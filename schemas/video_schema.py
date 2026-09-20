from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class DesignSystem(BaseModel):
    mode: Literal["light", "dark", "contrast"]
    background: str
    text_primary: str
    accent_color: str
    font_family: str

class SceneUI(BaseModel):
    headline: Optional[str]
    sub_badge: Optional[str]
    diagram_type: Optional[str]
    left_node: Optional[str]
    right_node: Optional[str]
    action_type: Optional[str]
    highlight_words: List[str]
    table_headers: Optional[List[str]]
    table_rows: Optional[List[List[str]]]
    icon_list: Optional[List[str]]
    bullet_points: Optional[List[str]]

class Scene(BaseModel):
    scene_id: int
    layout_type: Literal["title_hook", "split_screen", "metric_comparison", "flow_diagram", "rule_takeaway", "table_view", "icon_grid", "bullet_list"]
    speaker: Literal["Lead", "Expert", "Narrator", "None"]
    voice_id: Optional[str]
    spoken_text: Optional[str]
    display_text: Optional[str]
    ui_elements: SceneUI
    duration_frames: Optional[int]
    audio_file_path: Optional[str]

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
    scenes: Optional[List[Scene]]
    entities: Optional[List[Entity]]
    timeline: Optional[List[TimelineStep]]
