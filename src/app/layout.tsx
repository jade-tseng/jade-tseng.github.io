import type { Metadata } from 'next';
import './globals.css';
import SpiralWrapper from '@/components/SpiralWrapper';

export const metadata: Metadata = {
  title: 'Jade Tseng',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        {children}
        <SpiralWrapper />
      </body>
    </html>
  );
}
