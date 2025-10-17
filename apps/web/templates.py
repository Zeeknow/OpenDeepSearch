#!/usr/bin/env python3
"""
HTML Templates for DeFi Assistant
Landing page, feature pages, and components
"""

def get_3d_background_elements():
    """3D Background elements using Vanta.js for reliable animations"""
    return """
  <!-- Vanta.js 3D Background Container -->
  <div id="vanta-container" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; pointer-events: none;"></div>
  
  <!-- Fallback CSS Background Elements -->
  <div class="web3-grid"></div>
  <div class="holographic-overlay"></div>
  <div class="floating-particles">
    <div class="particle" style="left: 10%; animation-delay: 0s;"></div>
    <div class="particle" style="left: 20%; animation-delay: 2s;"></div>
    <div class="particle" style="left: 30%; animation-delay: 4s;"></div>
    <div class="particle" style="left: 40%; animation-delay: 6s;"></div>
    <div class="particle" style="left: 50%; animation-delay: 8s;"></div>
    <div class="particle" style="left: 60%; animation-delay: 10s;"></div>
    <div class="particle" style="left: 70%; animation-delay: 12s;"></div>
    <div class="particle" style="left: 80%; animation-delay: 14s;"></div>
    <div class="particle" style="left: 90%; animation-delay: 16s;"></div>
    <div class="particle" style="left: 15%; animation-delay: 1s;"></div>
    <div class="particle" style="left: 25%; animation-delay: 3s;"></div>
    <div class="particle" style="left: 35%; animation-delay: 5s;"></div>
    <div class="particle" style="left: 45%; animation-delay: 7s;"></div>
    <div class="particle" style="left: 55%; animation-delay: 9s;"></div>
    <div class="particle" style="left: 65%; animation-delay: 11s;"></div>
    <div class="particle" style="left: 75%; animation-delay: 13s;"></div>
    <div class="particle" style="left: 85%; animation-delay: 15s;"></div>
    <div class="particle" style="left: 95%; animation-delay: 17s;"></div>
  </div>
"""

def get_3d_javascript():
    """Universal 3D JavaScript using Vanta.js for reliable animations"""
    return """
  <!-- Vanta.js CDN -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.waves.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.particles.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.net.min.js"></script>
  
  <script>
    // Initialize Vanta.js 3D Background Effects
    function init3DBackground() {{
      console.log('Initializing Vanta.js 3D background...');
      
      // Create a container for Vanta effects
      const vantaContainer = document.getElementById('vanta-container');
      if (!vantaContainer) {{
        console.error('Vanta container not found!');
        return;
      }}
      
      // Initialize Waves effect
      VANTA.WAVES({{
        el: vantaContainer,
        mouseControls: true,
        touchControls: true,
        gyroControls: false,
        minHeight: 200.00,
        minWidth: 200.00,
        scale: 1.00,
        scaleMobile: 1.00,
        color: 0x7c5cff,
        shininess: 50.00,
        waveHeight: 20.00,
        waveSpeed: 0.75,
        zoom: 0.75
      }});
      
      console.log('Vanta.js waves effect initialized!');
    }}
    
    // Alternative: Particles effect
    function initParticlesBackground() {{
      const vantaContainer = document.getElementById('vanta-container');
      if (!vantaContainer) return;
      
      VANTA.PARTICLES({{
        el: vantaContainer,
        mouseControls: true,
        touchControls: true,
        gyroControls: false,
        minHeight: 200.00,
        minWidth: 200.00,
        scale: 1.00,
        scaleMobile: 1.00,
        color: 0x3ec6ff,
        color2: 0x7c5cff,
        size: 1.50,
        spacing: 18.00
      }});
    }}
    
    // Alternative: Net effect
    function initNetBackground() {{
      const vantaContainer = document.getElementById('vanta-container');
      if (!vantaContainer) return;
      
      VANTA.NET({{
        el: vantaContainer,
        mouseControls: true,
        touchControls: true,
        gyroControls: false,
        minHeight: 200.00,
        minWidth: 200.00,
        scale: 1.00,
        scaleMobile: 1.00,
        color: 0x7c5cff,
        backgroundColor: 0x0f1724,
        points: 20.00,
        maxDistance: 25.00,
        spacing: 18.00
      }});
    }}
    
    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', () => {{
      // Try waves effect first
      init3DBackground();
      
      // If waves don't work, try particles
      setTimeout(() => {{
        if (!document.querySelector('.vanta-canvas')) {{
          console.log('Waves failed, trying particles...');
          initParticlesBackground();
        }}
      }}, 1000);
    }});
    
    // Add mouse interaction effects
    document.addEventListener('mousemove', (e) => {{
      const vantaCanvas = document.querySelector('.vanta-canvas');
      if (vantaCanvas) {{
        // Add subtle interaction
        const intensity = Math.min(1, Math.sqrt(e.clientX * e.clientX + e.clientY * e.clientY) / 1000);
        vantaCanvas.style.filter = `brightness(${{1 + intensity * 0.2}})`;
      }}
    }});
  </script>
"""

