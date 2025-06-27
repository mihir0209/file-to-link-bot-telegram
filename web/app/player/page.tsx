"use client";

import { useSearchParams } from "next/navigation";
import { useState, useEffect } from "react";

export default function PlayerPage() {
  const searchParams = useSearchParams();
  const [videoUrl, setVideoUrl] = useState<string | null>(null);

  useEffect(() => {
    // Only set on client
    setVideoUrl(searchParams.get("url"));
  }, [searchParams]);

  if (!videoUrl) {
    return <div style={{ textAlign: "center", marginTop: 40 }}>No video URL provided.</div>;
  }

  return (
    <div style={{ maxWidth: 800, margin: "2rem auto", padding: 16 }}>
      <h2 style={{ textAlign: "center" }}>Online Video Player</h2>
      <video
        src={decodeURIComponent(videoUrl)}
        controls
        style={{
          width: "100%",
          height: "auto",
          borderRadius: 12,
          boxShadow: "0 4px 24px rgba(0,0,0,0.15)",
          background: "#000",
        }}
      />
      {/* Download Link */}
      <div style={{ marginTop: 16, textAlign: "center" }}>
        <a
          href={decodeURIComponent(videoUrl)}
          download
          style={{ marginRight: 16, textDecoration: "underline" }}
        >
          Download Video
        </a>
        {/* External Player Links */}
        <a
          href={`intent:${decodeURIComponent(videoUrl)}#Intent;package=com.mxtech.videoplayer.ad;S.title=Video;end`}
          target="_blank"
          rel="noopener noreferrer"
          style={{ marginRight: 16, textDecoration: "underline" }}
        >
          Open in MX Player
        </a>
        <a
          href={`playit://play?url=${encodeURIComponent(decodeURIComponent(videoUrl))}`}
          target="_blank"
          rel="noopener noreferrer"
          style={{ textDecoration: "underline" }}
        >
          Open in Playit
        </a>
      </div>
    </div>
  );
}
``