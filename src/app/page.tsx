import Link from 'next/link';

export default function Home() {
  return (
    <div className="home">
      <div className="intro-text">
        <br /><br /><br />
        hi. i am jade.<br />
        a technologist + builder in san francisco
        <br />
        I&apos;m a{' '}
        <a href="https://www.linkedin.com/in/jade-tseng/?locale=en_US">
          software engineer
        </a>{' '}
        focused on ML infra &amp; platform engineering.
        <br /><br /><br /><br />
        <Link href="/now">now</Link><br />
        <Link href="/library">library</Link><br />
        {/* <Link href="/blog">blog</Link> */}
      </div>
    </div>
  );
}
