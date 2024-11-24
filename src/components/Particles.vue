<template>
	<div ref="canvasContainer" class="canvas-container"></div>
</template>

<script>
import * as THREE from "three";
import gravelTexture from '../assets/textures/gravel_stones_disp_4k.png';
import darkTexture from '../assets/textures/particle.png';
import lightTexture from '../assets/textures/particle-light.png';

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
		window.removeEventListener("mousemove", this.onPointerMove);
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
			const bgColor = newTheme === "dark" ?  0x000000 : new THREE.Color(0xffffff);

			// Update sphere material color
			this.sphere.material.color.set(sphereColor);
			this.sphere.material.transparent = true; // Enable transparency
			this.sphere.material.opacity = newTheme === "light" ? 0 : 1; // Set opacity to 0 in light theme for transparency



			// Update scene background color
			this.scene.background.set(bgColor);

			// Update particles colors
			const textureLoader = new THREE.TextureLoader();
            const newTexture = newTheme === "dark" ? lightTexture : darkTexture;
            
            // Update material with the new texture
            this.asteroidRing.material.map = textureLoader.load(newTexture);
            this.asteroidRing.material.needsUpdate = true;
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
			this.scene.background = new THREE.Color(0xffffff);

			const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
			this.scene.add(ambientLight);

			const pointLight1 = new THREE.PointLight(0xffffff, 1, 500, 2);
			pointLight1.position.set(-200, 400, 200);
			this.scene.add(pointLight1);

			const pointLight2 = new THREE.PointLight(0xffa500, 0.8, 500, 2);
			pointLight2.position.set(200, -200, -200);
			this.scene.add(pointLight2);

            const textureLoader = new THREE.TextureLoader();

            const sphereTexture = textureLoader.load(gravelTexture);

			this.sphere = new THREE.Mesh(
				new THREE.SphereGeometry(100, 200, 200),
				new THREE.MeshPhongMaterial({ 
                    map: sphereTexture, 
                })
			);
			// this.scene.add(this.sphere);

			this.createAsteroidRing();

			this.renderer = new THREE.WebGLRenderer({alpha: true});
			this.renderer.setSize(window.innerWidth, window.innerHeight);

			// Append renderer's domElement directly
			this.$refs.canvasContainer.appendChild(this.renderer.domElement);

			window.addEventListener("resize", this.onWindowResize);
			window.addEventListener("mousemove", this.onPointerMove);

			// Start animation loop
			this.renderer.setAnimationLoop(() => this.animate(start));
		},
		createAsteroidRing() {
			const particleCount = 20000;
            const positions = new Float32Array(particleCount * 3);

            for (let i = 0; i < particleCount; i++) {
                const theta = Math.random() * 2 * Math.PI;
                const radius = 150 + Math.random() * 500;

                const x = Math.cos(theta) * radius;
                const y = Math.sin(theta) * radius;
                const z = (Math.random() - 0.5) * 30;

                positions[i] = x;
                positions[i + 1] = y;
                positions[i + 2] = z;
            }

            const particleGeometry = new THREE.BufferGeometry();
            particleGeometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));

            const textureLoader = new THREE.TextureLoader();
            const initialTexture = this.currentTheme === "dark" ? lightTexture : darkTexture;
			const particleTexture = textureLoader.load(initialTexture)

            const particleMaterial = new THREE.PointsMaterial({
                map: particleTexture,
                size: 2,
                transparent: true,
                opacity: 0.75,
                alphaTest: 0.5
            });

            this.asteroidRing = new THREE.Points(particleGeometry, particleMaterial);
            this.scene.add(this.asteroidRing);
		},
		animate(start) {
			const timer = Date.now() - start;

			// Smoothly interpolate camera position towards target position
			this.camera.position.x +=
				(this.targetCameraX - this.camera.position.x) * 0.05;
			this.camera.position.y +=
				(this.targetCameraY - this.camera.position.y) * 0.05;
			this.camera.position.z +=
				(this.targetCameraZ - this.camera.position.z) * 0.05;

			this.sphere.rotation.z = -timer * 0.0003;
			this.sphere.rotation.y = timer * 0.0003;

			this.asteroidRing.rotation.y += 0.001;

			this.renderer.render(this.scene, this.camera);
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
