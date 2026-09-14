import React from "react";
import { AbsoluteFill, spring, useCurrentFrame, useVideoConfig, Audio, staticFile } from "remotion";

export const SingleVoice: React.FC<any> = ({ scene, design_system }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame,
    fps,
    config: { damping: 12 },
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
      {scene.audio_file_path && <Audio src={staticFile(scene.audio_file_path)} />}
      <div
        style={{
          transform: `scale(${entrance})`,
          textAlign: "center",
          padding: "40px",
        }}
      >
        <h1 style={{ fontSize: "80px", fontWeight: "bold", marginBottom: "20px" }}>
          {scene.display_text || scene.ui_elements?.headline}
        </h1>
        {scene.ui_elements?.sub_badge && (
          <div
            style={{
              backgroundColor: design_system.accent_color,
              color: design_system.background,
              padding: "10px 20px",
              borderRadius: "20px",
              display: "inline-block",
              fontSize: "30px",
              fontWeight: "bold",
            }}
          >
            {scene.ui_elements.sub_badge}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
