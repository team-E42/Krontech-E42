import * as three from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { HDRLoader } from 'three/examples/jsm/loaders/HDRLoader.js';

// three js objects
export const scene = new three.Scene();
const renderDiv = document.getElementById('render');
const textureLoader = new three.TextureLoader();
const camera = new three.PerspectiveCamera(90, renderDiv.clientWidth / renderDiv.clientHeight, 0.1, 1000);
camera.position.z = 5;
const light = new three.HemisphereLight( 0xffffff, 0x080820, 7 );
const renderer = new three.WebGLRenderer({ antialias: true });
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

// background image
const setSkySphere_JPG = (scene, imagePath) => {  
  textureLoader.load(imagePath, (jpgTexture) => {
    let skySphereGeometry = new three.SphereGeometry(1000, 60, 60);
    let skySphereMaterial = new three.MeshBasicMaterial({
      map: jpgTexture
    });
  
    skySphereMaterial.side = three.BackSide;
    let skySphereMesh = new three.Mesh(skySphereGeometry, skySphereMaterial);

    scene.add(skySphereMesh);
  });
};

// building scene
const skyBoxPath = '/public/9078.jpg';
setSkySphere_JPG(scene, skyBoxPath);

scene.add(light);

renderer.setSize(renderDiv.clientWidth, renderDiv.clientHeight);
renderer.setPixelRatio(window.devicePixelRatio);
renderer.toneMapping = three.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1;

renderDiv.appendChild(renderer.domElement);

// updates and listeners
window.addEventListener('resize', (event) => {
    renderer.setSize(renderDiv.clientWidth, renderDiv.clientHeight);
    camera.aspect = (renderDiv.clientWidth / renderDiv.clientHeight);
    camera.updateProjectionMatrix();
});

renderer.setAnimationLoop((timestamp) => {
    controls.update();
    renderer.render(scene, camera);
});
