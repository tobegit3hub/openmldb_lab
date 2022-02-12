<template>

<div class="Notebook">
    
    <div id="control_block">
      <form name="control_block_form">
        
        <el-button type="primary" @click="addEmptyBlock" icon="el-icon-folder-add" id="addBlockButton">Add Block</el-button>

        <!-- Hide the file input and trigger by following button -->
        <input type="file" 
          ref="importNotebookJsonInputFile" 
          @change="importNotebookJson" 
          id="upload_notebook_json"
          style="display: none;"
          />
        <el-button icon="el-icon-upload2" onclick="document.control_block_form.upload_notebook_json.click()">Import Notebook</el-button>
        
        <el-button @click="exportNotebookJson" icon="el-icon-download">Export Notebook</el-button>

      </form>
    </div>
    
    <div id="step_bar">
      
      <el-steps :active="successBlockIndex" align-center finish-status="success">
          <el-step v-for="(block, index) in blocks" :key="block.id" :title="'Step ' + (index + 1)"></el-step>
      </el-steps>
      
    </div>
    
    <div class="notebook_blocks">
      
      <div v-for="block in blocks" :key="block.id" class="notebook_block">

          <el-row :gutter="24">
            <el-col :span="23">
              <el-input
                type="textarea"
                v-model=block.sql>
              </el-input>
            </el-col>
            
            <el-col :span="1">
              <div v-if="block.success != null">
                <el-button v-if="block.success == true" slot="reference" type="success" icon="el-icon-success"></el-button>
                <el-button v-else slot="reference" type="danger" icon="el-icon-error"></el-button>
              </div>
            </el-col>
          </el-row>
          
          <div>
            <el-button type="primary" 
              icon="el-icon-search" 
              style="margin-top: 10px;"
              @click="executeSql(block.id, block.sql)">Run</el-button>      
            
            <el-popconfirm
              title="Confirm to clear output?"
              @confirm="clearCurrentBlock(block.id)">
              <el-button slot="reference" type="warning" icon="el-icon-refresh-left" style="margin-left: 10px;">Clear</el-button>
            </el-popconfirm>
            
            <el-popconfirm
              title="Confirm to delete?"
              @confirm="deleteCurrentBlock(block.id)">
              <el-button slot="reference" type="danger" icon="el-icon-delete" style="margin-left: 10px;">Delete</el-button>
            </el-popconfirm>
            
          </div>
          
        <div id="execute_sql_result">
          
            <div v-if="block.success != null && block.success == true && block.is_query == true" style="margin-top: 20px;">
              <el-table
                :data="block.resultRows"
                stripe
                border
                style="width: 100%">
              
                <template v-for='(schema) in block.resultSchema'>
                  <el-table-column
                    sortable
                    :show-overflow-tooltip="true"
                    :prop="schema.name"
                    :label="schema.name + '(' + schema.type + ')'"
                    :key="schema.name">
                  </el-table-column>
                </template>
              </el-table>
            </div>

        </div>
        
      </div>
        
    </div>
    
  </div>

</template>

<script>
export default {
  name: 'Notebook',
  props: {
    builtinBlocks: Array
  },
  data: function() {
    return {
      /**
       * Example struct of block.
       * {
       *    id: 0,
       *    sql: SELECT 100, "foo"},
       *    success: True,
       *    is_query: True,
       *    resultSchema: [],
       *    resultRows: []
       * }
       */
      blocks: [],
      newBlockIndex: 1,
      // Record the largest index of successful blocks
      successBlockIndex: 0,
    }
  },
  mounted() {
    if (this.builtinBlocks != null) {
      this.blocks = this.builtinBlocks
    }
  },
  methods: {
    addEmptyBlock() {
      this.blocks.push({id: this.newBlockIndex, sql: "", success: null, is_query: null, resultSchema: null, resultRows: null})
      this.newBlockIndex++
    },
    
    deleteCurrentBlock(blockId) {      
      var index = this.blocks.findIndex(block => block.id == blockId)
      this.$delete(this.blocks, index)
    },
    
    clearCurrentBlock(blockId) {
      var index = this.blocks.findIndex(block => block.id == blockId)
      this.blocks[index]["success"] = null
      this.blocks[index]["is_query"] = null
      this.blocks[index]["resultSchema"] = null
      this.blocks[index]["resultRows"] = null
    },
    
    exportNotebookJson() {
      const data = JSON.stringify(this.blocks)
      //window.localStorage.setItem('arr', data);
      //console.log(JSON.parse(window.localStorage.getItem('arr')))
      
      const blob = new Blob([data], {type: 'text/plain'})
      const e = document.createEvent('MouseEvents'),
      a = document.createElement('a');
      a.download = "openmldb_notebook.json";
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
        
        reader.onerror = (err) => {
          this.$message.error(err);
        }
        reader.readAsText(this.file);
      } else {
        this.$message.error("Only support json file");
      }
    },
    
    executeSql(blockId, sqlText) {
      const requestOptions = {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({sql: sqlText})
        };
      
      var index = this.blocks.findIndex(block => block.id == blockId)
      var is_query = sqlText.toLowerCase().startsWith("select")
      this.blocks[index]["is_query"] = is_query
      
      fetch("http://127.0.0.1:5000/api/executesql", requestOptions)
        .then(response => response.json())
        .then(json => {
          if (json.success == false) {
            this.$message.error(json.error);
            this.blocks[index]["success"] = false
          } else {
            this.$message({
              message: "Success to execute: " + sqlText,
              type: "success"
            });
            
            this.blocks[index]["success"] = true
            this.blocks[index]["resultSchema"] = json.schema
            this.blocks[index]["resultRows"] = json.rows
            
            this.updateStepIndex()
          }
        })
    },
    
    updateStepIndex() {
      var index = 0;
      for (const block of this.blocks) {
        if (block["success"] != null && block["success"] == true) {
          index++
        } else {
          break
        }
      }
      this.successBlockIndex = index;
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
  margin-top: 50px;
  padding-top: 20px;
  padding-bottom: 20px;
  padding-left: 20px;
  padding-right: 50px;
  border: solid;
  border-width:thin;
  box-shadow: 5px 5px 5px rgba(0,0,0,0.1);
  border-color: beige;
}

#addBlockButton {
  margin-right: 10px;
}

#step_bar {
  margin-top: 30px;
}
  
.Notebook {
  padding-left: 30px;
  padding-right: 30px;
}
</style>
