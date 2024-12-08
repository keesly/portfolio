<template>
  <div class="loader-container">
    <div class="loader-textbox">
      <span>Mark Ryzhov</span> Portfolio
    </div>
  </div>
</template>


<script>
import "@/assets/fonts/fonts.css";

export default {
	name: "LoaderText",
	data() {
		return {};
	},

	watch: {},
	mounted() {},
	beforeUnmount() {},
	methods: {},
};
</script>

<style scoped lang="scss">

.loader-textbox {
  font-family: "Roboto mono", sans-serif;
  font-size: 2vw;
  span {
    font-weight: 800;
  }
} 

.loader-container {
  z-index: 9000;
	position: fixed;
	top: 50%;
	left: 50%;
	transform: translate(-50%, -50%);
	width: 40%;
	height: 100px;
	background-color: white;
	display: flex;
	justify-content: center;
	align-items: center;
	opacity: 1;
	transition: opacity 0.5s ease-out;
}

.loader-container.fade-out {
	opacity: 0;
}

.loader-container .loader-text {
	font-size: 1.5rem;
	color: #333;
}
</style>
