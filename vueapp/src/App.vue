<template>
  <div id="app">

  <el-menu
    :default-active="activeIndex"
    class="el-menu-demo"
    mode="horizontal"
    @select="handleSelect"
    background-color="#545c64"
    text-color="#fff"
    active-text-color="#ffd04b">
    <el-menu-item index="1">Console</el-menu-item>
    <el-submenu index="2">
      <template slot="title">Lab</template>
      <el-menu-item index="2-1">Lab1</el-menu-item>
    </el-submenu>
    <el-menu-item index="3"><a href="https://github.com/tobegit3hub/openmldb_lab" target="_blank">Github</a></el-menu-item>
  </el-menu>
  
  
	<Console v-if="show_console"/>
  <Lab1 v-if="show_lab1" />
  
  
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
  },
  data() {
    return {
      activeIndex: '1',
      show_console: true,
      show_lab1: false,
    };
  },
  methods: {
    handleSelect(key, keyPath) {
      console.log(key, keyPath);
      if (key == "1") {
        this.show_console = true
        this.show_lab1 = false
      } else if (key == "2-1") {
        this.show_console = false
        this.show_lab1 = true
      }
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
