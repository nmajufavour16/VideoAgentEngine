import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import * as LucideIcons from "lucide-react";
import { KineticText } from "./KineticText";

export const DynamicIcon: React.FC<{ name: string; size?: number; color?: string }> = ({ name, size = 48, color }) => {
  const IconComponent = (LucideIcons as any)[name] || (LucideIcons as any).HelpCircle;
  return <IconComponent size={size} color={color} />;
};

export const LayoutResolver: React.FC<any> = ({ scene, design_system }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame,
    fps,
    config: { damping: 14 },
  });

  const { layout_type, display_text, ui_elements } = scene;
  const { headline, table_headers, table_rows, icon_list, bullet_points, sub_badge } = ui_elements || {};

  const titleText = headline || display_text;

  // Rich Layout rendering
  if (layout_type === "table_view") {
    return (
      <div style={{ transform: `translateY(${(1 - entrance) * 100}px) scale(${0.95 + entrance * 0.05})`, opacity: entrance, display: "flex", flexDirection: "column", alignItems: "center", width: "80%" }}>
        <KineticText text={titleText} style={{ fontSize: "70px", fontWeight: "bold", marginBottom: "40px", textAlign: "center" }} />
        <table style={{ 
            width: "100%", 
            borderCollapse: "collapse", 
            backgroundColor: "rgba(255, 255, 255, 0.05)",
            backdropFilter: "blur(10px)",
            borderRadius: "20px",
            overflow: "hidden",
            boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.25)"
          }}>
          {table_headers && (
            <thead>
              <tr style={{ backgroundColor: design_system.accent_color, color: design_system.background }}>
                {table_headers.map((th: string, i: number) => (
                  <th key={i} style={{ padding: "30px", fontSize: "40px", textAlign: "left" }}>{th}</th>
                ))}
              </tr>
            </thead>
          )}
          <tbody>
            {table_rows?.map((row: string[], i: number) => (
              <tr key={i} style={{ borderBottom: "2px solid rgba(255,255,255,0.1)" }}>
                {row.map((cell: string, j: number) => (
                  <td key={j} style={{ padding: "30px", fontSize: "35px" }}>{cell}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }

  if (layout_type === "icon_grid") {
    return (
      <div style={{ transform: `translateY(${(1 - entrance) * 100}px)`, opacity: entrance, display: "flex", flexDirection: "column", alignItems: "center", width: "90%" }}>
        <KineticText text={titleText} style={{ fontSize: "80px", fontWeight: "bold", marginBottom: "60px", textAlign: "center" }} />
        <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", gap: "60px" }}>
          {icon_list?.map((iconName: string, i: number) => (
            <div key={i} style={{ 
                padding: "50px", 
                backgroundColor: "rgba(255, 255, 255, 0.05)",
                borderRadius: "30px",
                border: `4px solid ${design_system.accent_color}`,
                boxShadow: `0 0 40px ${design_system.accent_color}40`,
                display: "flex",
                flexDirection: "column",
                alignItems: "center"
              }}>
              <DynamicIcon name={iconName} size={100} color={design_system.accent_color} />
              <div style={{ marginTop: "20px", fontSize: "30px", fontWeight: "bold" }}>{iconName}</div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (layout_type === "bullet_list") {
    return (
      <div style={{ transform: `translateY(${(1 - entrance) * 100}px)`, opacity: entrance, display: "flex", flexDirection: "column", alignItems: "flex-start", width: "80%" }}>
        <KineticText text={titleText} style={{ fontSize: "80px", fontWeight: "bold", marginBottom: "60px", color: design_system.accent_color }} />
        <div style={{ display: "flex", flexDirection: "column", gap: "40px", width: "100%" }}>
          {bullet_points?.map((point: string, i: number) => {
            // Stagger animation
            const delay = i * 10;
            const pointEntrance = spring({
              frame: Math.max(0, frame - delay),
              fps,
              config: { damping: 12 },
            });
            return (
              <div key={i} style={{ 
                  transform: `translateX(${(1 - pointEntrance) * 100}px)`, 
                  opacity: pointEntrance,
                  display: "flex", 
                  alignItems: "center", 
                  gap: "30px",
                  fontSize: "45px",
                  backgroundColor: "rgba(255, 255, 255, 0.05)",
                  padding: "30px",
                  borderRadius: "20px"
                }}>
                <DynamicIcon name="CheckCircle2" size={50} color={design_system.accent_color} />
                <span>{point}</span>
              </div>
            );
          })}
        </div>
      </div>
    );
  }

  // Fallback (title_hook, etc.)
  return (
    <div
      style={{
        transform: `translateY(${(1 - entrance) * 100}px)`,
        opacity: entrance,
        textAlign: "center",
        padding: "40px",
      }}
    >
      <KineticText text={titleText} style={{ fontSize: "80px", fontWeight: "bold", marginBottom: "20px" }} />
      {sub_badge && (
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
          {sub_badge}
        </div>
      )}
    </div>
  );
};
