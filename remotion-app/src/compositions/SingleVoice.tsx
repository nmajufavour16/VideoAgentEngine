import React from "react";
import { AbsoluteFill, spring, useCurrentFrame, useVideoConfig, Audio, staticFile } from "remotion";
import { LayoutResolver } from "./LayoutResolver";

export const SingleVoice: React.FC<any> = ({ scene, design_system }) => {
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
      <LayoutResolver scene={scene} design_system={design_system} />
    </AbsoluteFill>
  );
};
