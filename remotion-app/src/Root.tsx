import React from "react";
import { Composition, getInputProps } from "remotion";
import { TechReel } from "./compositions/TechReel";
import defaultData from "../public/data.json";

export const RemotionRoot: React.FC = () => {
  const cliProps = getInputProps();
  const data = (Object.keys(cliProps).length > 0 && cliProps.format) ? cliProps : defaultData;

  const durationInFrames = data.scenes?.reduce((acc: number, scene: any) => acc + (scene.duration_frames || 150), 0) || 150;

  return (
    <>
      <Composition
        id="TechReel"
        component={TechReel}
        durationInFrames={durationInFrames}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={data}
      />
    </>
  );
};