def get_base_css():
    """Base CSS styles for all pages"""
    return """
:root{
  --bg:#0f1724;
  --card:#0b1220;
  --accent:#7c5cff;
  --accent-2:#3ec6ff;
  --muted:#9aa4b2;
  --glass: rgba(255,255,255,0.04);
  --text:#e6eef8;
  --success:#10b981;
  --warning:#f59e0b;
  --error:#ef4444;
  --shadow-soft: 0 4px 20px rgba(0,0,0,0.1);
  --shadow-medium: 0 8px 40px rgba(0,0,0,0.15);
  --shadow-strong: 0 16px 60px rgba(0,0,0,0.2);
  --gradient-primary: linear-gradient(135deg, var(--accent), var(--accent-2));
  --gradient-secondary: linear-gradient(45deg, rgba(124,92,255,0.1), rgba(62,198,255,0.1));
}
*{box-sizing:border-box}
body{
  margin:0;
  background: 
    radial-gradient(circle at 20% 80%, rgba(124, 92, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(62, 198, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(124, 92, 255, 0.05) 0%, transparent 50%),
    linear-gradient(180deg, #071022 0%, #081126 60%);
  font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
  color:var(--text);
  -webkit-font-smoothing:antialiased;
  -moz-osx-font-smoothing:grayscale;
  min-height:100vh;
  overflow-x: hidden;
  position: relative;
  animation: backgroundShift 20s ease-in-out infinite;
}
@keyframes backgroundShift {
  0%, 100% { background-position: 0% 0%, 100% 100%, 50% 50%; }
  50% { background-position: 100% 100%, 0% 0%, 25% 75%; }
}
/* Enhanced 3D Background System - Web3 Inspired */
.background-canvas {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  pointer-events: none;
}

/* Blockchain Network Visualization */
.blockchain-network {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  pointer-events: none;
  opacity: 0.08;
}
.blockchain-node {
  position: absolute;
  width: 6px;
  height: 6px;
  background: var(--accent);
  border-radius: 50%;
  animation: blockchainPulse 4s ease-in-out infinite;
  box-shadow: 0 0 10px var(--accent);
}
.blockchain-connection {
  position: absolute;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--accent), var(--accent-2), transparent);
  animation: blockchainFlow 6s linear infinite;
  border-radius: 1px;
}
@keyframes blockchainPulse {
  0%, 100% { 
    transform: scale(1);
    box-shadow: 0 0 10px var(--accent);
  }
  50% { 
    transform: scale(1.5);
    box-shadow: 0 0 20px var(--accent), 0 0 30px var(--accent-2);
  }
}
@keyframes blockchainFlow {
  0% { opacity: 0; transform: scaleX(0); }
  50% { opacity: 1; transform: scaleX(1); }
  100% { opacity: 0; transform: scaleX(0); }
}

/* DeFi Geometric Patterns */
.defi-geometry {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  pointer-events: none;
  opacity: 0.06;
}
.geometric-shape {
  position: absolute;
  border: 1px solid var(--accent);
  animation: geometricRotate 20s linear infinite;
}
.hexagon {
  width: 40px;
  height: 40px;
  background: linear-gradient(45deg, transparent, rgba(124, 92, 255, 0.1));
  clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
}
.triangle {
  width: 0;
  height: 0;
  border-left: 20px solid transparent;
  border-right: 20px solid transparent;
  border-bottom: 35px solid rgba(62, 198, 255, 0.1);
}
@keyframes geometricRotate {
  0% { transform: rotate(0deg) scale(1); }
  50% { transform: rotate(180deg) scale(1.2); }
  100% { transform: rotate(360deg) scale(1); }
}

/* Enhanced Floating Particles */
.floating-particles {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  pointer-events: none;
}
.particle {
  position: absolute;
  border-radius: 50%;
  animation: floatParticle 20s linear infinite;
  filter: blur(0.5px);
}
.particle::before {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  border-radius: 50%;
  background: inherit;
  filter: blur(2px);
  opacity: 0.3;
}
@keyframes floatParticle {
  0% { 
    transform: translateY(100vh) translateX(0px) rotate(0deg) scale(0.5);
    opacity: 0;
  }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { 
    transform: translateY(-100px) translateX(200px) rotate(720deg) scale(1.5);
    opacity: 0;
  }
}

/* Web3 Grid System */
.web3-grid {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  pointer-events: none;
  opacity: 0.1;
  background-image: 
    linear-gradient(rgba(124, 92, 255, 0.3) 2px, transparent 2px),
    linear-gradient(90deg, rgba(124, 92, 255, 0.3) 2px, transparent 2px),
    linear-gradient(rgba(62, 198, 255, 0.2) 1px, transparent 1px),
    linear-gradient(90deg, rgba(62, 198, 255, 0.2) 1px, transparent 1px);
  background-size: 50px 50px, 50px 50px, 100px 100px, 100px 100px;
  animation: web3GridMove 20s linear infinite;
}
@keyframes web3GridMove {
  0% { transform: translate(0, 0); }
  100% { transform: translate(50px, 50px); }
}

/* Simple Floating Particles - Guaranteed to Work */
.floating-particles {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  pointer-events: none;
  overflow: hidden;
}

.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: #7c5cff;
  border-radius: 50%;
  animation: floatUp 15s linear infinite;
  opacity: 0.8;
}

.particle:nth-child(2n) {
  background: #3ec6ff;
  animation-duration: 20s;
}

.particle:nth-child(3n) {
  background: #00ff88;
  animation-duration: 25s;
}

@keyframes floatUp {
  0% {
    transform: translateY(100vh) translateX(0px) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(-100px) translateX(100px) rotate(360deg);
    opacity: 0;
  }
}

/* Holographic Overlay Enhanced */
.holographic-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  pointer-events: none;
  background: 
    radial-gradient(circle at 20% 30%, rgba(124, 92, 255, 0.05) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(62, 198, 255, 0.05) 0%, transparent 50%),
    radial-gradient(circle at 50% 50%, rgba(16, 185, 129, 0.03) 0%, transparent 50%),
    radial-gradient(circle at 30% 80%, rgba(245, 158, 11, 0.03) 0%, transparent 50%);
  animation: holographicShift 35s ease-in-out infinite;
}
@keyframes holographicShift {
  0%, 100% { 
    background-position: 0% 0%, 100% 100%, 50% 50%, 30% 80%;
    filter: hue-rotate(0deg) brightness(1);
  }
  25% { 
    background-position: 100% 0%, 0% 100%, 25% 75%, 70% 20%;
    filter: hue-rotate(90deg) brightness(1.1);
  }
  50% { 
    background-position: 100% 100%, 0% 0%, 75% 25%, 20% 70%;
    filter: hue-rotate(180deg) brightness(1.2);
  }
  75% { 
    background-position: 0% 100%, 100% 0%, 75% 75%, 80% 30%;
    filter: hue-rotate(270deg) brightness(1.1);
  }
}

/* Crypto Data Streams */
.crypto-streams {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  pointer-events: none;
  opacity: 0.1;
}
.data-stream {
  position: absolute;
  width: 2px;
  height: 100px;
  background: linear-gradient(180deg, transparent, var(--accent), transparent);
  animation: dataStreamFlow 8s linear infinite;
}
@keyframes dataStreamFlow {
  0% { 
    transform: translateY(-100px) rotate(0deg);
    opacity: 0;
  }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { 
    transform: translateY(100vh) rotate(360deg);
    opacity: 0;
  }
}
.container{
  width:100%;
  max-width:1200px;
  margin:0 auto;
  padding:20px;
}
.navbar{
  background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.02));
  backdrop-filter: blur(20px);
  border-radius:16px;
  padding:20px 28px;
  margin-bottom:32px;
  border:1px solid rgba(255,255,255,0.1);
  display:flex;
  justify-content:space-between;
  align-items:center;
  box-shadow: var(--shadow-medium);
  position: relative;
  overflow: hidden;
  transform: translateZ(0);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.navbar::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
  transition: left 0.5s;
}
.navbar:hover::before {
  left: 100%;
}
.navbar:hover {
  transform: translateY(-2px) translateZ(0);
  box-shadow: var(--shadow-strong);
  border-color: rgba(124, 92, 255, 0.3);
}
.logo{
  display:flex;
  align-items:center;
  gap:12px;
  text-decoration:none;
  color:inherit;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  z-index: 1;
}
.logo:hover {
  transform: scale(1.05) translateZ(0);
}
.logo-icon{
  width:48px;
  height:48px;
  border-radius:12px;
  display:flex;
  align-items:center;
  justify-content:center;
  background: var(--gradient-primary);
  font-weight:700;
  box-shadow: var(--shadow-soft);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  font-size: 20px;
  color: white;
}
.logo-icon::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.3) 50%, transparent 70%);
  transform: translateX(-100%);
  transition: transform 0.6s;
}
.logo:hover .logo-icon::before {
  transform: translateX(100%);
}
.logo:hover .logo-icon {
  transform: rotateY(10deg) rotateX(5deg);
  box-shadow: var(--shadow-medium);
}
.nav-links{
  display:flex;
  gap:20px;
  align-items:center;
}
.nav-link{
  color:var(--muted);
  text-decoration:none;
  padding:12px 20px;
  border-radius:12px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-weight:500;
  position: relative;
  overflow: hidden;
  transform: translateZ(0);
}
.nav-link::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--gradient-primary);
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: inherit;
}
.nav-link:hover::before {
  opacity: 0.1;
}
.nav-link:hover{
  color:var(--text);
  background:rgba(255,255,255,0.08);
  transform: translateY(-2px) translateZ(0);
  box-shadow: var(--shadow-soft);
}
.nav-link.active {
  background: var(--gradient-primary);
  color: white;
  box-shadow: var(--shadow-medium);
}
.card{
  background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.02));
  backdrop-filter: blur(20px);
  border-radius:20px;
  padding:32px;
  margin-bottom:24px;
  border:1px solid rgba(255,255,255,0.1);
  box-shadow: var(--shadow-medium);
  position: relative;
  overflow: hidden;
  transform: translateZ(0);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}
.card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--gradient-secondary);
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: inherit;
}
.card:hover::before {
  opacity: 0.3;
}
.card:hover {
  transform: translateY(-8px) translateZ(0);
  box-shadow: var(--shadow-strong);
  border-color: rgba(124, 92, 255, 0.3);
}
.btn{
  background: var(--gradient-primary);
  border:none;
  color:white;
  padding:16px 28px;
  border-radius:16px;
  font-weight:600;
  cursor:pointer;
  text-decoration:none;
  display:inline-block;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  transform: translateZ(0);
  box-shadow: var(--shadow-soft);
  font-size: 16px;
}
.btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.2) 50%, transparent 70%);
  transform: translateX(-100%);
  transition: transform 0.6s;
}
.btn:hover::before {
  transform: translateX(100%);
}
.btn:hover{
  transform: translateY(-3px) translateZ(0);
  box-shadow: var(--shadow-medium);
}
.btn:active{
  transform: translateY(-1px) translateZ(0);
  box-shadow: var(--shadow-soft);
}
.btn-secondary{
  background:rgba(255,255,255,0.1);
  color:var(--text);
  border: 1px solid rgba(255,255,255,0.2);
}
.btn-secondary:hover{
  background:rgba(255,255,255,0.15);
  border-color: rgba(124, 92, 255, 0.3);
}
.grid{
  display:grid;
  gap:24px;
  margin-bottom:24px;
}
.grid-2{grid-template-columns:repeat(auto-fit, minmax(300px, 1fr))}
.grid-3{grid-template-columns:repeat(auto-fit, minmax(280px, 1fr))}
.grid-4{grid-template-columns:repeat(auto-fit, minmax(250px, 1fr))}
.grid-item {
  background: linear-gradient(135deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
  backdrop-filter: blur(15px);
  border-radius: 16px;
  padding: 24px;
  border: 1px solid rgba(255,255,255,0.08);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  transform: translateZ(0);
}
.grid-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--gradient-secondary);
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: inherit;
}
.grid-item:hover::before {
  opacity: 0.2;
}
.grid-item:hover {
  transform: translateY(-4px) translateZ(0);
  box-shadow: var(--shadow-medium);
  border-color: rgba(124, 92, 255, 0.2);
}
.feature-card{
  background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.02));
  backdrop-filter: blur(20px);
  border-radius:16px;
  padding:24px;
  border:1px solid rgba(255,255,255,0.1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  transform: translateZ(0);
  box-shadow: var(--shadow-soft);
  text-decoration:none;
  color:inherit;
}
.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--gradient-secondary);
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: inherit;
}
.feature-card:hover::before {
  opacity: 0.3;
}
.feature-card:hover{
  transform: translateY(-6px) translateZ(0);
  box-shadow: var(--shadow-medium);
  border-color: rgba(124, 92, 255, 0.3);
}
.feature-icon{
  width:56px;
  height:56px;
  border-radius:16px;
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:28px;
  margin-bottom:20px;
  background: var(--gradient-primary);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-soft);
}
.feature-icon::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.3) 50%, transparent 70%);
  transform: translateX(-100%);
  transition: transform 0.6s;
}
.feature-card:hover .feature-icon::before {
  transform: translateX(100%);
}
.feature-card:hover .feature-icon {
  transform: scale(1.1) rotateY(10deg);
  box-shadow: var(--shadow-medium);
}
.feature-title{
  font-size:18px;
  font-weight:700;
  margin-bottom:8px;
  color:var(--text);
}
.feature-description{
  font-size:14px;
  color:var(--muted);
  line-height:1.5;
}
/* Floating Animation for Cards */
@keyframes float {
  0%, 100% { transform: translateY(0px) translateZ(0); }
  50% { transform: translateY(-10px) translateZ(0); }
}
.floating {
  animation: float 6s ease-in-out infinite;
}
.floating:nth-child(2) {
  animation-delay: -2s;
}
.floating:nth-child(3) {
  animation-delay: -4s;
}
/* Pulse Animation for Interactive Elements */
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}
.pulse {
  animation: pulse 2s ease-in-out infinite;
}
/* Glow Effect */
@keyframes glow {
  0%, 100% { box-shadow: var(--shadow-soft); }
  50% { box-shadow: var(--shadow-medium), 0 0 20px rgba(124, 92, 255, 0.3); }
}
.glow {
  animation: glow 3s ease-in-out infinite;
}
/* Shimmer Effect */
@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}
.shimmer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  animation: shimmer 2s infinite;
}
/* 3D Tilt Effect */
@keyframes tilt {
  0%, 100% { transform: rotateX(0deg) rotateY(0deg); }
  25% { transform: rotateX(5deg) rotateY(5deg); }
  50% { transform: rotateX(0deg) rotateY(10deg); }
  75% { transform: rotateX(-5deg) rotateY(5deg); }
}
.tilt {
  animation: tilt 8s ease-in-out infinite;
}
/* Morphing Background */
@keyframes morph {
  0%, 100% { border-radius: 20px; }
  25% { border-radius: 30px 20px 20px 30px; }
  50% { border-radius: 20px 30px 30px 20px; }
  75% { border-radius: 30px; }
}
.morph {
  animation: morph 10s ease-in-out infinite;
}
/* Snackbar Notifications */
.snackbar {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
  backdrop-filter: blur(20px);
  color: var(--text);
  padding: 16px 24px;
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.1);
  box-shadow: var(--shadow-medium);
  z-index: 1000;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-weight: 500;
  max-width: 300px;
}
.snackbar.show {
  opacity: 1;
  transform: translateY(0);
}
.snackbar.success {
  border-color: rgba(16, 185, 129, 0.3);
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(16, 185, 129, 0.05));
}
.snackbar.warning {
  border-color: rgba(245, 158, 11, 0.3);
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(245, 158, 11, 0.05));
}
.snackbar.error {
  border-color: rgba(239, 68, 68, 0.3);
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(239, 68, 68, 0.05));
}
/* Enhanced Loading States */
.loading-spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255,255,255,0.1);
  border-radius: 50%;
  border-top-color: var(--accent);
  animation: spin 1s ease-in-out infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
/* Interactive Hover Effects */
.interactive-hover {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
}
.interactive-hover:hover {
  transform: translateY(-2px) scale(1.02);
  box-shadow: var(--shadow-medium);
}
/* Glitch Effect for Special Elements */
@keyframes glitch {
  0%, 100% { transform: translate(0); }
  20% { transform: translate(-2px, 2px); }
  40% { transform: translate(-2px, -2px); }
  60% { transform: translate(2px, 2px); }
  80% { transform: translate(2px, -2px); }
}
.glitch {
  animation: glitch 0.3s ease-in-out infinite;
}
.glitch:hover {
  animation: none;
}
.feature-desc{
  color:var(--muted);
  font-size:14px;
  line-height:1.5;
}
.loading{
  text-align:center;
  color:var(--muted);
  padding:20px;
}
.error{
  color:var(--error);
  background:rgba(239,68,68,0.1);
  border:1px solid rgba(239,68,68,0.2);
  padding:12px;
  border-radius:8px;
  margin:10px 0;
}
.success{
  color:var(--success);
  background:rgba(16,185,129,0.1);
  border:1px solid rgba(16,185,129,0.2);
  padding:12px;
  border-radius:8px;
  margin:10px 0;
}
@media (max-width:768px){
  .container{padding:10px}
  .navbar{flex-direction:column;gap:16px}
  .nav-links{flex-wrap:wrap;justify-content:center}
  .grid-2,.grid-3,.grid-4{grid-template-columns:1fr}
}

/* Snackbar notifications */
.snackbar{
  position:fixed;
  left:50%;
  transform:translateX(-50%);
  bottom:26px;
  background:var(--accent);
  color:white;
  padding:12px 20px;
  border-radius:8px;
  box-shadow:0 8px 30px rgba(2,6,23,0.6);
  z-index:9999;
  opacity:0;
  animation:slideUp .3s forwards;
}
@keyframes slideUp{
  from{transform:translateX(-50%) translateY(20px);opacity:0}
  to{transform:translateX(-50%) translateY(0);opacity:1}
}
.snackbar.warning{background:var(--warning)}
.snackbar.error{background:var(--error)}
.snackbar.success{background:var(--success)}

/* Hackathon Showcase Styles */
.hackathon-feature{{
  background:rgba(255,255,255,0.02);
  border:1px solid rgba(255,255,255,0.05);
  border-radius:12px;
  padding:24px;
  text-align:center;
  transition:all 0.3s ease;
  position:relative;
  overflow:hidden;
}}
.hackathon-feature:hover{{
  transform:translateY(-4px);
  border-color:rgba(124,92,255,0.3);
  box-shadow:0 8px 32px rgba(124,92,255,0.1);
}}
.hackathon-feature::before{{
  content:'';
  position:absolute;
  top:0;
  left:0;
  right:0;
  height:2px;
  background:linear-gradient(90deg,var(--accent),var(--accent-2));
  opacity:0;
  transition:opacity 0.3s ease;
}}
.hackathon-feature:hover::before{{
  opacity:1;
}}
.hackathon-icon{{
  font-size:48px;
  margin-bottom:16px;
  display:block;
}}
.hackathon-feature h3{{
  margin:0 0 12px 0;
  color:var(--text);
  font-size:18px;
  font-weight:600;
}}
.hackathon-feature p{{
  margin:0 0 16px 0;
  color:var(--muted);
  font-size:14px;
  line-height:1.5;
}}
.tech-badge{{
  display:inline-block;
  background:linear-gradient(135deg,var(--accent),var(--accent-2));
  color:white;
  padding:6px 12px;
  border-radius:20px;
  font-size:12px;
  font-weight:600;
  text-transform:uppercase;
  letter-spacing:0.5px;
}}
.innovation-badge{{
  display:inline-block;
  background:rgba(124,92,255,0.1);
  color:var(--accent);
  padding:8px 16px;
  border-radius:20px;
  font-size:14px;
  font-weight:500;
  border:1px solid rgba(124,92,255,0.2);
}}
"""

