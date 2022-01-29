<template>

<div class="lab2">

  <h2>Lab 2</h2>
  <p>Introduction: use basic SQL operations</p>

  <div class="step">
    <p>Step1: Create test database</p>
    <el-input v-model="createDbSql" />
    <el-button type="primary" @click="executeCreateDbSql">Run</el-button>
    <p v-if="createDbSqlSuccess!=null">Success: {{ createDbSqlSuccess }}</p>
    <p v-if="createDbSqlSuccess==false">Error: {{ createDbSqlError }}</p>
  </div>
  
  <div class="step">
    <p>Step2: Create test table</p>
    <el-input v-model="createTableSql" />
    <el-button type="primary" @click="executeCreateTableSql">Run</el-button>
    <p v-if="createTableSqlSuccess!=null">Success: {{ createTableSqlSuccess }}</p>
    <p v-if="createTableSqlSuccess==false">Error: {{ createTableSqlError }}</p>
  </div>

  <div class="step">
    <p>Step3: Insert data into table</p>
    <el-input v-model="insertSql" />
    <el-button type="primary" @click="executeInsertSql">Run</el-button>
    <p v-if="insertSqlSuccess!=null">Success: {{ insertSqlSuccess }}</p>
    <p v-if="insertSqlSuccess==false">Error: {{ insertSqlError }}</p>
  </div>
  
  <div class="step">
    <p>Step4: Select data from table</p>
    <el-input v-model="selectSql" />
    <el-button type="primary" @click="executeSelectSql">Run</el-button>
    <p v-if="selectSqlSuccess!=null">Success: {{ selectSqlSuccess }}</p>
    <p v-if="selectSqlSuccess==false">Error: {{ selectSqlError }}</p>
    <p>Result of {{ selectSql }}: </p>
    <ul>
      <li v-for="row in selectResultRows" :key="row">
        {{ row }}
      </li>
    </ul>
  </div>
  
  <div class="step">
    <p>Step5: Drop test table</p>
    <el-input v-model="dropTableSql" />
    <el-button type="primary" @click="executeDropTableSql">Run</el-button>
    <p v-if="dropTableSqlSuccess!=null">Success: {{ dropTableSqlSuccess }}</p>
    <p v-if="dropTableSqlSuccess==false">Error: {{ dropTableSqlError }}</p>
  </div>
  
  <div class="step">
    <p>Step6: Drop test database</p>
    <el-input v-model="dropDbSql" />
    <el-button type="primary" @click="executeDropTableSql">Run</el-button>
    <p v-if="dropDbSqlSuccess!=null">Success: {{ dropDbSqlSuccess }}</p>
    <p v-if="dropDbSqlSuccess==false">Error: {{ dropDbSqlError }}</p>
  </div>
  
</div>

</template>

<script>
export default {
  name: 'Lab2',
  data: function() {
    return {
      createDbSql: "CREATE DATABASE db1",
      createDbSqlSuccess: null,
      createDbSqlError: "",
      
      createTableSql: "CREATE TABLE db1.t1 (c1 INT, c2 STRING)",
      createTableSqlSuccess: null,
      createTableSqlError: "",
      
      insertSql: "INSERT INTO t1 VALUES (10, 'foo')",
      insertSqlSuccess: null,
      insertSqlError: "",
      
      selectSql: "SELECT * FROM t1",
      selectSqlSuccess: null,
      selectSqlError: "",
      selectResultRows: [],
      
      dropTableSql: "DROP TABLE t1",
      dropTableSqlSuccess: null,
      dropTableSqlError: "",
      
      dropDbSql: "DROP DATABASE db1",
      dropDbSqlSuccess: null,
      dropDbSqlError: "",
      
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
  
    executeCreateTableSql() {
      fetch("http://127.0.0.1:5000/api/executesql?sql=" + this.createTableSql)
        .then(response => response.json())
        .then(json => {
          this.createTableSqlSuccess = json.success
          if (typeof json.error != "undefined") {
            this.createTableSqlError = json.error
          }
        })
    },
    
    executeInsertSql() {
      fetch("http://127.0.0.1:5000/api/executesql?sql=" + this.insertSql)
        .then(response => response.json())
        .then(json => {
          this.insertSqlSuccess = json.success
          if (typeof json.error != "undefined") {
            this.insertSqlError = json.error
          }
        })
    },
    
    executeSelectSql() {
      fetch("http://127.0.0.1:5000/api/querysql?sql=" + this.selectSql)
        .then(response => response.json())
        .then(json => {
          this.selectSqlSuccess = json.success
          if (typeof json.error != "undefined") {
            this.selectSqlError = json.error
            this.selectResultRows = []
          } else {
            this.selectResultRows = json.rows
          }
        })
    },
    
    executeDropTableSql() {
      fetch("http://127.0.0.1:5000/api/executesql?sql=" + this.dropTableSql)
        .then(response => response.json())
        .then(json => {
          this.dropTableSqlSuccess = json.success
          if (typeof json.error != "undefined") {
            this.dropTableSqlError = json.error
          }
        })
    },
    
    executeDropDbSql() {
      fetch("http://127.0.0.1:5000/api/executesql?sql=" + this.dropDbSql)
        .then(response => response.json())
        .then(json => {
          this.dropDbSqlSuccess = json.success
          if (typeof json.error != "undefined") {
            this.dropDbSqlError = json.error
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
</style>
