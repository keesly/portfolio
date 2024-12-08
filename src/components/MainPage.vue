<template>
	<transition name="fade-left-right" @after-leave="showMainContent">
		<div v-if="loaderVisible" class="loader-container">
			<LoaderText />
		</div>
	</transition>
	<transition name="fade">
		<div v-if="mainContentVisible" :style="{ cursor: customCursor }">
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
					<div class="left-side">
						<h1>MARK RYZHOV</h1>
						<div class="job">Fullstack Developer</div>
						<div class="sections">
							<ul>
								<li
									:class="selectedOption === 'aboutMe' ? 'selected' : ''"
									@click="selectOption('aboutMe')"
								>
									<span>{{ selectedOption === "aboutMe" ? "->" : "" }}</span>
									about me
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
					</div>

					<div
						class="content"
						ref="contentDiv"
						style="overflow-y: auto; max-height: 100%"
					>
						<div
							v-if="selectedOption === 'aboutMe'"
							class="about-me-text"
							style="margin-top: 20px"
						>
							Born in 1999 in Far-Eastern region of Russia.<br /><br />I am a
							results-oriented fullstack web developer committed to crafting
							high-performance web applications.<br /><br />My goal is to merge
							functionality and aesthetics to create exceptional user
							experiences.
						</div>
						<div v-if="selectedOption === 'projects'">
							<ul>
								<li
									v-for="project in projects"
									:key="project.id"
									@mouseover="onHoverContact(project.name)"
									@mouseleave="onMouseLeave"
								>
									<a :href="project.html_url" target="_blank">{{
										project.name
									}}</a>
									<div>
										<span>{{ project.updated_at }}</span
										><span>/</span> <span>{{ project.type }}</span
										><span>/</span>
										<span>{{ project.language }}</span>
									</div>
								</li>
							</ul>
						</div>
						<div v-if="selectedOption === 'contacts'" style="margin-top: 20px">
							<ul>
								<li>
									<a href="https://t.me/eveanatomy" target="_blank">
										<!-- <img :src="require('@/assets/icons/tg.png')" alt="telegram" /> -->
										<div>telegram</div>
									</a>
								</li>
								<li>
									<a href="https://wa.me/996708857412" target="_blank">
										<!-- <img :src="require('@/assets/icons/wa.png')" alt="whatsapp" /> -->
										<div>whatsapp</div>
									</a>
								</li>
								<li>
									<a
										href="https://www.linkedin.com/in/mark-ryzhov-576487309?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BAt3GM91fQ%2F6p8%2BtL2zHQvA%3D%3D"
										target="_blank"
									>
										<!-- <img :src="require('@/assets/icons/li.png')" alt="linkedin" /> -->
										<div>linkedin</div>
									</a>
								</li>
								<li>
									<a href="mailto:fidgetyman@gmail.com" target="_blank">
										<!-- <img :src="require('@/assets/icons/email.png')" alt="email" /> -->
										<div>fidgetyman@gmail.com</div>
									</a>
								</li>
							</ul>
						</div>
					</div>
				</div>
			</div>
		</div>
	</transition>
</template>

<script>
// import axios from "axios";
import AsciiEffectCanvas from "./AsciiEffectCanvas.vue";
import Particles from "./Particles.vue";
import ImageParticles from "./ImageParticles.vue";
import "@/assets/fonts/fonts.css";
import customCursorDark from "@/assets/textures/cursor.png";
import customCursorLight from "@/assets/textures/cursor-light.png";
import LoaderText from "./LoaderText.vue";

