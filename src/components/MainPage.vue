<template>
	<div :style="{ cursor: customCursor }">
		<div class="side-buttons">
			<div class="theme-toggle" @click="toggleTheme">
				<span>{{
					currentTheme === "light" ? "Dark theme" : "Light theme"
				}}</span>
			</div>
			<!-- <div class="ascii-toggle" @click="toggleAsciiEffect">
				<span>{{
					asciiEffectEnabled ? "ascii planet off" : "ascii planet on"
				}}</span>
			</div> -->
		</div>
		<div class="wrapper">
			<AsciiEffectCanvas
				v-if="asciiEffectEnabled"
				:currentTheme="currentTheme"
			/>
			<Particles
				v-else-if="currentParticleImage === ''"
				:currentTheme="currentTheme"
			/>
			<ImageParticles
				v-else
				:particleImage="currentParticleImage"
				:currentTheme="currentTheme"
			/>
			<div class="text">
				<h1>Mark Ryzhov</h1>
				<div class="job">Fullstack Developer</div>
				<div class="sections">
					<ul>
						<li
							:class="selectedOption === 'aboutMe' ? 'selected' : ''"
							@click="selectOption('aboutMe')"
						>
							<span>{{ selectedOption === "aboutMe" ? "->" : "" }}</span> about
							me
						</li>
						<li
							:class="selectedOption === 'projects' ? 'selected' : ''"
							@click="selectOption('projects')"
						>
							<span>{{ selectedOption === "projects" ? "->" : "" }}</span>
							projects
						</li>
						<li
							:class="selectedOption === 'contacts' ? 'selected' : ''"
							@click="selectOption('contacts')"
						>
							<span>{{ selectedOption === "contacts" ? "->" : "" }}</span>
							contacts
						</li>
					</ul>
				</div>
				<div class="content">
					<div v-if="selectedOption === 'aboutMe'">
						Born in 1999 in Far-Eastern region of Russia.<br />I am a
						results-oriented fullstack web developer committed to crafting
						high-performance web applications.<br><br>My goal is to merge
						functionality and aesthetics to create exceptional user experiences.
					</div>
					<div v-if="selectedOption === 'projects'">
						<ul>
							<li
								v-for="project in projects"
								:key="project.id"
								@mouseover="onHoverContact(project.name)"
								@mouseleave="onMouseLeave"
							>
								<a
									v-if="project.name != 'portfolio'"
									:href="project.html_url"
									target="_blank"
									>{{ project.name }}</a
								>
							</li>
						</ul>
					</div>
					<div v-if="selectedOption === 'contacts'">
						<ul>
							<li>
								<a href="" target="_blank">
									<img :src="require('@/assets/icons/tg.png')" alt="telegram" />
									<div>telegram</div>
								</a>
							</li>
							<li>
								<a href="" target="_blank">
									<img :src="require('@/assets/icons/wa.png')" alt="whatsapp" />
									<div>whatsapp</div>
								</a>
							</li>
							<li>
								<a
									href="https://www.linkedin.com/in/mark-ryzhov-576487309?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BAt3GM91fQ%2F6p8%2BtL2zHQvA%3D%3D"
									target="_blank"
								>
									<img :src="require('@/assets/icons/li.png')" alt="linkedin" />
									<div>linkedin</div>
								</a>
							</li>
							<li>
								<a href="mailto:fidgetyman@gmail.com" target="_blank">
									<img :src="require('@/assets/icons/email.png')" alt="email" />
									<div>fidgetyman@gmail.com</div>
								</a>
							</li>
						</ul>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import axios from "axios";
import AsciiEffectCanvas from "./AsciiEffectCanvas.vue";
import Particles from "./Particles.vue";
import ImageParticles from "./ImageParticles.vue";
import "@/assets/fonts/fonts.css";
import customCursorDark from '@/assets/textures/cursor.png';
import customCursorLight from '@/assets/textures/cursor-light.png';

