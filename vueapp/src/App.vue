<template>
  <div id="app">
    <!-- 
    <img alt="Vue logo" src="./assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
	-->
	<Console />
  <Lab1 />
  </div>
</template>

<script>
import Console from './components/Console.vue'
import Lab1 from './components/Lab1.vue'

export default {
  name: 'App',
  components: {
    Console,
    Lab1
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
