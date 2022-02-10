<template>

<div class="console">
  
  <el-row :gutter="24">
    <el-col :span="6">
      <div class="grid-content db_list">
        <h3>Databases</h3>

        <template>
          <el-table
            :data="databaseListData"
            highlight-current-row
            style="width: 100%">
            <el-table-column
              prop="name">
            </el-table-column>
          </el-table>
        </template>
        
      </div>
    </el-col>
    
    
    <el-col :span="6">
      <div class="grid-content table_list">
        <h3>Tables</h3>
        
        <template>
          <el-table
            :data="tableListData"
            highlight-current-row
            style="width: 100%">
            <el-table-column
              prop="name">
            </el-table-column>
          </el-table>
        </template>
        
        
      </div>
    </el-col>
    
    <el-col :span="12">
      <div class="grid-content table_info">
        <h3>Table Info</h3>
        
      </div>
    </el-col>
  </el-row>
  

  
  <div class="execute_sql">
    <h2> Execute Query SQL</h2>
    <p>select * from db1.table_test</p>
    <el-input v-model="sql" placeholder="SELECT * FROM t1;" />
    <el-button type="primary" @click="querySql" >
      Run
    </el-button>
    <div class="sql_result">
    <p>SQL Result</p>
    <ul>
      <li v-for="row in sqlResultRows" :key="row">
        {{ row }}
      </li>
    </ul>
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
     fetch("http://127.0.0.1:5000/api/tables")
               .then(response => response.json())
               .then(json => {
                 this.tableListData = json.tables
               })
  },
  data: function() {
    return {
      databaseListData: [{name: "db1"}, {name: "db2"}, {name: "db3"}, {name: "db4"}],
      tableListData: [],
      sql: "",
      sqlResultRows: []
    }
  },
  methods: {
    querySql() {
      fetch("http://127.0.0.1:5000/api/querysql?sql=" + this.sql)
        .then(response => response.json())
        .then(json => {
          this.sqlResultRows = json.rows
        })
    }
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
</style>