def get_landing_page():
    """Landing page HTML"""
    return f"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Safe DeFi Assistant - Your DeFi Safety Companion</title>
<style>{get_base_css()}</style>
</head>
<body>
{get_3d_background_elements()}
  <div class="container">
    <nav class="navbar">
      <a href="/" class="logo">
        <div class="logo-icon">DF</div>
        <div>
          <div style="font-size:20px;font-weight:700">Safe DeFi Assistant</div>
          <div style="font-size:12px;color:var(--muted)">DeFi Safety & Intelligence</div>
        </div>
      </a>
      <div class="nav-links">
            <a href="/" class="nav-link active">Home</a>
            <a href="/chat" class="nav-link">AI Assistant</a>
            <a href="/gas-prices" class="nav-link">Gas Prices</a>
            <a href="/market-data" class="nav-link">Market Data</a>
            <a href="/risk-analysis" class="nav-link">Risk Analysis</a>
            <a href="/portfolio" class="nav-link">Portfolio</a>
            <a href="/yield-farming" class="nav-link">Yield Farming</a>
      </div>
    </nav>

    <div class="card" style="text-align:center;padding:40px">
      <h1 style="font-size:48px;margin:0 0 16px 0;background:linear-gradient(135deg,var(--accent),var(--accent-2));-webkit-background-clip:text;-webkit-text-fill-color:transparent">
        Safe DeFi Assistant
      </h1>
      <p style="font-size:20px;color:var(--muted);margin:0 0 32px 0;max-width:600px;margin-left:auto;margin-right:auto">
        Your comprehensive DeFi safety companion with real-time market data, risk analysis, and AI-powered insights
      </p>
      <div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap">
        <a href="/chat" class="btn">Start Chatting</a>
        <a href="/market-data" class="btn btn-secondary">View Market Data</a>
      </div>
    </div>

    <div class="grid grid-3">
      <a href="/gas-prices" class="feature-card">
        <div class="feature-icon">⛽</div>
        <div class="feature-title">Real-Time Gas Prices</div>
        <div class="feature-desc">
          Monitor Ethereum, Polygon, and Arbitrum gas prices in real-time. Get optimal transaction timing recommendations.
        </div>
      </a>
      
      <a href="/market-data" class="feature-card">
        <div class="feature-icon">📈</div>
        <div class="feature-title">DeFi Market Data</div>
        <div class="feature-desc">
          Track TVL changes, protocol performance, and market trends across major DeFi protocols.
        </div>
      </a>
      
      <a href="/risk-analysis" class="feature-card">
        <div class="feature-icon">🔍</div>
        <div class="feature-title">Risk Analysis</div>
        <div class="feature-desc">
          Comprehensive risk assessments for DeFi protocols including smart contract audits and safety scores.
        </div>
      </a>
      
      <a href="/yield-farming" class="feature-card">
        <div class="feature-icon">🌾</div>
        <div class="feature-title">Yield Opportunities</div>
        <div class="feature-desc">
          Discover high-yield farming opportunities with risk-adjusted returns and safety recommendations.
        </div>
      </a>
      
      <a href="/chat" class="feature-card">
        <div class="feature-icon">🤖</div>
        <div class="feature-title">AI Assistant</div>
        <div class="feature-desc">
          Chat with our AI-powered assistant for personalized DeFi advice and real-time market insights.
        </div>
      </a>
      
      <a href="/portfolio" class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Portfolio Analysis</div>
        <div class="feature-desc">
          Analyze your DeFi portfolio performance, risks, and optimization opportunities.
        </div>
      </a>
    </div>

    <div class="card">
      <h2 style="margin-top:0">Why Choose Safe DeFi Assistant?</h2>
      <div class="grid grid-2">
        <div>
          <h3>🛡️ Safety First</h3>
          <p>Comprehensive risk analysis and safety recommendations for all major DeFi protocols.</p>
        </div>
        <div>
          <h3>⚡ Real-Time Data</h3>
          <p>Live market data, gas prices, and yield opportunities updated every 30 seconds.</p>
        </div>
        <div>
          <h3>🤖 AI-Powered</h3>
          <p>Advanced AI assistant with access to current web data for accurate, up-to-date advice.</p>
        </div>
        <div>
          <h3>🔍 Multi-Chain</h3>
          <p>Support for Ethereum, Polygon, Arbitrum, and other major DeFi ecosystems.</p>
        </div>
      </div>
    </div>

    <!-- Hackathon Showcase Section -->
    <div class="card" style="background: linear-gradient(135deg, rgba(124, 92, 255, 0.1), rgba(62, 198, 255, 0.1)); border: 1px solid rgba(124, 92, 255, 0.2);">
      <div style="text-align: center; margin-bottom: 32px;">
        <h2 style="margin-top: 0; background: linear-gradient(135deg, var(--accent), var(--accent-2)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
          🏆 Built for Sentient Builder Program
        </h2>
        <p style="font-size: 18px; color: var(--muted); max-width: 600px; margin: 0 auto;">
          Powered by cutting-edge AI technologies and built specifically for the Sentient ecosystem
        </p>
      </div>

      <div class="grid grid-3">
        <div class="hackathon-feature floating shimmer">
          <div class="hackathon-icon">🧠</div>
          <h3>OpenDeepSearch Integration</h3>
          <p>Advanced semantic search and reasoning capabilities powered by OpenDeepSearch for intelligent DeFi analysis and real-time web data processing.</p>
          <div class="tech-badge">OpenDeepSearch</div>
        </div>

        <div class="hackathon-feature floating shimmer">
          <div class="hackathon-icon">🤖</div>
          <h3>Sentient AI Platform</h3>
          <p>Full compatibility with Sentient's AI platform, featuring agent metadata, query processing, and seamless integration with the Sentient ecosystem.</p>
          <div class="tech-badge">Sentient AI</div>
        </div>

        <div class="hackathon-feature floating shimmer">
          <div class="hackathon-icon">🔍</div>
          <h3>Advanced Reranking</h3>
          <p>State-of-the-art semantic reranking using Jina AI for precise information retrieval and context-aware responses in DeFi queries.</p>
          <div class="tech-badge">Jina AI</div>
        </div>

        <div class="hackathon-feature floating shimmer">
          <div class="hackathon-icon">⚡</div>
          <h3>LiteLLM Integration</h3>
          <p>Efficient AI model integration with LiteLLM, supporting multiple model providers and optimized for DeFi-specific reasoning tasks.</p>
          <div class="tech-badge">LiteLLM</div>
        </div>

        <div class="hackathon-feature floating shimmer">
          <div class="hackathon-icon">🌐</div>
          <h3>Real-Time Web Data</h3>
          <p>Live web scraping and data processing using Crawl4AI for up-to-date market information, protocol updates, and DeFi intelligence.</p>
          <div class="tech-badge">Crawl4AI</div>
        </div>

        <div class="hackathon-feature floating shimmer">
          <div class="hackathon-icon">🛡️</div>
          <h3>MEV Protection</h3>
          <p>Advanced MEV detection and protection strategies, leveraging real-time blockchain data for sandwich attack prevention and transaction safety.</p>
          <div class="tech-badge">MEV Shield</div>
        </div>
      </div>

      <div style="text-align: center; margin-top: 32px; padding: 20px; background: rgba(255, 255, 255, 0.02); border-radius: 12px;">
        <h3 style="margin-top: 0; color: var(--accent);">🚀 Hackathon Innovation</h3>
        <p style="margin-bottom: 16px; color: var(--muted);">
          This DeFi Assistant demonstrates the power of combining Sentient's AI platform with real-world DeFi applications, 
          showcasing how AI can democratize access to complex financial analysis and risk management.
        </p>
        <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
          <span class="innovation-badge">AI-Powered Analysis</span>
          <span class="innovation-badge">Real-Time Data</span>
          <span class="innovation-badge">Risk Management</span>
          <span class="innovation-badge">User Safety</span>
        </div>
      </div>
    </div>
  </div>

  <script>
    function showComingSoon(feature) {{
      showSnackbar('🚧 ' + feature + ' is coming soon!', 'warning');
    }}

    function showSnackbar(message, type = 'info') {{
      const snackbar = document.createElement('div');
      snackbar.className = 'snackbar ' + type;
      snackbar.textContent = message;
      document.body.appendChild(snackbar);
      
      // Trigger animation
      setTimeout(() => snackbar.classList.add('show'), 10);
      
      setTimeout(() => {{
        snackbar.classList.remove('show');
        setTimeout(() => snackbar.remove(), 300);
      }}, 3000);
    }}
  </script>
{get_3d_javascript()}
</body>
</html>
"""

def get_gas_prices_page():
    """Gas prices page HTML"""
    return f"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Gas Prices - Safe DeFi Assistant</title>
<style>{get_base_css()}</style>
</head>
<body>
{get_3d_background_elements()}
  <div class="container">
    <nav class="navbar">
      <a href="/" class="logo">
        <div class="logo-icon">DF</div>
        <div>
          <div style="font-size:20px;font-weight:700">Safe DeFi Assistant</div>
          <div style="font-size:12px;color:var(--muted)">Gas Price Monitor</div>
        </div>
      </a>
      <div class="nav-links">
            <a href="/" class="nav-link">Home</a>
            <a href="/chat" class="nav-link">AI Assistant</a>
            <a href="/gas-prices" class="nav-link active">Gas Prices</a>
            <a href="/market-data" class="nav-link">Market Data</a>
            <a href="/risk-analysis" class="nav-link">Risk Analysis</a>
            <a href="/portfolio" class="nav-link">Portfolio</a>
            <a href="/yield-farming" class="nav-link">Yield Farming</a>
      </div>
    </nav>

    <div class="card">
      <h1 style="margin-top:0">⛽ Real-Time Gas Prices</h1>
      <p>Monitor gas prices across multiple networks and get optimal transaction timing recommendations.</p>
      
      <div id="gas-data" class="loading">
        Loading gas price data...
      </div>
      
      <div style="margin-top:20px">
        <button class="btn" onclick="refreshGasPrices()">🔄 Refresh Data</button>
        <button class="btn btn-secondary" onclick="setAutoRefresh()">⏰ Auto Refresh</button>
      </div>
    </div>

    <div class="card">
      <h2>Gas Price Tips</h2>
      <div class="grid grid-2">
        <div>
          <h3>🕐 Best Times to Transact</h3>
          <ul>
            <li>Early morning (UTC): 6-10 AM</li>
            <li>Weekend mornings</li>
            <li>Avoid peak hours: 2-6 PM UTC</li>
          </ul>
        </div>
        <div>
          <h3>💰 Cost Optimization</h3>
          <ul>
            <li>Use Layer 2 solutions (Polygon, Arbitrum)</li>
            <li>Batch multiple transactions</li>
            <li>Monitor gas price trends</li>
          </ul>
        </div>
      </div>
    </div>
  </div>

  <script>
    async function fetchGasPrices() {{
      try {{
        const response = await fetch('/api/gas-prices');
        const data = await response.json();
        return data.success ? data.data : null;
      }} catch (error) {{
        console.error('Error fetching gas prices:', error);
        return null;
      }}
    }}

    function updateGasDisplay(data) {{
      const container = document.getElementById('gas-data');
      if (!data) {{
        container.innerHTML = '<div class="error">Failed to load gas price data</div>';
        return;
      }}
      
      const eth = data.ethereum;
      let html = '<div class="grid grid-2">';
      html += '<div class="card"><h3>Ethereum Gas Prices</h3>';
      html += '<div style="display:flex;justify-content:space-between;margin:8px 0"><span>Slow</span><span style="font-weight:600">' + eth.slow + ' Gwei</span></div>';
      html += '<div style="display:flex;justify-content:space-between;margin:8px 0"><span>Standard</span><span style="font-weight:600">' + eth.standard + ' Gwei</span></div>';
      html += '<div style="display:flex;justify-content:space-between;margin:8px 0"><span>Fast</span><span style="font-weight:600">' + eth.fast + ' Gwei</span></div>';
      html += '<div style="display:flex;justify-content:space-between;margin:8px 0"><span>Instant</span><span style="font-weight:600">' + Math.round(eth.instant) + ' Gwei</span></div>';
      html += '</div>';
      
      html += '<div class="card"><h3>Last Updated</h3>';
      html += '<p>' + new Date(data.last_updated).toLocaleString() + '</p>';
      html += '<p>Sources: ' + data.sources.join(', ') + '</p>';
      html += '</div>';
      html += '</div>';
      
      container.innerHTML = html;
    }}

    async function refreshGasPrices() {{
      const data = await fetchGasPrices();
      updateGasDisplay(data);
    }}

    function setAutoRefresh() {{
      setInterval(refreshGasPrices, 30000);
      alert('Auto-refresh enabled! Gas prices will update every 30 seconds.');
    }}

    // Initial load
    window.addEventListener('load', refreshGasPrices);
  </script>
</body>
</html>
"""

