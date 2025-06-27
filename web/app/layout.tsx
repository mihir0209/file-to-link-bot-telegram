import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'FileToLink Web Player',
  description: 'Stream videos and view images from FileToLink Bot',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="font-sans">{children}</body>
    </html>
  );
}