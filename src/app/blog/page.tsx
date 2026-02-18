import Link from 'next/link';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Blog – Jade Tseng',
};

export default function BlogPage() {
  return (
    <div className="page">
      <Link href="/" className="back-link">
        ← back
      </Link>
      <div className="content">
        <h1>Blog</h1>
        <p>Coming soon.</p>
      </div>
    </div>
  );
}

