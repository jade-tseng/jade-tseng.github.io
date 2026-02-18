import fs from 'fs';
import path from 'path';
import Link from 'next/link';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Now – Jade Tseng',
};

/** Minimal markdown → HTML for the subset we use (headings, lists, links, emphasis). */
function renderMarkdown(md: string): string {
  let html = md
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>')
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/((?:<li>.*<\/li>\n?)+)/g, '<ul>$1</ul>')
    .replace(/\n\n+/g, '\n\n');

  html = html
    .split('\n\n')
    .map((block) => {
      block = block.trim();
      if (!block) return '';
      if (block.startsWith('<h') || block.startsWith('<ul') || block.startsWith('<ol')) {
        return block;
      }
      return '<p>' + block + '</p>';
    })
    .join('\n');

  return html;
}

export default function NowPage() {
  const mdPath = path.join(process.cwd(), 'content', 'now.md');
  const md = fs.readFileSync(mdPath, 'utf-8');
  const html = renderMarkdown(md);

  return (
    <div className="page">
      <Link href="/" className="back-link">
        ← back
      </Link>
      <div className="content" dangerouslySetInnerHTML={{ __html: html }} />
    </div>
  );
}

