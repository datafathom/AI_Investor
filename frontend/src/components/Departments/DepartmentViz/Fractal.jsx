import React, { useRef, useEffect } from 'react';

const Fractal = ({ color = "#dc2626" }) => {
  const canvasRef = useRef(null);
  const animationRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let width = canvas.width = canvas.parentElement.clientWidth;
    let height = canvas.height = canvas.parentElement.clientHeight;
    
    // Julia Set Parameters
    let cX = -0.7;
    let cY = 0.27015;
    let zoom = 1;

    const renderFractal = (time) => {
      // Animate parameters
      const t = time * 0.0005;
      cX = -0.7 + Math.sin(t) * 0.1;
      cY = 0.27015 + Math.cos(t) * 0.1;

      const imageData = ctx.createImageData(width, height);
      const data = imageData.data;

      // Render simplified Julia Set
      for (let x = 0; x < width; x++) {
        for (let y = 0; y < height; y++) {
          let zx = 1.5 * (x - width / 2) / (0.5 * zoom * width);
          let zy = (y - height / 2) / (0.5 * zoom * height);
          
          let i = 0;
          const maxIter = 50; // Keep low for performance
          
          while (zx * zx + zy * zy < 4 && i < maxIter) {
            const temp = zx * zx - zy * zy + cX;
            zy = 2.0 * zx * zy + cY;
            zx = temp;
            i++;
          }

          const offset = (y * width + x) * 4;
          // Map iterations to color
          const intensity = i === maxIter ? 0 : (i / maxIter) * 255;
          
          // Use provided color for tint (simplified hex parse)
          // Defaulting to red-ish scale for stress tester
          data[offset] = intensity;     // R
          data[offset + 1] = 0;         // G
          data[offset + 2] = intensity * 0.2; // B
          data[offset + 3] = 255;       // Alpha
        }
      }

      ctx.putImageData(imageData, 0, 0);
      
      // Overlay
      ctx.fillStyle = "rgba(0,0,0,0.5)";
      ctx.fillRect(0, 0, 150, 60);
      ctx.fillStyle = "#fff";
      ctx.font = "12px monospace";
      ctx.fillText(`CHAOS METRIC: ${(Math.abs(cX) * 100).toFixed(2)}%`, 10, 20);
      ctx.fillText(`ENTROPY: ${(Math.abs(cY) * 100).toFixed(2)}`, 10, 40);

      animationRef.current = requestAnimationFrame(renderFractal);
    };

    animationRef.current = requestAnimationFrame(renderFractal);

    const handleResize = () => {
         if(canvas.parentElement) {
            width = canvas.width = canvas.parentElement.clientWidth;
            height = canvas.height = canvas.parentElement.clientHeight;
         }
    };
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationRef.current);
    };
  }, [color]);

  return (
    <div style={{ width: '100%', height: '100%', minHeight: '400px', position: 'relative', overflow: 'hidden' }}>
      <canvas 
        ref={canvasRef} 
        style={{ width: '100%', height: '100%', display: 'block', background: '#000' }} 
      />
      <div style={{ position: 'absolute', bottom: 20, left: 20, color: '#dc2626', pointerEvents: 'none', textShadow: '0 0 10px black' }}>
        <h4 style={{ margin: 0 }}>SYSTEM FRACTRESS</h4>
        <p style={{ margin: 0, fontSize: '0.8em', opacity: 0.8 }}>Chaos Theory Simulation</p>
      </div>
    </div>
  );
};

export default Fractal;
