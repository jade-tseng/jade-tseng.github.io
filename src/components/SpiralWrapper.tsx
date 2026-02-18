'use client';

import { usePathname } from 'next/navigation';
import Spiral from './Spiral';

export default function SpiralWrapper() {
  const pathname = usePathname();
  const isHome = pathname === '/';

  return (
    <div className={`spiral-wrapper ${isHome ? 'spiral-home' : 'spiral-mini'}`}>
      <Spiral />
    </div>
  );
}