def get_market_data_page():
    """Market data page HTML"""
    return f"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Market Data - Safe DeFi Assistant</title>
<style>{get_base_css()}</style>
</head>
<body>
{get_3d_background_elements()}
  <div class="container">
    <nav class="navbar">
      <a href="/" class="logo">
        <div class="logo-icon">DF</div>
        <div>
          <div style="font-size:20px;font-weight:700">Safe DeFi Assistant</div>
          <div style="font-size:12px;color:var(--muted)">Market Intelligence</div>
        </div>
      </a>
      <div class="nav-links">
            <a href="/" class="nav-link">Home</a>
            <a href="/chat" class="nav-link">AI Assistant</a>
            <a href="/gas-prices" class="nav-link">Gas Prices</a>
            <a href="/market-data" class="nav-link active">Market Data</a>
            <a href="/risk-analysis" class="nav-link">Risk Analysis</a>
            <a href="/portfolio" class="nav-link">Portfolio</a>
            <a href="/yield-farming" class="nav-link">Yield Farming</a>
      </div>
    </nav>

    <div class="card">
      <h1 style="margin-top:0">📈 DeFi Market Data</h1>
      <p>Real-time TVL tracking, protocol performance, and market trends.</p>
      
      <div id="market-data" class="loading">
        Loading market data...
      </div>
      
      <div style="margin-top:20px">
        <button class="btn" onclick="refreshMarketData()">🔄 Refresh All Data</button>
        <button class="btn btn-secondary" onclick="toggleAutoRefresh()">⏰ Auto Refresh</button>
      </div>
    </div>

    <div class="grid grid-2">
      <div class="card">
        <h2>📊 Protocol TVL Rankings</h2>
        <div id="tvl-data" class="loading">Loading TVL data...</div>
      </div>
      
      <div class="card">
        <h2>🌾 Top Yield Opportunities</h2>
        <div id="yield-data" class="loading">Loading yield data...</div>
      </div>
    </div>
  </div>

  <script>
    let autoRefreshInterval = null;

    async function fetchMarketData() {{
      try {{
        const response = await fetch('/api/market-data');
        const data = await response.json();
        return data.success ? data.data : null;
      }} catch (error) {{
        console.error('Error fetching market data:', error);
        return null;
      }}
    }}

    function updateMarketDisplay(data) {{
      if (!data) {{
        document.getElementById('market-data').innerHTML = '<div class="error">Failed to load market data</div>';
        return;
      }}
      
      let html = '<div class="grid grid-3">';
      html += '<div class="card"><h3>Total DeFi TVL</h3><p style="font-size:24px;font-weight:700">$' + (data.tvl_data.total_tvl / 1e9).toFixed(1) + 'B</p></div>';
      html += '<div class="card"><h3>Gas Prices</h3><p style="font-size:24px;font-weight:700">' + data.gas_prices.ethereum.standard + ' Gwei</p></div>';
      html += '<div class="card"><h3>Top Yields</h3><p style="font-size:24px;font-weight:700">' + (data.yield_opportunities.top_yields[0]?.apy || 0) + '% APY</p></div>';
      html += '</div>';
      
      document.getElementById('market-data').innerHTML = html;
    }}

    function updateTVLDisplay(data) {{
      const container = document.getElementById('tvl-data');
      if (!data || !data.protocols) {{
        container.innerHTML = '<div class="error">Failed to load TVL data</div>';
        return;
      }}
      
      let html = '';
      const protocols = Object.values(data.protocols).slice(0, 5);
      protocols.forEach(protocol => {{
        const change = protocol.change_1d > 0 ? '+' : '';
        const changeColor = protocol.change_1d > 0 ? 'var(--success)' : 'var(--error)';
        html += '<div style="display:flex;justify-content:space-between;margin:8px 0;padding:8px;background:rgba(255,255,255,0.02);border-radius:6px">';
        html += '<span>' + protocol.name + '</span>';
        html += '<div style="text-align:right">';
        html += '<div style="font-weight:600">$' + (protocol.tvl/1e9).toFixed(1) + 'B</div>';
        html += '<div style="font-size:12px;color:' + changeColor + '">' + change + protocol.change_1d.toFixed(1) + '%</div>';
        html += '</div></div>';
      }});
      
      container.innerHTML = html;
    }}

    function updateYieldDisplay(data) {{
      const container = document.getElementById('yield-data');
      if (!data || !data.top_yields) {{
        container.innerHTML = '<div class="error">Failed to load yield data</div>';
        return;
      }}
      
      let html = '';
      data.top_yields.slice(0, 5).forEach(yield => {{
        html += '<div style="display:flex;justify-content:space-between;margin:8px 0;padding:8px;background:rgba(255,255,255,0.02);border-radius:6px">';
        html += '<span>' + yield.protocol + '</span>';
        html += '<div style="text-align:right">';
        html += '<div style="font-weight:600;color:var(--success)">' + yield.apy + '% APY</div>';
        html += '<div style="font-size:12px;color:var(--muted)">$' + (yield.tvl/1e6).toFixed(1) + 'M TVL</div>';
        html += '</div></div>';
      }});
      
      container.innerHTML = html;
    }}

    async function refreshMarketData() {{
      const data = await fetchMarketData();
      updateMarketDisplay(data);
      if (data) {{
        updateTVLDisplay(data.tvl_data);
        updateYieldDisplay(data.yield_opportunities);
      }}
    }}

    function toggleAutoRefresh() {{
      if (autoRefreshInterval) {{
        clearInterval(autoRefreshInterval);
        autoRefreshInterval = null;
        alert('Auto-refresh disabled');
      }} else {{
        autoRefreshInterval = setInterval(refreshMarketData, 30000);
        alert('Auto-refresh enabled! Data will update every 30 seconds.');
      }}
    }}

    // Initial load
    window.addEventListener('load', refreshMarketData);
  </script>
