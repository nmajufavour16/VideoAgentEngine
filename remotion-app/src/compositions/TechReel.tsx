import React from "react";
import { AbsoluteFill, Sequence } from "remotion";
import { SingleVoice } from "./SingleVoice";
import { DualVoice } from "./DualVoice";
import { VoicelessDiagram } from "./VoicelessDiagram";

export const TechReel: React.FC<any> = (props) => {
  const { format, scenes, design_system } = props;

  let currentFrame = 0;

  return (
    <AbsoluteFill style={{ backgroundColor: design_system.background }}>
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