export default {
	components: {
		AsciiEffectCanvas,
		Particles,
		ImageParticles,
		LoaderText,
	},
	data() {
		return {
			projects: [
				{
					name: "PORTFOLIO",
					html_url: "https://github.com/keesly/portfolio",
					description: "portfolio",
					type: "web app",
					language: "Vue+Python",
					updated_at: "DEC 2024",
				},
				{
					name: "FISH WEIGHT PREDICTION",
					html_url: "",
					description: "fish weight estimation",
					type: "ML",
					language: "Python",
					updated_at: "OCT 2024",
				},
				{
					name: "AI ASSISSTANT",
					html_url: "",
					description: "ai chat assisstant",
					type: "web app",
					language: "Vue+Python",
					updated_at: "AUG 2024",
				},
				{
					name: "NEWS ANALYSER",
					html_url: "",
					description: "news analyser",
					type: "web app",
					language: "Streamlit+Python",
					updated_at: "MAY 2021",
				},
			],
			loading: true,
			error: null,
			selectedOption: "aboutMe",
			currentTheme: "light",
			asciiEffectEnabled: false,
			currentParticleImage: "",
			customCursor: `url(${customCursorDark}) 16 16, pointer`,
			loaderVisible: true,
			mainContentVisible: false,
		};
	},
	computed: {
		isDarkTheme() {
			return this.currentTheme === "dark";
		},
	},
	watch: {
		// Watch for changes in the selectedOption to add/remove scroll listener dynamically
		selectedOption(newOption) {
			if (newOption === "projects") {
				this.attachScrollListener();
			} else {
				this.detachScrollListener();
			}
		},
	},
	async mounted() {
		setTimeout(() => {
			this.loaderVisible = false; // Hide loader after 1 second
		}, 1000);
		if (this.selectedOption === "projects") {
			this.attachScrollListener();
		}
		try {
			// const response = await axios.get(
			// 	`${process.env.VUE_APP_API_URL}/projects`
			// );
			// this.projects = response.data.projects;
		} catch (err) {
			console.log(err);
			this.error = "Failed to load projects.";
		} finally {
			setTimeout(2000);
			this.loading = false;
		}
	},
	beforeUnmount() {
		this.detachScrollListener();
	},
	methods: {
		showMainContent() {
			this.mainContentVisible = true; // Show main content after loader disappears
		},
		attachScrollListener() {
			const contentDiv = this.$refs.contentDiv;
			console.log("attaching to ", contentDiv);
			if (contentDiv) {
				contentDiv.addEventListener("scroll", this.handleScroll);
			}
		},
		// Detach the scroll listener
		detachScrollListener() {
			const contentDiv = this.$refs.contentDiv;
			if (contentDiv) {
				contentDiv.removeEventListener("scroll", this.handleScroll);
			}
		},
		// Handle the scroll event
		handleScroll(event) {
			const contentDiv = event.target;
			console.log("Scroll Top:", contentDiv.scrollTop);
			console.log("Scroll Height:", contentDiv.scrollHeight);
			console.log("Client Height:", contentDiv.clientHeight);
		},
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

			this.customCursor =
				this.currentTheme === "dark"
					? `url(${customCursorLight}) 16 16, pointer`
					: `url(${customCursorDark}) 16 16, pointer`;
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
/* Global styles for lists and links */
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
	font-size: 5vw; /* Responsive font size */
	margin: 0 5px;
	text-align: left;
	font-weight: 400;
}

.wrapper {
	position: relative;
	border: 1px solid rgb(187, 187, 187);
	margin: 20px;
	height: calc(100vh - 60px);
	max-width: 90%; /* Ensures the wrapper fits within screen bounds */
	overflow: hidden; /* Prevent overflow */

	@media (min-width: 768px) {
		max-width: none; /* Original width for larger screens */
	}
}

.about-me-text {
	font-weight: 400;
	font-size: 2.5vw !important;
}

.text {
	position: relative;
	font-family: "Roboto mono", sans-serif;
	padding: 0 20px 20px 20px;
	font-size: 4vw; /* Responsive font size */
	text-align: left; /* Center align text for smaller screens */
	display: flex;
	flex-direction: row;
	height: 100%;
	gap: 80px;

	@media (min-width: 768px) {
		text-align: left;
	}
}

.job {
	font-size: 2vw; /* Responsive font size */
	font-weight: 600;
	color: var(--text-color);
	margin: 20px 5px;
}

li {
	margin-top: 5px;
	transition: 0.15s ease;
	width: fit-content;
	color: var(--text-color);
	text-align: center; /* Center-align text on mobile */

	a {
		text-decoration: none;
		gap: 10px;
		display: flex;
		align-items: center;
		justify-content: flex-end; /* Center-align links on mobile */
		text-align: right;
	}

	img {
		width: 20px; /* Smaller icon size for mobile */
		height: 20px;

		@media (min-width: 768px) {
			width: 24px; /* Original size for tablets and above */
			height: 24px;
		}
	}
}

.sections {
	margin: 20px 5px;
	font-size: 3vw; /* Smaller font for mobile */
	font-weight: 800;

	.selected {
		color: rgb(187, 187, 187);
	}

	li:hover {
		color: rgb(187, 187, 187);
	}

	@media (min-width: 768px) {
		font-size: 3vw;
	}
}

.left-side {
	margin-top: 20px;
}

.content {
	overflow-x: hidden; /* Prevent horizontal overflow */
	overflow-y: auto;
	flex: 1; /* Take up remaining space */
	-ms-overflow-style: none; /* Hide scrollbar for Internet Explorer and Edge */
	scrollbar-width: none; /* Hide scrollbar for Firefox */

	/* For WebKit browsers (Chrome, Safari, etc.) */
	&::-webkit-scrollbar {
		display: none; /* Hide scrollbar */
	}

	& > div {
		font-size: 2vw;
		text-align: right;
	}

	ul {
		display: flex;
		flex-direction: column;
		align-items: flex-end;
		gap: 20px;

		li {
			font-size: 5vw;
			div {
				display: flex;
				flex-direction: row;
				justify-content: flex-end;
				gap: 20px;
				font-size: 4vw;
			}
		}

		span {
			font-size: 2vw;
		}
	}
}

.side-buttons {
	display: none;
	flex-direction: column; /* Stack vertically for smaller screens */
	gap: 10px;
	position: fixed;
	bottom: 10px;
	left: 50%; /* Center on mobile */
	transform: translateX(-50%);

	@media (min-width: 768px) {
		display: flex;
		flex-direction: row; /* Horizontal alignment for tablets and above */
		bottom: 180px;
		left: -60px;
		transform: rotate(-90deg);
	}

	.theme-toggle,
	.ascii-toggle {
		width: fit-content;
		color: var(--text-color);
	}
}

/* Border color matches the theme */
.wrapper {
	border-color: var(--text-color);
}

/* Additional responsive adjustments */
@media (max-width: 767px) {
	.sections {
		font-size: 3vw;
	}
	h1 {
		font-size: 7vw;
	}
	.job {
		font-size: 4vw;
	}
	.content > div {
		font-size: 4vw;

		ul {
			li {
				font-size: 8vw;
				div {
					gap: 10px;
				}
			}
			span {
				font-size: 4vw;
			}
		}
	}
	.text {
		flex-direction: column;
		justify-content: flex-start;
		gap: 20px;
	}
}

@media (min-width: 768px) and (max-width: 1024px) {
	.wrapper {
		margin: 40px; /* Adjust the margin for tablets */
		height: calc(100vh - 83px);
	}
	.sections {
		font-size: 3vw;
	}
	h1 {
		font-size: 7vw;
	}
	.job {
		font-size: 4vw;
	}
	.content > div {
		font-size: 4vw;
		ul li div {
			gap: 10px;
		}
	}
	.text {
		flex-direction: column;
		justify-content: flex-start;
		gap: 20px;
	}
}

@media (min-width: 1025px) {
	.sections {
		font-size: 1.5vw;
	}
}

@keyframes fade-left-right {
	from {
		opacity: 1;
	}
	to {
		opacity: 0;
	}
}

@keyframes fade {
	from {
		opacity: 0;
	}
	to {
		opacity: 1;
	}
}

/* Apply animation when loader is entering */
.fade-left-right-enter-active {
	animation: fade-left-right 0.5s forwards;
}

/* Apply animation when loader is leaving */
.fade-left-right-leave-active {
	animation: fade-left-right 0.5s forwards;
}

.fade-enter-active {
	animation: fade 0.5s forwards;
}
.fade-leave-active {
	animation: fade 0.5s forwards;
}

</style>
