<template>
	<div ref="canvasContainer" class="canvas-container"></div>
</template>

<script>
import * as THREE from "three";
import gravelTexture from "../assets/textures/gravel_stones_disp_4k.png";
import darkTexture from "../assets/textures/particle.png";
import lightTexture from "../assets/textures/particle-light.png";
import silhouetteImageSrc from "../assets/textures/eve-ai.png";

export default {
	name: "ImageParticles",
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
		image: {},
	},
	watch: {
		currentTheme(newTheme) {
			const sphereColor =
				newTheme === "dark"
					? new THREE.Color(0, 0, 0)
					: new THREE.Color(0xffffff);
			const bgColor =
				newTheme === "dark" ? 0x000000 : new THREE.Color(0xffffff);

			// Update sphere material color
			this.sphere.material.color.set(sphereColor);
			this.sphere.material.transparent = true;
			this.sphere.material.opacity = newTheme === "light" ? 0 : 1;

			// Update scene background color
			this.scene.background.set(bgColor);

			// Update particle texture based on theme
			const textureLoader = new THREE.TextureLoader();
			const newTexture = newTheme === "dark" ? lightTexture : darkTexture;
			this.particleSystem.material.map = textureLoader.load(newTexture);
			this.particleSystem.material.needsUpdate = true;
		},
	},
	methods: {
		init() {
			THREE.ColorManagement.enabled = true;

			this.windowHalfX = window.innerWidth / 2;
			this.windowHalfY = window.innerHeight / 2;
			this.mouseX = 0;
			this.mouseY = 0;

			this.camera = new THREE.PerspectiveCamera(
				70,
				window.innerWidth / window.innerHeight,
				1,
				1000
			);
			this.camera.position.set(-150, 0, 350);

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

			this.renderer = new THREE.WebGLRenderer({ alpha: true });
			this.renderer.setSize(window.innerWidth, window.innerHeight);
			this.$refs.canvasContainer.appendChild(this.renderer.domElement);

			this.createSilhouetteParticles().then(() => {
				window.addEventListener("resize", this.onWindowResize);
				window.addEventListener("mousemove", this.onPointerMove);

				// Start animation loop only after particles are created
				this.renderer.setAnimationLoop(() => this.animate());
			});
		},
		async createSilhouetteParticles() {
			const silhouetteImage = new Image();
			silhouetteImage.src = silhouetteImageSrc;
			await silhouetteImage.decode();

			const canvas = document.createElement("canvas");
			canvas.width = silhouetteImage.width;
			canvas.height = silhouetteImage.height;
			const context = canvas.getContext("2d");
			context.drawImage(silhouetteImage, 0, 0);

			const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
			const particles = [];
			const particleSizeRange = [1, 10];

			const scale = 1; // Adjust for desired particle spacing

			for (let y = 0; y < canvas.height; y += 1) {
				for (let x = 0; x < canvas.width; x += 1) {
					const i = (y * canvas.width + x) * 4;
					const alpha = imageData.data[i + 3];

					if (alpha > 128) {
						const px = (x - canvas.width / 2) * scale;
						const py = (canvas.height / 2 - y) * scale;
						const pz = (Math.random() - 0.5) * 150;
						const size =
							particleSizeRange[0] +
							Math.random() * (particleSizeRange[1] - particleSizeRange[0]);

						particles.push({ position: new THREE.Vector3(px, py, pz), size });
					}
				}
			}

			const geometry = new THREE.BufferGeometry();
			const positions = new Float32Array(particles.length * 3);
			const sizes = new Float32Array(particles.length);

			particles.forEach((particle, i) => {
				positions[i * 3] = particle.position.x;
				positions[i * 3 + 1] = particle.position.y;
				positions[i * 3 + 2] = particle.position.z;
				sizes[i] = particle.size;
			});

			geometry.setAttribute(
				"position",
				new THREE.BufferAttribute(positions, 3)
			);
			geometry.setAttribute("size", new THREE.BufferAttribute(sizes, 1));

			const textureLoader = new THREE.TextureLoader();
			const particleTexture = textureLoader.load(
				this.currentTheme === "dark" ? lightTexture : darkTexture
			);

			const material = new THREE.PointsMaterial({
				map: particleTexture,
				size: 1,
				transparent: true,
				opacity: 0.75,
			});

			this.particleSystem = new THREE.Points(geometry, material);
			this.scene.add(this.particleSystem);
		},
		animate() {
			const time = Date.now() * 0.0005;

			// Parallax effect for 3D depth
			this.camera.position.x += Math.sin(time * 0.05) * 0.01;
			this.camera.position.y += Math.cos(time * 0.05) * 0.01;

			// this.particleSystem.rotation.y += 0.00001;
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