</body>
</html>
"""

def get_chat_page():
    """Chat page HTML"""
    return f"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>AI Assistant - Safe DeFi Assistant</title>
<style>{get_base_css()}
.chat-container{{
  display:grid;
  grid-template-columns:300px 1fr;
  gap:20px;
  height:70vh;
}}
.chat-sidebar{{
  background:var(--glass);
  border-radius:12px;
  padding:20px;
  border:1px solid rgba(255,255,255,0.03);
  overflow-y:auto;
}}
.chat-main{{
  background:var(--glass);
  border-radius:12px;
  border:1px solid rgba(255,255,255,0.03);
  display:flex;
  flex-direction:column;
}}
.chat-messages{{
  flex:1;
  padding:20px;
  overflow-y:auto;
  display:flex;
  flex-direction:column;
  gap:12px;
}}
.chat-input{{
  padding:20px;
  border-top:1px solid rgba(255,255,255,0.03);
  display:flex;
  gap:12px;
}}
.chat-input input{{
  flex:1;
  background:rgba(255,255,255,0.05);
  border:1px solid rgba(255,255,255,0.1);
  border-radius:8px;
  padding:12px;
  color:inherit;
  font-size:14px;
}}
.chat-input input:focus{{
  outline:none;
  border-color:var(--accent);
}}
.message{{
  max-width:80%;
  padding:12px 16px;
  border-radius:12px;
  word-wrap:break-word;
}}
.message.user{{
  margin-left:auto;
  background:linear-gradient(135deg,var(--accent),var(--accent-2));
  color:white;
}}
.message.bot{{
  margin-right:auto;
  background:rgba(255,255,255,0.05);
  border:1px solid rgba(255,255,255,0.1);
}}
.quick-action{{
  background:rgba(255,255,255,0.05);
  border:1px solid rgba(255,255,255,0.1);
  border-radius:8px;
  padding:12px;
  margin-bottom:8px;
  cursor:pointer;
  transition:background 0.2s ease;
}}
.quick-action:hover{{
  background:rgba(255,255,255,0.1);
}}
@media (max-width:768px){{
  .chat-container{{grid-template-columns:1fr}}
  .chat-sidebar{{display:none}}
}}
</style>
</head>
<body>
{get_3d_background_elements()}
  <div class="container">
    <nav class="navbar">
      <a href="/" class="logo">
        <div class="logo-icon">DF</div>
        <div>
          <div style="font-size:20px;font-weight:700">Safe DeFi Assistant</div>
          <div style="font-size:12px;color:var(--muted)">AI Chat Assistant</div>
        </div>
      </a>
      <div class="nav-links">
            <a href="/" class="nav-link">Home</a>
            <a href="/chat" class="nav-link active">AI Assistant</a>
            <a href="/gas-prices" class="nav-link">Gas Prices</a>
            <a href="/market-data" class="nav-link">Market Data</a>
            <a href="/risk-analysis" class="nav-link">Risk Analysis</a>
            <a href="/portfolio" class="nav-link">Portfolio</a>
            <a href="/yield-farming" class="nav-link">Yield Farming</a>
      </div>
    </nav>

    <div class="chat-container">
      <div class="chat-sidebar">
        <h3 style="margin-top:0">Quick Actions</h3>
        <div class="quick-action" onclick="askQuestion('What are current gas prices?')">
          ⛽ Gas Prices
        </div>
        <div class="quick-action" onclick="askQuestion('What are the risks of using Aave?')">
          🔍 Aave Risks
        </div>
        <div class="quick-action" onclick="askQuestion('Is Uniswap safe to use?')">
          🦄 Uniswap Safety
        </div>
        <div class="quick-action" onclick="askQuestion('Analyze staking 100 USDC on Compound')">
          📊 DeFi Analysis
        </div>
        
        <h3 style="margin-top:24px">Live Data</h3>
        <div id="live-gas" class="loading">Loading gas data...</div>
        <div id="live-tvl" class="loading">Loading TVL data...</div>
      </div>
      
      <div class="chat-main">
        <div class="chat-messages" id="chat-messages">
          <div class="message bot">
            <strong>👋 Welcome!</strong><br>
            I'm your Safe DeFi Assistant. Ask me about gas prices, protocol risks, yield farming opportunities, or any DeFi-related questions!
          </div>
        </div>
        
        <div class="chat-input">
          <input type="text" id="message-input" placeholder="Ask about DeFi..." onkeydown="handleKey(event)">
          <button class="btn" onclick="sendMessage()">Send</button>
        </div>
      </div>
    </div>
  </div>

  <script>
    function markdownToHtml(text) {{
      return text
        .replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>')
        .replace(/\\*(.*?)\\*/g, '<em>$1</em>')
        .replace(/`(.*?)`/g, '<code>$1</code>')
        .replace(/\\n/g, '<br>');
    }}

    function addMessage(text, type) {{
      const container = document.getElementById('chat-messages');
      const message = document.createElement('div');
      message.className = 'message ' + type;
      message.innerHTML = markdownToHtml(text);
      container.appendChild(message);
      container.scrollTop = container.scrollHeight;
    }}

    function askQuestion(question) {{
      document.getElementById('message-input').value = question;
      sendMessage();
    }}

    function handleKey(e) {{
      if (e.key === 'Enter') sendMessage();
    }}

    async function sendMessage() {{
      const input = document.getElementById('message-input');
      const text = input.value.trim();
      if (!text) return;

      addMessage('<strong>You:</strong><br>' + text, 'user');
      input.value = '';

      // Show loading
      const loadingMsg = document.createElement('div');
      loadingMsg.className = 'message bot';
      loadingMsg.innerHTML = '<strong>Assistant:</strong><br>Thinking...';
      document.getElementById('chat-messages').appendChild(loadingMsg);

      try {{
        const response = await fetch('/api/chat', {{
          method: 'POST',
          headers: {{'Content-Type': 'application/json'}},
          body: JSON.stringify({{message: text}})
        }});

        const data = await response.json();
        loadingMsg.remove();

        if (data.success) {{
          addMessage('<strong>Assistant:</strong><br>' + data.response, 'bot');
        }} else {{
          addMessage('<strong>Error:</strong><br>' + (data.error || 'Something went wrong'), 'bot');
        }}
      }} catch (error) {{
        loadingMsg.remove();
        addMessage('<strong>Error:</strong><br>Network error: ' + error.message, 'bot');
      }}
    }}

    // Load live data
    async function loadLiveData() {{
      try {{
        const response = await fetch('/api/market-data');
        const data = await response.json();
        if (data.success) {{
          const gas = data.data.gas_prices.ethereum;
          const tvl = data.data.tvl_data.total_tvl;
          document.getElementById('live-gas').innerHTML = '⛽ ETH: ' + gas.standard + ' Gwei';
          document.getElementById('live-tvl').innerHTML = '📈 TVL: $' + (tvl/1e9).toFixed(1) + 'B';
        }}
      }} catch (error) {{
        console.error('Error loading live data:', error);
      }}
    }}

    // Auto-refresh live data
    setInterval(loadLiveData, 30000);
    window.addEventListener('load', loadLiveData);
  </script>
{get_3d_javascript()}
</body>
</html>
"""

