<template>

<div class="console">
  
  <div id="openmldb_data_info">
    <br/>
    <h2>OpenMLDB Console</h2>
    
    <el-row :gutter="24">
      <el-col :span="5">
        <div class="grid-content db_list">
          <h3>Databases</h3>

          <template>
            <el-table
              ref="databaseListTable"
              :data="databaseListData"
              highlight-current-row
              @current-change="handleSelectDb"
              style="width: 100%">
              <el-table-column
                align="center"
                prop="name">
              </el-table-column>
            </el-table>
          </template>
          
        </div>
      </el-col>
      
      <el-col :span="5">
        <div class="grid-content table_list">
          <h3>Tables</h3>
          
          <template>
            <el-table
              ref="tableListTable"
              :data="tableListData"
              highlight-current-row
              @current-change="handleSelectTable"
              style="width: 100%">
              <el-table-column
                align="center"
                prop="name">
              </el-table-column>
            </el-table>
          </template>
          
        </div>
      </el-col>
      
      <el-col :span="14">
        <div class="grid-content table_data">
          <h3>Table Data</h3>
          
          <el-table
            :data="tableDataList"
            stripe
            style="width: 100%">
          
            <template v-for='(schema) in tableDataSchemaList'>
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
      </el-col>
    </el-row>
  </div>
  
  <br />
  
  <div class="execute_sql">
    <h2> Execute SQL</h2>
    
    <div id="execute_sql_input">

      <el-input placeholder="SELECT * FROM t1" v-model="executeSqlText" @keyup.enter.native="executeSql">
      <el-select id="execute_sql_select_mode" v-model="execute_sql_mode" slot="prepend" placeholder="Mode">
        <el-option label="Online Mode" value="1"></el-option>
        <el-option label="Offline Mode" value="2"></el-option>
      </el-select>
        <el-button slot="append" icon="el-icon-search" @click="executeSql"></el-button>
      </el-input>
    </div>
    
    <div id="execute_sql_result">
      <el-table
        :data="executeSqlDataList"
        stripe
        border
        style="width: 100%">
      
        <template v-for='(schema) in executeSqlSchemaList'>
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

</template>

<script>
export default {
  name: 'Console',
  props: {
    msg: String
  },
  created() {
    this.refreshDbList()
    this.refreshTableList()
  },
  data: function() {
    return {
      databaseListData: [],
      selectedDb: null,
      selectedDbItem: null,
      tableListData: [],
      selectedTable: null,
      selectedTableItem: null,
      tableDataList: [],
      tableDataSchemaList: [],
      execute_sql_mode: "online",
      executeSqlText: "",
      executeSqlDataList: [],
      executeSqlSchemaList: [],
    }
  },
  
  watch: {
    databaseListData: function () {
      this.$nextTick(function() {
        if (this.databaseListData.length > 0) {
          if (this.selectedDbItem == null) {
            // Set default selected database
            this.$refs.databaseListTable.setCurrentRow(this.databaseListData[0])
            this.selectedDbItem = this.databaseListData[0]
            this.selectedDb = this.selectedDbItem.name
          } else {
            // TODO: This does not work when inserting new item
            this.$refs.databaseListTable.setCurrentRow(this.selectedDbItem)
            this.selectedDb = this.selectedDbItem.name
          }
        }
      })
    },
    
    tableListData: function () {
      this.$nextTick(function() {
        if (this.selectedTableItem == null) {
          this.$refs.tableListTable.setCurrentRow(this.tableListData[0])
        }
      })
    },
  },
  
  methods: {
    notifyError(errorMessage) {
      this.$message.error(errorMessage);
    },
    
    notifySuccess(sqlText) {      
      this.$message({
        message: "Success to execute: " + sqlText,
        type: "success"
      });
    },  
    
    refreshDbList() {
      fetch("http://127.0.0.1:7788/api/dbs")
                .then(response => response.json())
                .then(json => {
                  this.databaseListData = json.databases
                })        
    },
    
    handleSelectDb(val) {
      if (val != null) {
        var dbName = val.name
        this.selectedDb = dbName
        this.selectedDbItem = val
        this.refreshTableList(dbName)
        
        this.updateDefaultDb(dbName)
      }
    },
    
    updateDefaultDb(dbName) {
      const requestOptions = {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({db: dbName})
        };
      
      fetch("http://127.0.0.1:7788/api/defaultdb", requestOptions)
        .then(response => response.json())
        .then(json => {
          return json.success
        })
    },
    
    refreshTableList(dbName) {
      fetch("http://127.0.0.1:7788/api/tables?db=" + dbName)
        .then(response => response.json())
        .then(json => {
          if (json.success == false) {
            this.notifyError(json.error)
          } else {
            this.tableListData = json.tables
          }
        })
    },
    
    handleSelectTable(val) {
      if (val != null) {
        var tableName = val.name
        this.selectedTable = tableName
        this.selectedTableItem = val
        this.refreshTableData(tableName)
      }
    },
    
    refreshTableData(tableName) {    
      fetch("http://127.0.0.1:7788/api/tabledata?table=" + tableName)
        .then(response => response.json())
        .then(json => {
          if (json.success == false) {
            this.notifyError(json.error)
          } else {
            this.tableDataList = json.rows
            this.tableDataSchemaList = json.schema
          }
        })
    },
    
    executeSql() {
      
      const requestOptions = {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({sql: this.executeSqlText})
        };
      
      fetch("http://127.0.0.1:7788/api/executesql", requestOptions)
        .then(response => response.json())
        .then(json => {
          if (json.success == false) {
            this.notifyError(json.error)
          } else {
            this.notifySuccess(this.executeSqlText)
            if (json.query_sql) {
              this.executeSqlDataList = json.rows
              this.executeSqlSchemaList = json.schema
            } else {
              this.refreshDbList()
              this.refreshTableList(this.selectedDb)
              this.refreshTableData(this.selectedTable)    
            }
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

  /* Refer to https://element.eleme.cn/#/zh-CN/component/layout */
  .el-row {
    margin-bottom: 20px;
    &:last-child {
      margin-bottom: 0;
    }
  }
  .el-col {
    border-radius: 4px;
  }
  .bg-purple-dark {
    background: #99a9bf;
  }
  .bg-purple {
    background: #d3dce6;
  }
  .bg-purple-light {
    background: #e5e9f2;
  }
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
  }
  .row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
  }

#execute_sql_select_mode {
  /* TODO: Not work to set select width */
  width: 130px;
}
  
#openmldb_data_info {
  margin-top: 10px;
  margin-left: 30px;
  margin-right: 30px;
}

#execute_sql_input {
  margin-left: 100px;
  margin-right: 100px;
}
  
#execute_sql_result {
  margin-top: 30px;
  margin-left: 100px;
  margin-right: 100px;
}
</style>