export default {
	components: {
		AsciiEffectCanvas,
		Particles,
		ImageParticles,
	},
	data() {
		return {
			projects: [],
			loading: true,
			error: null,
			selectedOption: "aboutMe",
			currentTheme: "light",
			asciiEffectEnabled: false,
			currentParticleImage: "",
			customCursor: `url(${customCursorDark}) 16 16, pointer`
		};
	},
	computed: {
		isDarkTheme() {
			return this.currentTheme === "dark";
		},
	},
	async mounted() {
		try {
			const response = await axios.get(
				`${process.env.VUE_APP_API_URL}/projects`
			);
			this.projects = response.data.projects;
		} catch (err) {
			console.log(err);
			this.error = "Failed to load projects.";
		} finally {
			this.loading = false;
		}
	},
	methods: {
		selectOption(option) {
			this.selectedOption = option;
			this.currentParticleImage = "";
		},

		toggleTheme() {
			this.currentTheme = this.currentTheme === "light" ? "dark" : "light";
			document.documentElement.classList.toggle(
				"dark",
				this.currentTheme === "dark"
			);
			document.documentElement.classList.toggle(
				"light",
				this.currentTheme === "light"
			);

			this.customCursor = this.currentTheme === "dark" ? `url(${customCursorLight}) 16 16, pointer` : `url(${customCursorDark}) 16 16, pointer`;
		},

		toggleAsciiEffect() {
			this.asciiEffectEnabled = !this.asciiEffectEnabled;
			console.log(this.asciiEffectEnabled);
		},

		onHoverContact(option) {
			switch (option) {
				case "eve-ai-assisstant":
					this.currentParticleImage = require("@/assets/textures/eve-ai.png");
					break;
				case "fish-weight-estimation":
					this.currentParticleImage = require("@/assets/textures/fish.png");
					break;
				case "news-analyser":
					this.currentParticleImage = require("@/assets/textures/news.png");
					break;
				default:
					this.currentParticleImage = "";
			}
		},

		onMouseLeave() {
			this.currentParticleImage = ""; // Reset when mouse leaves
		},
	},
};
</script>

<style scoped lang="scss">
ul,
ol {
	list-style: none; /* Remove bullet points */
	padding: 0; /* Optional: Remove padding */
	margin: 0; /* Optional: Remove margin */
}

a {
	color: var(--text-color);
	transition: 0.15s ease;

	&:hover {
		color: rgb(187, 187, 187);
	}
}

h1 {
	margin: 0;
	color: var(--text-color);
}
.wrapper {
	position: relative;
	border: 1px solid rgb(187, 187, 187);

	margin: 50px;
	height: 87vh;
}

.text {
	position: absolute;
	font-family: "Roboto mono", sans-serif;
	margin-left: 50px;
	margin-top: 50px;
	font-size: 24px;
	text-align: left;
	width: 30%;
}

.job {
	font-size: 20px;
	font-weight: 800;
	color: var(--text-color);
}

li {
	margin-top: 5px;
	transition: 0.15s ease;
	width: fit-content;
	color: var(--text-color);

	&:hover {
		color: rgb(187, 187, 187);
	}

	a {
		text-decoration: none;
		gap: 10px;
		display: flex;
		align-items: center;
	}

	img {
		width: 24px;
		height: 24px;
	}
}

.sections {
	margin-top: 30px;
	font-size: 14px;
	font-weight: 800;
	transition: 0.1s ease;

	.selected {
		color: rgb(187, 187, 187);
	}
}

.side-buttons {
	display: flex;
	flex-direction: row;
	gap: 30px;
	position: fixed;
	z-index: 2;
	bottom: 180px;
	left: -60px;
	transform: rotate(-90deg);

	.theme-toggle,
	.ascii-toggle {
		width: fit-content;
	}
}

.content {
	font-size: 18px;
	margin-top: 20px;
	color: var(--text-color);
}

.wrapper {
	border-color: var(--text-color);
}

.side-buttons .theme-toggle,
.ascii-toggle {
	color: var(--text-color);
}
</style>
