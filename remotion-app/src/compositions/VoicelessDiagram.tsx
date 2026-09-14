import React from "react";
import { AbsoluteFill, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const VoicelessDiagram: React.FC<any> = ({ scene, design_system }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({
    frame,
    fps,
    config: { damping: 10 },
  });

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        fontFamily: design_system.font_family,
        color: design_system.text_primary,
      }}
    >
      <div style={{ transform: `scale(${scale})`, display: "flex", alignItems: "center", gap: "40px" }}>
        <div style={{ width: "200px", height: "200px", borderRadius: "50%", backgroundColor: design_system.accent_color, display: "flex", justifyContent: "center", alignItems: "center", fontSize: "40px", color: design_system.background }}>
          {scene.ui_elements?.left_node || "Node A"}
        </div>
        <div style={{ fontSize: "60px", fontWeight: "bold" }}>&rarr;</div>
        <div style={{ width: "200px", height: "200px", borderRadius: "50%", border: `10px solid ${design_system.accent_color}`, display: "flex", justifyContent: "center", alignItems: "center", fontSize: "40px" }}>
          {scene.ui_elements?.right_node || "Node B"}
        </div>
      </div>
      <h2 style={{ position: "absolute", bottom: "100px", fontSize: "50px" }}>{scene.display_text}</h2>
    </AbsoluteFill>
  );
};
