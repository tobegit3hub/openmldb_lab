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
    <el-menu-item index="2">Notebook</el-menu-item>
    <el-submenu index="3">
      <template slot="title">Labs</template>
      <el-menu-item index="3-1">Lab1: Basic SQL</el-menu-item>
      <el-menu-item index="3-2">Lab2: Online/Offline Mode</el-menu-item>
      <el-menu-item index="3-3">Lab3: End-to-end Demo</el-menu-item>
    </el-submenu>
    <!-- TODO: Support sql debugger with sql compiler api -->
    <!-- <el-menu-item index="4">SQL Debugger</el-menu-item> -->
    <el-menu-item index="5">Task Manager</el-menu-item>

    <el-submenu index="7" id="github_submenu">
      <template slot="title">Github</template>
      <el-menu-item index="7-1"><el-link type="primary" href="https://github.com/4paradigm/openmldb" target="_blank">OpenMLDB</el-link></el-menu-item>
      <el-menu-item index="7-2"><el-link type="primary" href="https://github.com/tobegit3hub/openmldb_lab" target="_blank">OpenMLDB Lab</el-link></el-menu-item>
    </el-submenu>
    
    <el-submenu index="6" id="settings_submenu">
      <template slot="title">Settings</template>
      <el-menu-item index="6-1"><el-button type="text" @click="changeOpenmldbServer">OpenMLDB Server</el-button></el-menu-item>
    </el-submenu>
    
  </el-menu>
  
	<Console v-if="activeIndex=='1' || activeIndex==null || activeIndex=='6-1'" />
  <NotebookPage v-if="activeIndex=='2'" />
  <Lab1 v-if="activeIndex=='3-1'" />
  <Lab2 v-if="activeIndex=='3-2'" />
  <Lab3 v-if="activeIndex=='3-3'" />
  <TaskManager v-if="activeIndex=='5'" />
  
  </div>
</template>

<script>
import Console from './components/Console.vue'
import NotebookPage from './components/NotebookPage.vue'
import Lab1 from './components/Lab1.vue'
import Lab2 from './components/Lab2.vue'
import Lab3 from './components/Lab3.vue'
import TaskManager from './components/TaskManager.vue'

export default {
  name: 'App',
  components: {
    Console,
    NotebookPage,
    Lab1,
    Lab2,
    Lab3,
    TaskManager,
  },
  data() {
    return {
      activeIndex: '1',
    };
  },
  methods: {
    handleSelect(key, keyPath) {
      this.activeIndex = key
      keyPath
    },
    
    changeOpenmldbServer() {
      this.$prompt('Please update OpenMLDB endpoint(eg. "127.0.0.1:2181/openmldb")', 'Notice', {
        confirmButtonText: 'Update',
        cancelButtonText: 'Cancel',
      }).then(({ value }) => {

        const requestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({openmldb_server: value})
          };
        
        fetch("http://127.0.0.1:7788/api/server", requestOptions)
          .then(response => response.json())
          .then(json => {
            if (json.success == false) {
              this.$message.error(json.error)
            } else {
              // Success to update OpenMLDB server
              this.$message({
                type: 'success',
                message: 'Update OpenMLDB server: ' + value
              });
              
              // TODO: Does not work to update Console page with new OpenMLDB server
              // this.$forceUpdate()
              location.reload()
            }
          })
        
      }).catch(() => {
        this.$message({
          type: 'info',
          message: 'Cancel update server'
        });       
      });
    },
          
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

#settings_submenu {
  float: right;
}

#github_submenu{
  float: right;
}
</style>
