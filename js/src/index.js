import * as three from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { HDRLoader } from 'three/examples/jsm/loaders/HDRLoader.js';

const leftDiv = document.getElementById('left');

const scene = new three.Scene();

const light = new three.PointLight(0xff0000, 1000, 100 );
light.position.set(5, 0, 5);
scene.add(light);

const light = new three.HemisphereLight( 0xffffff, 0x080820, 1 );
scene.add(light);

const camera = new three.PerspectiveCamera(90, leftDiv.clientWidth / leftDiv.clientHeight, 0.1, 1000);
camera.position.z = 5;

//-------HAND MOVEMENT-------\\\
const hand1 = {
  wrist: "HANDPALM_joint_02",

  index: ["INDEX_BASE_joint_03", "INDEX_MID_joint_04", "INDEX_TOP_joint_05"],
  middle: ["MIDDLE_F_BASE_joint_07", "MIDDLE_F_MID_joint_08", "MIDDLE_F_TOP_joint_09"],
  ring: ["RING_BASE_joint_011", "RING_MID_joint_012", "RING_TOP_joint_013"],
  pinky: ["PINK_BASE_joint_015", "PINK_MID_joint_016", "PINK_TOP_joint_017"],
  thumb: ["THUMB_BASE_joint_019", "THUMB_MID_joint_020", "THUMB_TOP_joint_021"]
};

const hand2 = {
  wrist: "HANDPALM_joint_024",

  index: ["INDEX_BASE_joint_025", "INDEX_MID_joint_026", "INDEX_TOP_joint_027"],
  middle: ["MIDDLE_F_BASE_joint_029", "MIDDLE_F_MID_joint_030", "MIDDLE_F_TOP_joint_031"],
  ring: ["RING_BASE_joint_033", "RING_MID_joint_034", "RING_TOP_joint_035"],
  pinky: ["PINK_BASE_joint_037", "PINK_MID_joint_038", "PINK_TOP_joint_039"],
  thumb: ["THUMB_BASE_joint_041", "THUMB_MID_joint_042", "THUMB_TOP_joint_06"]
};

let bones = {};

function setFingerCurl(hand, fingerName, amount) {
    const [base, mid, top] = hand[fingerName];
    
   // console.log(base, bones[base]);
  //  console.log(mid, bones[mid]);
   // console.log(top, bones[top]);

    if (!bones[base] || !bones[mid] || !bones[top]) {
        console.error("Bone missing!", base, mid, top);
        return;
    }
    
    bones[base].rotation.set(0, 0, 0);
    bones[mid].rotation.set(0, 0, 0);
    bones[top].rotation.set(0, 0, 0);

    if(fingerName === "thumb") {
        bones[base].rotation.y = -amount * 0.3;
        bones[mid].rotation.z = -amount * 0.7;
        bones[top].rotation.z = -amount * 0.9;
    }else{
        bones[base].rotation.y = amount * 0.5;
        bones[mid].rotation.y = amount * 0.7;
        bones[top].rotation.y = amount * 0.9;
    }
    
}

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
renderer.setSize(leftDiv.clientWidth, leftDiv.clientHeight);
renderer.setPixelRatio(window.devicePixelRatio);
renderer.toneMapping = three.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1;

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

leftDiv.appendChild(renderer.domElement);

//const lensFlare = new three.LensFlare();
//lensFlare.addElement(new three.LensFlareElement(new three.TextureLoader().load('/public/lensflare.png'), 512, 0, new three.Vector2(0.5, 0.5)));

renderer.setAnimationLoop((timestamp) => {
    controls.update();
    renderer.render(scene, camera);
});

window.addEventListener('resize', (event) => {
    renderer.setSize(leftDiv.clientWidth, leftDiv.clientHeight);
    camera.aspect = (leftDiv.clientWidth / leftDiv.clientHeight);
    camera.updateProjectionMatrix();
});

//--------TTS--------\\

let currentLanguage = 'en-US';

const textInput = document.getElementById('textInput');
const speakBtn = document.getElementById('speakBtn');
const stopBtn = document.getElementById('stopBtn');

const synth = window.speechSynthesis;

let voices = [];

function loadVoices() {
    voices = synth.getVoices();
}
synth.onvoiceschanged = loadVoices;
loadVoices();

const langToggle = document.getElementById('langToggle');

langToggle.addEventListener('click', () => {
    if (currentLanguage === "en-US") {
        currentLanguage = "ro-RO";
        langToggle.textContent = "🌐 Română";
    } else {
        currentLanguage = "en-US";
        langToggle.textContent = "🌐 English";
    }
});

console.log(voices);

speakBtn.addEventListener('click', () => {
    const text = textInput.value;
    if (text) {
        const utterance = new SpeechSynthesisUtterance(text);

        const voice = voices.find(v => v.lang === currentLanguage);
        if (voice) utterance.voice = voice;

        utterance.lang = currentLanguage;
        utterance.rate = .9;
        utterance.pitch = 2;  
        utterance.volume = 1; 

        synth.speak(utterance);
    }
});

stopBtn.addEventListener('click', () => {
    synth.cancel();
});