def get_portfolio_page():
    return f"""
    <!doctype html>
    <html lang="en">
    <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>Portfolio Analysis - Safe DeFi Assistant</title>
    <style>{get_base_css()}
    .portfolio-container {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 20px;
    }}
    .wallet-input {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 20px;
    }}
    .wallet-input input {{
      width: 100%;
      padding: 12px;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: var(--bg);
      color: var(--text);
      font-size: 14px;
    }}
    .wallet-input button {{
      margin-top: 10px;
      width: 100%;
    }}
    .analysis-result {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px;
      margin-top: 20px;
      display: none;
    }}
    .risk-score {{
      display: inline-block;
      padding: 8px 16px;
      border-radius: 20px;
      font-weight: 700;
      font-size: 18px;
    }}
    .risk-low {{ background: #10b981; color: white; }}
    .risk-medium {{ background: #f59e0b; color: white; }}
    .risk-high {{ background: #ef4444; color: white; }}
    .positions-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 15px;
      margin: 20px 0;
    }}
    .position-card {{
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 15px;
    }}
    .position-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }}
    .protocol-name {{
      font-weight: 700;
      color: var(--primary);
    }}
    .position-value {{
      font-weight: 700;
      color: var(--text);
    }}
    .risk-factors, .recommendations {{
      margin: 15px 0;
    }}
    .risk-factors ul, .recommendations ul {{
      margin: 10px 0;
      padding-left: 20px;
    }}
    .risk-factors li, .recommendations li {{
      margin: 5px 0;
      color: var(--text-secondary);
    }}
    </style>
    </head>
    <body>
{get_3d_background_elements()}
      <div class="container">
        <nav class="navbar">
          <a href="/" class="logo">
            <div class="logo-icon">DF</div>
            <div>
              <div style="font-size:20px;font-weight:700">Safe DeFi Assistant</div>
              <div style="font-size:12px;color:var(--muted)">Portfolio Analysis</div>
            </div>
          </a>
          <div class="nav-links">
            <a href="/" class="nav-link">Home</a>
            <a href="/chat" class="nav-link">AI Assistant</a>
            <a href="/gas-prices" class="nav-link">Gas Prices</a>
            <a href="/market-data" class="nav-link">Market Data</a>
            <a href="/risk-analysis" class="nav-link">Risk Analysis</a>
            <a href="/portfolio" class="nav-link active">Portfolio</a>
            <a href="/yield-farming" class="nav-link">Yield Farming</a>
          </div>
        </nav>
        
        <div class="portfolio-container">
          <div class="page-header">
            <h1>📊 Portfolio Risk Analysis</h1>
            <p>Analyze your DeFi portfolio for risks and get personalized recommendations</p>
          </div>
          
          <div class="wallet-input">
            <h3>Enter Wallet Address</h3>
            <input type="text" id="walletInput" placeholder="0x1234567890123456789012345678901234567890" />
            <button class="btn-primary" onclick="analyzePortfolio()">Analyze Portfolio</button>
          </div>
          
          <div id="loadingIndicator" style="display: none; text-align: center; padding: 40px;">
            <div style="font-size: 18px;">🔍 Analyzing portfolio...</div>
            <div style="color: var(--muted); margin-top: 10px;">This may take a few moments</div>
          </div>
          
          <div id="analysisResult" class="analysis-result">
            <div class="analysis-header">
              <h2>📈 Portfolio Analysis Results</h2>
              <div id="riskScore" class="risk-score"></div>
            </div>
            
            <div class="portfolio-summary">
              <h3>💰 Portfolio Summary</h3>
              <div id="portfolioSummary"></div>
            </div>
            
            <div class="positions-section">
              <h3>📋 Positions</h3>
              <div id="positionsGrid" class="positions-grid"></div>
            </div>
            
            <div class="risk-factors">
              <h3>⚠️ Risk Factors</h3>
              <ul id="riskFactorsList"></ul>
            </div>
            
            <div class="recommendations">
              <h3>💡 Recommendations</h3>
              <ul id="recommendationsList"></ul>
            </div>
          </div>
        </div>
      </div>
      
      <script>
        async function analyzePortfolio() {{
          const walletInput = document.getElementById('walletInput');
          const walletAddress = walletInput.value.trim();
          
          if (!walletAddress) {{
            showSnackbar('Please enter a wallet address', 'error');
            return;
          }}
          
          if (!walletAddress.startsWith('0x') || walletAddress.length !== 42) {{
            showSnackbar('Please enter a valid Ethereum address', 'error');
            return;
          }}
          
          // Show loading indicator
          document.getElementById('loadingIndicator').style.display = 'block';
          document.getElementById('analysisResult').style.display = 'none';
          
          try {{
            const response = await fetch(`/api/portfolio/analyze?wallet=${{walletAddress}}`);
            const data = await response.json();
            
            if (data.success) {{
              displayAnalysisResults(data.data);
            }} else {{
              showSnackbar('Analysis failed: ' + data.error, 'error');
            }}
          }} catch (error) {{
            showSnackbar('Error analyzing portfolio: ' + error.message, 'error');
          }} finally {{
            document.getElementById('loadingIndicator').style.display = 'none';
          }}
        }}
        
        function displayAnalysisResults(data) {{
          // Show results
          document.getElementById('analysisResult').style.display = 'block';
          
          // Risk score
          const riskScore = document.getElementById('riskScore');
          const score = data.risk_score;
          riskScore.textContent = `Risk Score: ${{score}}/10`;
          riskScore.className = 'risk-score ' + (score <= 3 ? 'risk-low' : score <= 7 ? 'risk-medium' : 'risk-high');
          
          // Portfolio summary
          document.getElementById('portfolioSummary').innerHTML = `
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 15px 0;">
              <div style="background: var(--bg); padding: 15px; border-radius: 8px; text-align: center;">
                <div style="font-size: 24px; font-weight: 700; color: var(--primary);">$${{data.total_value.toLocaleString()}}</div>
                <div style="color: var(--muted);">Total Value</div>
              </div>
              <div style="background: var(--bg); padding: 15px; border-radius: 8px; text-align: center;">
                <div style="font-size: 24px; font-weight: 700; color: var(--primary);">${{data.positions.length}}</div>
                <div style="color: var(--muted);">Positions</div>
              </div>
              <div style="background: var(--bg); padding: 15px; border-radius: 8px; text-align: center;">
                <div style="font-size: 24px; font-weight: 700; color: var(--primary);">${{data.liquidation_risks.length}}</div>
                <div style="color: var(--muted);">Liquidation Risks</div>
              </div>
            </div>
          `;
          
          // Positions
          const positionsGrid = document.getElementById('positionsGrid');
          positionsGrid.innerHTML = data.positions.map(pos => `
            <div class="position-card">
              <div class="position-header">
                <div class="protocol-name">${{pos.protocol}}</div>
                <div class="position-value">$${{pos.value_usd}}</div>
              </div>
              <div style="color: var(--text-secondary); margin-bottom: 10px;">${{pos.token}}</div>
              <div style="color: var(--text-secondary); font-size: 14px;">${{pos.amount}}</div>
              ${{pos.health_factor ? `<div style="margin-top: 10px; padding: 4px 8px; background: var(--bg); border-radius: 4px; font-size: 12px;">Health Factor: ${{pos.health_factor}}</div>` : ''}}
            </div>
          `).join('');
          
          // Risk factors
          const riskFactorsList = document.getElementById('riskFactorsList');
          riskFactorsList.innerHTML = data.risk_factors.map(factor => `<li>${{factor}}</li>`).join('');
          
          // Recommendations
          const recommendationsList = document.getElementById('recommendationsList');
          recommendationsList.innerHTML = data.recommendations.map(rec => `<li>${{rec}}</li>`).join('');
        }}
        
        function showSnackbar(message, type = 'info') {{
          const snackbar = document.createElement('div');
          snackbar.className = `snackbar snackbar-${{type}}`;
          snackbar.textContent = message;
          document.body.appendChild(snackbar);
          
          setTimeout(() => {{
            snackbar.classList.add('show');
          }}, 100);
          
          setTimeout(() => {{
            snackbar.classList.remove('show');
            setTimeout(() => document.body.removeChild(snackbar), 300);
          }}, 3000);
        }}
      </script>
{get_3d_javascript()}
    </body>
    </html>
    """

