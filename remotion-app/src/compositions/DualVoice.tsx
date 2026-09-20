import React from "react";
import { AbsoluteFill, Audio, staticFile, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { LayoutResolver } from "./LayoutResolver";

export const DualVoice: React.FC<any> = ({ scene, design_system }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Badge animation
  const badgeEntrance = spring({
    frame: frame - 10, // Slight delay
    fps,
    config: { damping: 12 },
  });

  const isLead = scene.speaker === "Lead";

  return (
    <AbsoluteFill
      style={{
        fontFamily: design_system.font_family,
        color: design_system.text_primary,
        justifyContent: "center",
        alignItems: "center"
      }}
    >
      {scene.audio_file_path && <Audio src={staticFile(scene.audio_file_path)} />}
      
      {/* Full screen layout */}
      <LayoutResolver scene={scene} design_system={design_system} />

      {/* Speaker Badge */}
      {scene.speaker !== "None" && (
        <div
          style={{
            position: "absolute",
            bottom: "50px",
            left: isLead ? "50px" : undefined,
            right: !isLead ? "50px" : undefined,
            transform: `translateY(${(1 - badgeEntrance) * 100}px)`,
            opacity: badgeEntrance,
            backgroundColor: "rgba(255, 255, 255, 0.1)",
            backdropFilter: "blur(10px)",
            padding: "15px 30px",
            borderRadius: "50px",
            border: `2px solid ${design_system.accent_color}`,
            boxShadow: `0 0 20px ${design_system.accent_color}50`,
            display: "flex",
            alignItems: "center",
            gap: "15px",
            fontSize: "30px",
            fontWeight: "bold",
            color: design_system.accent_color
          }}
        >
          <span>🎙️</span>
          <span>{scene.speaker}</span>
        </div>
      )}
    </AbsoluteFill>
  );
};
