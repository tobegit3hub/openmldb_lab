<template>
  <div id="app">

  <el-menu
    class="el-menu-demo"
    mode="horizontal"
    @select="handleSelect"
    background-color="#545c64"
    text-color="#fff"
    active-text-color="#ffd04b">
    <el-menu-item index="1">Console</el-menu-item>
    <el-submenu index="2">
      <template slot="title">Labs</template>
      <el-menu-item index="2-1">Lab1: Basic SQL</el-menu-item>
      <el-menu-item index="2-2">Lab2: Online/Offline Mode</el-menu-item>
      <el-menu-item index="2-3">Lab3: End-to-end Demo</el-menu-item>
    </el-submenu>
    <el-menu-item index="3">Playground</el-menu-item>
    <el-menu-item index="4">SQL Debugger</el-menu-item>
    <el-menu-item index="5"><a href="https://github.com/tobegit3hub/openmldb_lab" target="_blank">Github</a></el-menu-item>
  </el-menu>
  
	<Console v-if="activeIndex=='1'"/>
  <Lab1 v-if="activeIndex=='2-1'" />
  <Lab2 v-if="activeIndex=='2-2'" />
  
  </div>
</template>

<script>
import Console from './components/Console.vue'
import Lab1 from './components/Lab1.vue'
import Lab2 from './components/Lab2.vue'

export default {
  name: 'App',
  components: {
    Console,
    Lab1,
    Lab2,
  },
  data() {
    return {
      activeIndex: '1',
    };
  },
  methods: {
    handleSelect(key, keyPath) {
      console.log(key, keyPath)
      this.activeIndex = key
    }
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
}
</style>