def get_risk_analysis_page():
    return f"""
    <!doctype html>
    <html lang="en">
    <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>Risk Analysis - Safe DeFi Assistant</title>
    <style>{get_base_css()}</style>
    </head>
    <body>
{get_3d_background_elements()}
      <div class="container">
        <nav class="navbar">
          <a href="/" class="logo">
            <div class="logo-icon">DF</div>
            <div>
              <div style="font-size:20px;font-weight:700">Safe DeFi Assistant</div>
              <div style="font-size:12px;color:var(--muted)">Risk Analysis</div>
            </div>
          </a>
          <div class="nav-links">
            <a href="/" class="nav-link">Home</a>
            <a href="/chat" class="nav-link">AI Assistant</a>
            <a href="/gas-prices" class="nav-link">Gas Prices</a>
            <a href="/market-data" class="nav-link">Market Data</a>
            <a href="/risk-analysis" class="nav-link active">Risk Analysis</a>
            <a href="/portfolio" class="nav-link">Portfolio</a>
            <a href="/yield-farming" class="nav-link">Yield Farming</a>
          </div>
        </nav>
        
        <div class="page-header">
          <h1>⚠️ Risk Analysis</h1>
          <p>Comprehensive DeFi risk assessment and protocol safety analysis</p>
        </div>
        
        <div class="card">
          <h2>🚧 Coming Soon</h2>
          <p>Our advanced risk analysis feature is currently under development. This will include:</p>
          <ul>
            <li>Smart contract security audits</li>
            <li>Protocol risk scoring</li>
            <li>Liquidation risk analysis</li>
            <li>Market volatility assessment</li>
            <li>Cross-protocol risk comparison</li>
            <li>Real-time risk alerts</li>
          </ul>
          <p>In the meantime, you can use our <a href="/chat">AI Assistant</a> to get personalized risk assessments!</p>
        </div>
      </div>
      
      <script>
        function showSnackbar(message, type = 'info') {{
          const snackbar = document.createElement('div');
          snackbar.className = `snackbar snackbar-${{type}}`;
          snackbar.textContent = message;
          document.body.appendChild(snackbar);
          
          setTimeout(() => {{
            snackbar.classList.add('show');
          }}, 100);
          
          setTimeout(() => {{
            snackbar.classList.remove('show');
            setTimeout(() => document.body.removeChild(snackbar), 300);
          }}, 3000);
        }}
      </script>
{get_3d_javascript()}
    </body>
    </html>
    """

