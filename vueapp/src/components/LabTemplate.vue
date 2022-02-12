<template>

<div class="Lab">

    <h2>{{ title }}</h2>
    
    <p>{{ subtitle }}</p>

    <Notebook :builtinBlocks="builtinBlocks"></Notebook>
    
</div>

</template>

<script>

import Notebook from './Notebook.vue'
  
export default {
  name: 'LabTemplate',
  components: {
    Notebook
  },
  props: {
    title: String,
    subtitle: String,
    labFile: String,
  },
  data: function() {
    return {
      builtinBlocks: []
    }
  },
  created() {
    this.loadLabFile(this.labFile)
  },
  methods: {
    loadLabFile(fileName) {
      const xhr = new XMLHttpRequest()
      const okStatus = document.location.protocol === 'file:' ? 0 : 200
      xhr.open('GET', fileName, false)
      xhr.overrideMimeType('text/html;charset=utf-8')
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
