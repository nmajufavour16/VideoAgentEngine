import React from "react";
import { AbsoluteFill, Audio, staticFile } from "remotion";

export const DualVoice: React.FC<any> = ({ scene, design_system }) => {
  return (
    <AbsoluteFill
      style={{
        flexDirection: "row",
        fontFamily: design_system.font_family,
        color: design_system.text_primary,
      }}
    >
      {scene.audio_file_path && <Audio src={staticFile(scene.audio_file_path)} />}
      <div style={{ flex: 1, borderRight: `4px solid ${design_system.accent_color}`, display: "flex", justifyContent: "center", alignItems: "center" }}>
        {scene.speaker === "Lead" && (
          <h2 style={{ fontSize: "60px", padding: "40px", textAlign: "center" }}>{scene.display_text}</h2>
        )}
      </div>
      <div style={{ flex: 1, display: "flex", justifyContent: "center", alignItems: "center" }}>
        {scene.speaker === "Expert" && (
          <h2 style={{ fontSize: "60px", padding: "40px", textAlign: "center", color: design_system.accent_color }}>{scene.display_text}</h2>
        )}
      </div>
    </AbsoluteFill>
  );
};
