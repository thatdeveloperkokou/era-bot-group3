import { useEffect, useRef } from 'react';
import { FaBolt } from 'react-icons/fa';
import './cursor.css';

const ThunderboltCursor = ({ grayscaleSelector = '[data-grayscale-target]' }) => {
  const cursorRef = useRef(null);

  useEffect(() => {
    const cursor = cursorRef.current;
    let grayscaleTarget = null;

    const handleMouseMove = (event) => {
      if (!cursor) return;

      cursor.style.left = `${event.clientX}px`;
      cursor.style.top = `${event.clientY}px`;

      const hoveredElement = document.elementFromPoint(event.clientX, event.clientY);
      const candidate = hoveredElement?.closest(grayscaleSelector);

      if (candidate && candidate !== grayscaleTarget) {
        grayscaleTarget?.classList.remove('cursor-grayscale');
        candidate.classList.add('cursor-grayscale');
        grayscaleTarget = candidate;
      } else if (!candidate && grayscaleTarget) {
        grayscaleTarget.classList.remove('cursor-grayscale');
        grayscaleTarget = null;
      }
    };

    window.addEventListener('mousemove', handleMouseMove);

    return () => {
      grayscaleTarget?.classList.remove('cursor-grayscale');
      window.removeEventListener('mousemove', handleMouseMove);
    };
  }, [grayscaleSelector]);

  return (
    <div ref={cursorRef} className="thunderbolt-cursor" aria-hidden="true">
      <FaBolt />
    </div>
  );
};

export default ThunderboltCursor;

