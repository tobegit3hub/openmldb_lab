<template>

<div class="Playground">


  <div id="plaground_notebook">
    
    <h2>OpenMLDB Playground</h2>
    
    <div id="control_block">
      <el-button>Import Notebook</el-button>
      <el-button>Export Notebook</el-button>
      <el-button @click="addEmptyBlock">Add SQL Block</el-button>
      
    </div>
    
    <div class="notebook_blocks">
      
      <div v-for="block in blocks" :key="block.id" class="notebook_block">
        
        <el-input
          type="textarea"
          v-model=block.text
        >
        </el-input>
        
        <el-button type="primary" icon="el-icon-search"></el-button>      
        <el-button type="danger" icon="el-icon-delete" @click="deleteCurrentBlock(block.id)"></el-button>
        
      </div>
        
    </div>
    
  </div>
  </div>

</template>

<script>
export default {
  name: 'Playground',
  data: function() {
    return {
      blocks: [{id: 0, text: "select * from t1"}],
      newBlockIndex: 1,
    }
  },
  methods: {
    addEmptyBlock() {
      this.blocks.push({id: this.newBlockIndex, text: ""})
      this.newBlockIndex++
    },
    
    deleteCurrentBlock(blockId) {
      console.log("Call delete current block, id: " + blockId)
      
      var index = this.blocks.findIndex(block => block.id == blockId)
      
      this.$delete(this.blocks, index)
    },
        
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}

  .el-row {
    margin-bottom: 20px;
    &:last-child {
      margin-bottom: 0;
    }
  }
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
  }
  
  #plaground_notebook {
    margin-top: 30px;
    margin-left: 100px;
    margin-right: 100px;
  }
  
  .notebook_block {
    margin-top: 30px;
  }
  
</style>
