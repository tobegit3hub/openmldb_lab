<template>

<div class="Playground">


  <div id="plaground_notebook">
    
    <h2>OpenMLDB Playground</h2>
    
    <div id="control_block">
      <form name="control_block_form">
        
        <el-button type="primary" @click="addEmptyBlock" icon="el-icon-folder-add" id="addBlockButton">Add Block</el-button>



        <input type="file" ref="importNotebookJsonInputFile" @change="importNotebookJson" />

    
        <!-- Hide the file input and trigger by following button 
        <input type="file"
               id="upload_notebook_json"
               :ref="doc"
               style="display: none;"
               @change="readFile">
        <el-button icon="el-icon-upload2" onclick="document.control_block_form.upload_notebook_json.click()">Import Notebook</el-button>
        -->
        
        <el-button @click="exportNotebookJson" icon="el-icon-download">Export Notebook</el-button>

      </form>
    </div>
    
    <div class="notebook_blocks">
      
      <div v-for="block in blocks" :key="block.id" class="notebook_block">
        <form>
          <el-input
            type="textarea"
            v-model=block.text>
          </el-input>
          
          <el-button type="primary" icon="el-icon-search"></el-button>      
          <el-button type="danger" icon="el-icon-delete" @click="deleteCurrentBlock(block.id)"></el-button>
        </form>
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
      var index = this.blocks.findIndex(block => block.id == blockId)
      this.$delete(this.blocks, index)
    },
    
    exportNotebookJson() {
      const data = JSON.stringify(this.blocks)
      //window.localStorage.setItem('arr', data);
      //console.log(JSON.parse(window.localStorage.getItem('arr')))
      
      const blob = new Blob([data], {type: 'text/plain'})
      const e = document.createEvent('MouseEvents'),
      a = document.createElement('a');
      a.download = "test.json";
      a.href = window.URL.createObjectURL(blob);
      a.dataset.downloadurl = ['text/json', a.download, a.href].join(':');
      e.initEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
      a.dispatchEvent(e);
    },
    
    importNotebookJson() {
      this.file = this.$refs.importNotebookJsonInputFile.files[0];
      const reader = new FileReader();

      if (this.file.name.includes(".json")) {
        reader.onload = (res) => {
          // TODO: Handle json with incorrect format
          const jsonObject = JSON.parse(res.target.result);
          this.blocks = jsonObject
          
          this.$message({
                    message: "Success to load notebook file",
                    type: "success"
                  });
        };
        
        reader.onerror = (err) => console.log(err);
        reader.readAsText(this.file);
      } else {
        this.$message.error("Only support json file");
      }
      
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
  
  #addBlockButton {
    margin-right: 10px;
  }
  
</style>
