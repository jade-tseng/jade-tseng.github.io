import Link from 'next/link';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Library – Jade Tseng',
};

export default function LibraryPage() {
  return (
    <div className="page">
      <Link href="/" className="back-link">
        ← back
      </Link>
      <div className="content">
        <h1>books i&apos;m reading</h1>
        <p>
          Blaise Aguera y Arcas &lsquo;What Is Intelligence? Lessons from AI About
          Evolution, Computing, and Minds&rsquo;
          <br />
          Iain Banks &lsquo;The Player of Games&rsquo;
        </p>

        <h1>books i love [mostly fiction]</h1>
        <p>
          Marguerite Yourcenar&apos;s Memoirs of Hadrian
          <br />
          James Baldwin&apos;s Giovanni&apos;s Room
          <br />
          Clarice Lispector&apos;s The Passion According to G.H.
          <br />
          Mikhail Bulgakov&apos;s The Master and Margarita
          <br />
          David Abram&apos;s Spell of the Sensuous
          <br />
          Elena Ferrante&apos;s Neapolitan Quartet
          <br />
          Cixin Liu&apos;s Three Body Problem trilogy
          <br />
          Adrian Tchaikovsky&apos;s Children of Time
          <br />
          Benjamin Labatut&apos;s When We Cease to Understand the World
          <br />
          Susanna Clarke&apos;s Piranesi
          <br />
          and many more.
        </p>
      </div>
    </div>
  );
}

