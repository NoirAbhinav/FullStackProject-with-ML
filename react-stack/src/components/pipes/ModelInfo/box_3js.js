import React, { useRef, useState } from "react";
import { Canvas, useFrame } from "@react-three/fiber";

function Cylinder3d(props) {
  // This reference gives us direct access to the THREE.Mesh object
  const ref = useRef();
  // Hold state for hovered and clicked events
  const [hovered, hover] = useState(false);
  const [clicked, click] = useState(false);
  // Subscribe this component to the render-loop, rotate the mesh every frame
  //   useFrame((state, delta) => (ref.current.rotation.x += 0.01));
  // Return the view, these are regular Threejs elements expressed in JSX
  return (
    <mesh
      visible
      ref={ref}
      position={props.position}
      scale={clicked ? 1.5 : 1}
      onClick={(event) => click(!clicked)}
      onPointerOver={(event) => hover(true)}
      onPointerOut={(event) => hover(false)}
    >
      {console.log(props.position[0])}
      <boxGeometry attach="geometry" args={[1, 1, 1]} />
      <meshStandardMaterial
        wireframe={props.wireframe}
        color={hovered ? "hotpink" : "orange"}
      />
    </mesh>
  );
}

export default function Box_node() {
  return (
    <Canvas>
      <ambientLight />
      <pointLight position={[100, 100, 100]} />
      <Cylinder3d
        position={[5, 0, 0]}
        size={[4, 4, 0.5]}
        rotation={[Math.PI * 0.1, Math.PI * 0.5, Math.PI * 0.05]}
      />
      <Cylinder3d
        position={[0, 0, 0]}
        size={[1, 1, 0.5]}
        rotation={[Math.PI * 0.1, Math.PI * 0.5, Math.PI * 0.05]}
      />
    </Canvas>
  );
}
