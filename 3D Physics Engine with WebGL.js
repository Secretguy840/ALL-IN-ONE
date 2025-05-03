// Three.js based physics simulation
import * as THREE from 'three';
import { Physics, RigidBody, CuboidCollider } from '@react-three/rapier';

function QuantumParticles() {
  const particles = useRef([]);
  const [count] = useState(1000);
  
  useFrame((state) => {
    particles.current.forEach((particle, i) => {
      // Quantum position probability
      particle.position.x = Math.sin(state.clock.elapsedTime + i) * 5;
      particle.position.y = Math.cos(state.clock.elapsedTime * 0.5 + i) * 5;
      particle.position.z = Math.sin(state.clock.elapsedTime * 0.3 + i) * 5;
    });
  });

  return (
    <Physics gravity={[0, -2, 0]}>
      {Array.from({ length: count }).map((_, i) => (
        <RigidBody key={i} ref={(el) => (particles.current[i] = el)}>
          <mesh>
            <sphereGeometry args={[0.1, 16, 16]} />
            <meshStandardMaterial color="hotpink" />
          </mesh>
          <CuboidCollider args={[0.1, 0.1, 0.1]} />
        </RigidBody>
      ))}
    </Physics>
  );
}