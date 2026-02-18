'use client';

import { useEffect, useRef, useCallback } from 'react';

interface Point {
  element: HTMLDivElement;
  originalT: number;
  originalRadius: number;
  index: number;
}

export default function Spiral() {
  const containerRef = useRef<HTMLDivElement>(null);
  const stateRef = useRef({
    points: [] as Point[],
    isAnimating: true,
    speed: 0.5,
    rotation: 0,
    characters: ['●', '○', '◉', '◎', '⬢', '⬡', '▲', '△', '■', '□', '◆', '◇'],
    currentCharIndex: 0,
    spiralParams: {
      points: 120,
      maxRadius: 250,
      turns: 6,
      centerX: 300,
      centerY: 300,
    },
  });

  const updatePositions = useCallback(() => {
    const s = stateRef.current;
    s.points.forEach((point) => {
      const t = point.originalT + s.rotation;
      const x = s.spiralParams.centerX + Math.cos(t) * point.originalRadius;
      const y = s.spiralParams.centerY + Math.sin(t) * point.originalRadius;

      const hue = (t * 30 + s.rotation * 50) % 360;
      const saturation = 40 + 20 * Math.sin(t + s.rotation);
      const lightness = 75 + 15 * Math.cos(t * 2 + s.rotation);
      const opacity = 0.7 + 0.3 * Math.sin(t + s.rotation * 2);

      point.element.style.left = x + 'px';
      point.element.style.top = y + 'px';
      point.element.style.color = `hsl(${hue}, ${saturation}%, ${lightness}%)`;
      point.element.style.textShadow = `0 0 8px hsla(${hue}, ${saturation}%, ${lightness}%, 0.6)`;
      point.element.style.opacity = String(opacity);
    });
  }, []);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const s = stateRef.current;

    // Create spiral points
    for (let i = 0; i < s.spiralParams.points; i++) {
      const t = (i / s.spiralParams.points) * s.spiralParams.turns * Math.PI * 2;
      const radius = (i / s.spiralParams.points) * s.spiralParams.maxRadius;

      const point = document.createElement('div');
      point.className = 'spiral-point';
      point.textContent = s.characters[s.currentCharIndex];

      container.appendChild(point);
      s.points.push({ element: point, originalT: t, originalRadius: radius, index: i });
    }

    // Animation loop
    let animId: number;
    const animate = () => {
      if (s.isAnimating) {
        s.rotation += 0.02 * s.speed;
        updatePositions();
      }
      animId = requestAnimationFrame(animate);
    };
    animate();

    // Pause on hover
    const handleEnter = () => { s.isAnimating = false; };
    const handleLeave = () => { s.isAnimating = true; };

    // Click to change character
    const handleClick = () => {
      s.currentCharIndex = (s.currentCharIndex + 1) % s.characters.length;
      s.points.forEach((p) => {
        p.element.textContent = s.characters[s.currentCharIndex];
      });
    };

    // Resize
    const handleResize = () => {
      s.spiralParams.centerX = container.offsetWidth / 2;
      s.spiralParams.centerY = container.offsetHeight / 2;
    };

    container.addEventListener('mouseenter', handleEnter);
    container.addEventListener('mouseleave', handleLeave);
    container.addEventListener('click', handleClick);
    window.addEventListener('resize', handleResize);

    return () => {
      cancelAnimationFrame(animId);
      container.removeEventListener('mouseenter', handleEnter);
      container.removeEventListener('mouseleave', handleLeave);
      container.removeEventListener('click', handleClick);
      window.removeEventListener('resize', handleResize);
    };
  }, [updatePositions]);

  return <div ref={containerRef} className="spiral-container" />;
}

