import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { scene } from './render';

// load 3d model into scene
const loader = new GLTFLoader();
let bones = {};
loader.load('/public/hand_model.glb', (model) => {
    model.scene.traverse((obj) => {
        if(obj.isMesh) {
            obj.material.color.set(0x0186ea8);

        }
        if (obj.isBone) {
            bones[obj.name] = obj;
            console.log("Bone found:", obj.name);
        }
    });
    scene.add(model.scene);
    scene.getObjectByName("Root_joint_01").rotateZ(Math.PI/2);
    scene.getObjectByName("Root_joint_01").position.set(0, 40000, 0);
    scene.getObjectByName("Root_joint_023").rotateZ(Math.PI/2);
});

// prepare finger movement
export const hands = {
    hand1: {
        wrist: "HANDPALM_joint_02",

        index: ["INDEX_BASE_joint_03", "INDEX_MID_joint_04", "INDEX_TOP_joint_05"],
        middle: ["MIDDLE_F_BASE_joint_07", "MIDDLE_F_MID_joint_08", "MIDDLE_F_TOP_joint_09"],
        ring: ["RING_BASE_joint_011", "RING_MID_joint_012", "RING_TOP_joint_013"],
        pinky: ["PINK_BASE_joint_015", "PINK_MID_joint_016", "PINK_TOP_joint_017"],
        thumb: ["THUMB_BASE_joint_019", "THUMB_MID_joint_020", "THUMB_TOP_joint_021"]
    },
    hand2: {
        wrist: "HANDPALM_joint_024",

        index: ["INDEX_BASE_joint_025", "INDEX_MID_joint_026", "INDEX_TOP_joint_027"],
        middle: ["MIDDLE_F_BASE_joint_029", "MIDDLE_F_MID_joint_030", "MIDDLE_F_TOP_joint_031"],
        ring: ["RING_BASE_joint_033", "RING_MID_joint_034", "RING_TOP_joint_035"],
        pinky: ["PINK_BASE_joint_037", "PINK_MID_joint_038", "PINK_TOP_joint_039"],
        thumb: ["THUMB_BASE_joint_041", "THUMB_MID_joint_042", "THUMB_TOP_joint_06"]
    }
};

export const setFingerCurl = (hand, fingerName, amount) => {
    const [base, mid, top] = hand[fingerName];
   
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
};
