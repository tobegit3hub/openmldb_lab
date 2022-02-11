<template>

<div class="Playground">


  <div id="plaground_notebook">
    <h2>OpenMLDB Playground</h2>
    
    <div id="control_block">
      <el-button>Import Notebook</el-button>
      <el-button>Export Notebook</el-button>
      <el-button>Add Text Block</el-button>
      <el-button>Add SQL Block</el-button>
      
    </div>
    
    <div class="notebook_block">
      <el-input
        type="textarea"
        placeholder="请输入内容"
        v-model="textarea1"
        show-word-limit
      >
      </el-input>

      <el-button type="primary" icon="el-icon-search" circle></el-button>      
      <el-button type="danger" icon="el-icon-delete" circle></el-button>
    </div>
    
    <div class="notebook_block">
      <el-input
        type="textarea"
        placeholder="请输入内容"
        v-model="textarea2"
        show-word-limit
      >
      </el-input>
      
      <el-button>Run</el-button>
      
      <el-button>Delete</el-button>
    </div>
    
  </div>
  </div>

</template>

<script>
export default {
  name: 'Playground',
  data: function() {
    return {
      textarea1: "",
      textarea2: "",

    }
  },
  methods: {
    executeCreateDbSql() {
      fetch("http://127.0.0.1:5000/api/executesql?sql=" + this.createDbSql)
        .then(response => response.json())
        .then(json => {
          this.createDbSqlSuccess = json.success
          if (typeof json.error != "undefined") {
            this.createDbSqlError = json.error
          }
        })
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
