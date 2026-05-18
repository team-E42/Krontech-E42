import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { hands, setFingerCurl } from './hand_loader';
import './tts-pane'

const socket = new WebSocket('ws://localhost:4040');

socket.onopen = () => {
    console.log('WebSocket connection established');
};

socket.onmessage = (event) => {
  const data = JSON.parse(event.data);;

  const arr = data.values;

  const indexCurl = parseFloat(arr[0]);
  const middleCurl = parseFloat(arr[1]);
  const ringCurl = parseFloat(arr[2]);
  const pinkyCurl = parseFloat(arr[3]);
  const thumbCurl = parseFloat(arr[4]);


  setFingerCurl(hands.hand2, "index", -indexCurl);
  setFingerCurl(hands.hand2, "middle", -middleCurl);
  setFingerCurl(hands.hand2, "ring", -ringCurl);
  setFingerCurl(hands.hand2, "pinky", -pinkyCurl);
  setFingerCurl(hands.hand2, "thumb", -thumbCurl);

  document.getElementById("textInput").innerText = `${data.label}`;
};

socket.onclose = () => {
    console.log('WebSocket connection closed');
};

/*
const indexSlider = document.getElementById("indexSlider");
const indexSlider2 = document.getElementById("indexSlider2");

indexSlider.addEventListener("input", (e) => {
  const value = parseFloat(e.target.value);
  setFingerCurl(hands.hand2, "index", -value);
});

indexSlider2.addEventListener("input", (e) => {
  const value = parseFloat(e.target.value);
  setFingerCurl(hands.hand1, "index", -value);
});*/