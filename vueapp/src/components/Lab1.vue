<template>

<div class="Lab">

    <h2>Lab1: Basic SQL</h2>
    
    <p>Introduction: use basic SQL operations.</p>

    <Notebook :builtinBlocks="builtinBlocks"></Notebook>
    
</div>

</template>

<script>

import Notebook from './Notebook.vue'
  
export default {
  name: 'NotebookPage',
  components: {
    Notebook
  },
  data: function() {
    return {
      builtinBlocks: [],
    }
  },
  created() {
    const fileName = "lab1.json"
    this.loadLabFile(fileName)
    
  },
  methods: {
    loadLabFile(fileName) {
      const xhr = new XMLHttpRequest()
      const okStatus = document.location.protocol === 'file:' ? 0 : 200
      xhr.open('GET', fileName, false)
      xhr.overrideMimeType('text/html;charset=utf-8')// 默认为utf-8
      xhr.send(null)
      if(xhr.status === okStatus) {
        const blocksStr = xhr.responseText
        this.builtinBlocks = JSON.parse(blocksStr)
      } else {
        this.$message.error("Fail to load lab file: " + fileName);
      }
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