def get_yield_farming_page():
    return f"""
    <!doctype html>
    <html lang="en">
    <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>Yield Farming - Safe DeFi Assistant</title>
    <style>{get_base_css()}</style>
    </head>
    <body>
{get_3d_background_elements()}
      <div class="container">
        <nav class="navbar">
          <a href="/" class="logo">
            <div class="logo-icon">DF</div>
            <div>
              <div style="font-size:20px;font-weight:700">Safe DeFi Assistant</div>
              <div style="font-size:12px;color:var(--muted)">Yield Farming</div>
            </div>
          </a>
          <div class="nav-links">
            <a href="/" class="nav-link">Home</a>
            <a href="/chat" class="nav-link">AI Assistant</a>
            <a href="/gas-prices" class="nav-link">Gas Prices</a>
            <a href="/market-data" class="nav-link">Market Data</a>
            <a href="/risk-analysis" class="nav-link">Risk Analysis</a>
            <a href="/portfolio" class="nav-link">Portfolio</a>
            <a href="/yield-farming" class="nav-link active">Yield Farming</a>
          </div>
        </nav>
        
        <div class="page-header">
          <h1>🌾 Yield Farming Opportunities</h1>
          <p>Discover high-yield farming opportunities with risk-adjusted returns and safety recommendations</p>
        </div>
        
        <div class="card">
          <h2>🚧 Coming Soon</h2>
          <p>Our yield farming analysis feature is currently under development. This will include:</p>
          <ul>
            <li>Real-time yield opportunity detection</li>
            <li>Risk-adjusted return calculations</li>
            <li>Protocol safety assessments</li>
            <li>Impermanent loss analysis</li>
            <li>Automated yield optimization suggestions</li>
          </ul>
          <p>In the meantime, you can use our <a href="/chat">AI Assistant</a> to get personalized yield farming advice!</p>
        </div>
      </div>
      
      <script>
        function showSnackbar(message, type = 'info') {{
          const snackbar = document.createElement('div');
          snackbar.className = `snackbar snackbar-${{type}}`;
          snackbar.textContent = message;
          document.body.appendChild(snackbar);
          
          setTimeout(() => {{
            snackbar.classList.add('show');
          }}, 100);
          
          setTimeout(() => {{
            snackbar.classList.remove('show');
            setTimeout(() => document.body.removeChild(snackbar), 300);
          }}, 3000);
        }}
      </script>
{get_3d_javascript()}
    </body>
    </html>
    """

def get_risk_analysis_page():
    return f"""
    <!doctype html>
    <html lang="en">
    <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>Risk Analysis - Safe DeFi Assistant</title>
    <style>{get_base_css()}</style>
    </head>
    <body>
{get_3d_background_elements()}
      <div class="container">
        <nav class="navbar">
          <a href="/" class="logo">
            <div class="logo-icon">DF</div>
            <div>
              <div style="font-size:20px;font-weight:700">Safe DeFi Assistant</div>
              <div style="font-size:12px;color:var(--muted)">Risk Analysis</div>
            </div>
          </a>
          <div class="nav-links">
            <a href="/" class="nav-link">Home</a>
            <a href="/chat" class="nav-link">AI Assistant</a>
            <a href="/gas-prices" class="nav-link">Gas Prices</a>
            <a href="/market-data" class="nav-link">Market Data</a>
            <a href="/risk-analysis" class="nav-link active">Risk Analysis</a>
            <a href="/portfolio" class="nav-link">Portfolio</a>
            <a href="/yield-farming" class="nav-link">Yield Farming</a>
          </div>
        </nav>
        
        <div class="page-header">
          <h1>⚠️ Risk Analysis</h1>
          <p>Comprehensive DeFi risk assessment and protocol safety analysis</p>
        </div>
        
        <div class="card">
          <h2>🚧 Coming Soon</h2>
          <p>Our advanced risk analysis feature is currently under development. This will include:</p>
          <ul>
            <li>Smart contract security audits</li>
            <li>Protocol risk scoring</li>
            <li>Liquidation risk analysis</li>
            <li>Market volatility assessment</li>
            <li>Cross-protocol risk comparison</li>
            <li>Real-time risk alerts</li>
          </ul>
          <p>In the meantime, you can use our <a href="/chat">AI Assistant</a> to get personalized risk assessments!</p>
        </div>
      </div>
      
      <script>
        function showSnackbar(message, type = 'info') {{
          const snackbar = document.createElement('div');
          snackbar.className = `snackbar snackbar-${{type}}`;
          snackbar.textContent = message;
          document.body.appendChild(snackbar);
          
          setTimeout(() => {{
            snackbar.classList.add('show');
          }}, 100);
          
          setTimeout(() => {{
            snackbar.classList.remove('show');
            setTimeout(() => document.body.removeChild(snackbar), 300);
          }}, 3000);
        }}
      </script>
{get_3d_javascript()}
    </body>
    </html>
    """
