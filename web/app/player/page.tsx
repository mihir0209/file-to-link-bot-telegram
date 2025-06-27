import './globals.css';
import type { Metadata } from 'next';

// Apply Geist font globally via CSS variables
const geistSans = {
  variable: '--font-geist-sans',
};
const geistMono = {
  variable: '--font-geist-mono',
};

export const metadata: Metadata = {
  title: 'FileToLink Web Player',
  description: 'Stream videos and view images from FileToLink Bot',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${geistSans.variable} ${geistMono.variable}`}>
      <head>
        <style jsx global>{`
          :root {
            --font-geist-sans: 'GeistSans', sans-serif;
            --font-geist-mono: 'GeistMono', monospace;
          }
          body {
            font-family: var(--font-geist-sans);
          }
        `}</style>
      </head>
      <body>{children}</body>
    </html>
  );
}