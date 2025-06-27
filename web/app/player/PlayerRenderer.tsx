// app/player/PlayerRenderer.tsx
'use client';

import { useSearchParams } from 'next/navigation';

export default function PlayerRenderer() {
  const searchParams = useSearchParams();

  let fileUrl: string | null = null;
  let fileName: string = 'Unknown File';
  let fileType: string = '';

  try {
    fileUrl = searchParams.get('url');
    fileName = searchParams.get('name') || 'Unknown File';
    fileType = searchParams.get('type') || '';
  } catch (error) {
    console.error('Error reading search params:', error);
  }

  if (!fileUrl) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100 dark:bg-gray-900">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-800 dark:text-gray-200 mb-4">
            No File Specified
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Please provide a valid file URL to view or play the content.
          </p>
        </div>
      </div>
    );
  }

  const isVideo =
    fileType.startsWith('video/') ||
    (fileUrl && fileUrl.match(/\.(mp4|webm|ogg|avi|mkv|mov)$/i) !== null);
  const isImage =
    fileType.startsWith('image/') ||
    (fileUrl && fileUrl.match(/\.(jpg|jpeg|png|gif|webp|svg|bmp)$/i) !== null);

  return (
    <div className="min-h-screen bg-black flex flex-col">
      <header className="bg-gray-900 text-white p-4">
        <h1 className="text-xl font-semibold truncate">{fileName}</h1>
      </header>

      <main className="flex-1 flex items-center justify-center p-4">
        {isVideo ? (
          <video
            controls
            autoPlay
            className="max-w-full max-h-full"
            src={fileUrl}
          >
            Your browser does not support the video element.
          </video>
        ) : isImage ? (
          <img
            src={fileUrl}
            alt={fileName}
            className="max-w-full max-h-full object-contain"
          />
        ) : (
          <div className="text-center text-white">
            <h2 className="text-2xl mb-4">Unsupported File Type</h2>
            <p className="mb-4">This file type cannot be previewed.</p>
            <a
              href={fileUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded transition-colors"
            >
              Download File
            </a>
          </div>
        )}
      </main>
    </div>
  );
}
