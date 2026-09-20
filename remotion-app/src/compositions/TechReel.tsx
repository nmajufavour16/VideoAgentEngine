import React from "react";
import { AbsoluteFill, Sequence, useCurrentFrame } from "remotion";
import { SingleVoice } from "./SingleVoice";
import { DualVoice } from "./DualVoice";
import { VoicelessDiagram } from "./VoicelessDiagram";

export const TechReel: React.FC<any> = (props) => {
  const { format, scenes, design_system } = props;
  const frame = useCurrentFrame();

  const xOffset = Math.sin(frame / 60) * 15;
  const yOffset = Math.cos(frame / 80) * 15;

  let currentFrame = 0;

  return (
    <AbsoluteFill style={{ 
      backgroundColor: design_system.background,
      backgroundImage: `radial-gradient(circle at ${50 + xOffset}% ${50 + yOffset}%, ${design_system.accent_color}30, transparent 70%)`
    }}>
      {scenes.map((scene: any) => {
        const startFrame = currentFrame;
        const durationFrames = scene.duration_frames || 150;
        currentFrame += durationFrames;

        return (
          <Sequence
            key={scene.scene_id}
            from={startFrame}
            durationInFrames={durationFrames}
          >
            {format === "single_voice" && (
              <SingleVoice scene={scene} design_system={design_system} />
            )}
            {format === "dual_voice" && (
              <DualVoice scene={scene} design_system={design_system} />
            )}
            {format === "voiceless_diagram" && (
              <VoicelessDiagram scene={scene} design_system={design_system} />
            )}
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
