import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

interface KineticTextProps {
  text: string;
  style?: React.CSSProperties;
}

export const KineticText: React.FC<KineticTextProps> = ({ text, style }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  if (!text) return null;

  const words = text.split(" ");

  return (
    <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", ...style }}>
      {words.map((word, i) => {
        const delay = i * 4; // stagger entrance
        
        const entrance = spring({
          frame: Math.max(0, frame - delay),
          fps,
          config: { damping: 14, mass: 0.5 },
        });

        return (
          <span
            key={i}
            style={{
              display: "inline-block",
              marginRight: "15px",
              marginBottom: "10px",
              transform: `translateY(${(1 - entrance) * 50}px)`,
              opacity: entrance,
            }}
          >
            {word}
          </span>
        );
      })}
    </div>
  );
};
