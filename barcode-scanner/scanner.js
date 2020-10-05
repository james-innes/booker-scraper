// To debug this code, open wixDefaultCustomElement.js in Developer Tools.

import Quagga from "quagga";
var _scannerIsRunning = false;

function startScanner() {
	Quagga.init({
			inputStream: {
				name: "Live",
				type: "LiveStream",
				target: document.querySelector("#wdce-scanner-container"),
				constraints: {
					width: 480,
					height: 320,
					facingMode: "environment"
				}
			},
			decoder: {
				readers: [
					"code_128_reader",
					"ean_reader",
					"ean_8_reader",
					"code_39_reader",
					"code_39_vin_reader",
					"codabar_reader",
					"upc_reader",
					"upc_e_reader",
					"i2of5_reader"
				],
				debug: {
					showCanvas: true,
					showPatches: true,
					showFoundPatches: true,
					showSkeleton: true,
					showLabels: true,
					showPatchLabels: true,
					showRemainingPatchLabels: true,
					boxFromPatches: {
						showTransformed: true,
						showTransformedBox: true,
						showBB: true
					}
				}
			}
		},
		function (err) {
			if (err) {
				console.log(err);
				return;
			}

			console.log("Initialization finished. Ready to start");
			Quagga.start();

			// Set flag to is running
			_scannerIsRunning = true;
		}
	);

	Quagga.onProcessed(function (result) {
		var drawingCtx = Quagga.canvas.ctx.overlay,
			drawingCanvas = Quagga.canvas.dom.overlay;

		if (result) {
			if (result.boxes) {
				drawingCtx.clearRect(
					0,
					0,
					parseInt(drawingCanvas.getAttribute("width")),
					parseInt(drawingCanvas.getAttribute("height"))
				);
				result.boxes
					.filter(function (box) {
						return box !== result.box;
					})
					.forEach(function (box) {
						Quagga.ImageDebug.drawPath(box, { x: 0, y: 1 }, drawingCtx, {
							color: "green",
							lineWidth: 2
						});
					});
			}

			if (result.box) {
				Quagga.ImageDebug.drawPath(result.box, { x: 0, y: 1 }, drawingCtx, {
					color: "#00F",
					lineWidth: 2
				});
			}

			if (result.codeResult && result.codeResult.code) {
				Quagga.ImageDebug.drawPath(
					result.line, { x: "x", y: "y" },
					drawingCtx, { color: "red", lineWidth: 3 }
				);
			}
		}
	});

	Quagga.onDetected(function (result) {
		console.log(
			"Barcode detected and processed : [" + result.codeResult.code + "]",
			result
		);
	});
}

// Start/stop scanner
document.getElementById("wdce-btn").addEventListener(
	"click",
	function () {
		if (_scannerIsRunning) {
			Quagga.stop();
		} else {
			startScanner();
		}
	},
	false
);

//

// //

const createScannerContainer = () => {
	const scannerContainer = document.createElement('div');
	scannerContainer.id = 'wdce-scanner-container';
	return scannerContainer;
};

const createScannerButton = () => {
	const scannerButton = document.createElement('input');
	scannerButton.id = 'wdce-btn';
	scannerButton.type = 'button';
	scannerButton.value = 'Start/Stop the scanner';
}

// end of my code

const IMAGE_URL = 'https://icatcare.org/app/uploads/2018/07/Thinking-of-getting-a-cat.png';
const H2_TEXT = 'This is a Custom Element (Corvid)';

const createImage = () => {
	const imageElement = document.createElement('img');
	imageElement.src = IMAGE_URL;
	imageElement.id = 'wdce-image';
	return imageElement;
};

const createH2 = () => {
	const h2Element = document.createElement('h2');
	h2Element.textContent = H2_TEXT;
	h2Element.id = 'wdce-h2';
	return h2Element;
};

const createTextContainer = () => {
	const textContainer = document.createElement('div');
	textContainer.id = 'wdce-text-container';
	textContainer.appendChild(createH2());
	textContainer.appendChild(createH3('wdce-h3-1', H3_1_TEXT));
	textContainer.appendChild(createH3('wdce-h3-2', H3_2_TEXT));
	return textContainer;
};

const createImageContainer = () => {
	const imageContainer = document.createElement('div');
	imageContainer.id = 'wdce-image-container';
	imageContainer.appendChild(createImage());
	return imageContainer;
};

const createStyle = () => {
	const styleElement = document.createElement('style');
	styleElement.innerHTML = `
    wix-default-custom-element {
        background-color: #fe5900;
        display: flex;
        height: 100%;
        height: -moz-available;
        height: -webkit-fill-available;
        width: 100%;
        justify-content: center;
        canvas.drawing,
        canvas.drawingBuffer {
          position: absolute;
          left: 0;
          top: 0;
		    }
    }

    #wdce-image-container {
        width: 35%;
        max-width: 165px;
        display: flex;
        margin: 0 20px 0 30px;
        overflow: hidden;
    }

    #wdce-image {
        width: 100%;
        min-width: 100px;
    }

    #wdce-text-container {
        display: flex;
        flex-direction: column;
        width: 65%;
        justify-content: center;
        max-width: 314px;
        min-width: 200px;
    }

    #wdce-h2 {
        font-family: 'HelveticaNeueW01-45Ligh, HelveticaNeueW02-45Ligh, HelveticaNeueW10-45Ligh, Helvetica Neue, Helvetica, Arial, メイリオ, meiryo, ヒラギノ角ゴ pro w3, hiragino kaku gothic pro, sans-serif',
        font-size: 16px;
        font-weight: 500;
        letter-spacing: 0.89px;
        color: #32536a;
        margin: 0 0 16px 0;
    }
    `;
	return styleElement;
};

class WixDefaultCustomElement extends HTMLElement {
	constructor() {
		super();
	}

	connectedCallback() {
		this.appendChild(createStyle());
		this.appendChild(createImageContainer());
		this.appendChild(createTextContainer());
		this.appendChild(createScannerContainer());
		this.appendChild(createScannerButton());
	}
}
customElements.define('wix-default-custom-element', WixDefaultCustomElement);