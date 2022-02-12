<template>

<div class="NotebookPage">

    <h2>OpenMLDB Notebook</h2>

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
      builtinBlocks: [{id: 0, sql: 'SELECT 100, "foo"', success: null, is_query: null, resultSchema: null, resultRows: null}],
    }
  },
  methods: {
    
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
