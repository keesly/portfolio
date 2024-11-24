<template>
	<div ref="canvasContainer" class="canvas-container"></div>
</template>

<script>
import * as THREE from "three";
import { AsciiEffect } from "three/examples/jsm/effects/AsciiEffect.js";

export default {
	name: "AsciiEffectCanvas",
	mounted() {
		this.init();
	},
	beforeUnmount() {
		if (this.renderer) {
			this.renderer.dispose();
		}
		cancelAnimationFrame(this.animationId);
		window.removeEventListener("resize", this.onWindowResize);
		window.removeEventListener("pointermove", this.onPointerMove);
	},
	props: {
		currentTheme: {
			type: String,
			default: "light",
		},
	},
	watch: {
		currentTheme(newTheme) {
			const sphereColor = newTheme === "dark" ? new THREE.Color(0, 0, 0) : new THREE.Color(0xffffff);
			const bgColor = newTheme === "dark" ? 0x000000 : new THREE.Color(0, 0, 0);

			// Update sphere material color
			this.sphere.material.color.set(sphereColor);
			this.sphere.material.transparent = true; // Enable transparency
			this.sphere.material.opacity = newTheme === "light" ? 0 : 1; // Set opacity to 0 in light theme for transparency

			// Update scene background color
			this.scene.background.set(bgColor);

			// Update AsciiEffect colors
			this.effect.domElement.style.color = newTheme === "dark" ? "white" : "black";
			this.effect.domElement.style.backgroundColor = newTheme === "dark" ? "black" : "white";
		},
	},
	methods: {
		init() {
			const start = Date.now();
			THREE.ColorManagement.enabled = true;

			this.windowHalfX = window.innerWidth / 2;
			this.windowHalfY = window.innerHeight / 2;
			this.mouseX = 0;
			this.mouseY = 0;

			this.targetCameraX = 100;
			this.targetCameraY = 70;
			this.targetCameraZ = 280;

			this.camera = new THREE.PerspectiveCamera(
				70,
				window.innerWidth / window.innerHeight,
				1,
				1000
			);
			this.camera.position.y = 70;
			this.camera.position.z = 280;
			this.camera.position.x = 100;

			this.scene = new THREE.Scene();
			this.scene.background = new THREE.Color(0, 0, 0);

			const pointLight1 = new THREE.PointLight(0xffffff, 1, 0, 0);
			pointLight1.position.set(-200, 400, 200);
			this.scene.add(pointLight1);

			const pointLight2 = new THREE.PointLight(0xffffff, 1, 0, 0);
			pointLight2.position.set(200, -400, -150);
			this.scene.add(pointLight2);

			this.sphere = new THREE.Mesh(
				new THREE.SphereGeometry(100, 50, 50),
				new THREE.MeshPhongMaterial({ flatShading: false, })
			);
			this.scene.add(this.sphere);

			this.ring = new THREE.Mesh(
				new THREE.RingGeometry(150, 200, 100),
				new THREE.MeshBasicMaterial({
					color: 0xffd700,
					side: THREE.DoubleSide,
					transparent: true,
					opacity: 1,
				})
			);

			this.ring.position.set(0, 0, 0);
			this.ring.rotation.x = Math.PI / 1.9;
			this.ring.rotation.y = Math.PI / 6;
			this.scene.add(this.ring);

			this.renderer = new THREE.WebGLRenderer();
			this.renderer.setSize(window.innerWidth, window.innerHeight);

			this.effect = new AsciiEffect(this.renderer, " cool.:-+*=%@#", {
				invert: true,
			});
			this.effect.setSize(window.innerWidth, window.innerHeight);
			this.effect.domElement.style.color = "black";
			this.effect.domElement.style.backgroundColor = "white";

			this.$refs.canvasContainer.appendChild(this.effect.domElement);

			this.renderer.setAnimationLoop(() => this.animate(start));

			window.addEventListener("resize", this.onWindowResize);
			window.addEventListener("pointermove", this.onPointerMove);
		},
		animate(start) {
			const timer = Date.now() - start;

			// Smoothly interpolate camera position towards target position
			this.camera.position.x += (this.targetCameraX - this.camera.position.x) * 0.05;
			this.camera.position.y += (this.targetCameraY - this.camera.position.y) * 0.05;
			this.camera.position.z += (this.targetCameraZ - this.camera.position.z) * 0.05;

			this.camera.lookAt(this.scene.position);

			this.sphere.rotation.z = -timer * 0.0003;
			this.sphere.rotation.y = timer * 0.0003;

			this.ring.rotation.z = timer * 0.00005;

			this.effect.render(this.scene, this.camera);
		},

		onPointerMove(event) {
			this.targetCameraX = (event.clientX - this.windowHalfX) * 0.1;
			this.targetCameraY = (this.windowHalfY - event.clientY) * 0.1;
			this.targetCameraZ = 280 + (this.windowHalfX - event.clientY) * 0.1;
		},

		onWindowResize() {
			this.camera.aspect = window.innerWidth / window.innerHeight;
			this.camera.updateProjectionMatrix();

			this.renderer.setSize(window.innerWidth, window.innerHeight);
			this.effect.setSize(window.innerWidth, window.innerHeight);
		},
	},
};
</script>

<style scoped>
.canvas-container {
	width: 100%;
	height: 100%;
	overflow: hidden;
	background-color: black;
	position: absolute;
}
</style>
