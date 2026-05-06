import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { hands, setFingerCurl } from './hand_loader';
import './tts-pane'

const indexSlider = document.getElementById("indexSlider");
const indexSlider2 = document.getElementById("indexSlider2");

indexSlider.addEventListener("input", (e) => {
  const value = parseFloat(e.target.value);
  setFingerCurl(hands.hand2, "index", -value);
});

indexSlider2.addEventListener("input", (e) => {
  const value = parseFloat(e.target.value);
  setFingerCurl(hands.hand1, "index", -value);
});