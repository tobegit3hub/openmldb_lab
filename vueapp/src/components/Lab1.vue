<template>

<div class="lab1">
  

  <h2>Lab 1</h2>
  <p>Introduction: use basic SQL operations</p>

  <div class="step">
    <p>Step1: Create test database</p>
    <input v-model="createDbSql" />
    <button @click="executeCreateDbSql">Run</button>
    <p v-if="createDbSqlSuccess!=null">Success: {{ createDbSqlSuccess }}</p>
    <p v-if="createDbSqlSuccess==false">Error: {{ createDbSqlError }}</p>
  </div>
  
  <div class="step">
    <p>Step2: Create test table</p>
    <input v-model="createTableSql" />
    <button @click="executeCreateTableSql">Run</button>
    <p v-if="createTableSqlSuccess!=null">Success: {{ createTableSqlSuccess }}</p>
    <p v-if="createTableSqlSuccess==false">Error: {{ createTableSqlError }}</p>
  </div>  
  
</div>

</template>

<script>
export default {
  name: 'Lab1',
  props: {
  },
  created() {
  },
  data: function() {
    return {
      createDbSql: "CREATE DATABASE db1",
      createDbSqlSuccess: null,
      createDbSqlError: "",
      createTableSql: "CREATE TABLE db1.t1 (c1 INT, c2 STRING)",
      createTableSqlSuccess: null,
      createTableSqlError: "",
      sqlResultRows: []
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
</style>
