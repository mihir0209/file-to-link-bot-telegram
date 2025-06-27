// app/player/page.tsx

import { Suspense } from 'react';
import PlayerRenderer from './PlayerRenderer';

function LoadingFallback() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 dark:bg-gray-900">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <p className="text-gray-600 dark:text-gray-400">Loading player...</p>
      </div>
    </div>
  );
}

export const dynamic = 'force-dynamic';
export const runtime = 'nodejs';

export default function PlayerPage() {
  return (
    <Suspense fallback={<LoadingFallback />}>
      <PlayerRenderer />
    </Suspense>
  );
}
