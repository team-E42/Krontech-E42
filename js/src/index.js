import * as three from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { HDRLoader } from 'three/examples/jsm/loaders/HDRLoader.js';

const scene = new three.Scene();

const camera = new three.PerspectiveCamera(90, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 5;

let mixer;
const loader = new GLTFLoader();
loader.load('/public/hand_model.gltf', (gltf) => {
    const model = gltf.scene;
    console.log(model.skeleton);
    scene.add(model);
    mixer = new three.AnimationMixer(model);
    mixer.clipAction(gltf.animations[0]).play();
});

// init render and controls
const renderer = new three.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
renderer.setPixelRatio(window.devicePixelRatio);
renderer.toneMapping = three.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1;

document.body.appendChild(renderer.domElement);

renderer.setAnimationLoop((timestamp) => {
    controls.update();
    renderer.render(scene, camera);
});

window.addEventListener('resize', (event) => {
    renderer.setSize(window.innerWidth, window.innerHeight);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
});
