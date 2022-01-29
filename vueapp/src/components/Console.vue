<template>

<div class="console">
  <div class="db_list">
    <h2>Databases</h2>
    <ul>
      <li>db1</li>
      <li>db2</li>
      <li>db3</li>
    </ul>
  </div>

  <div class="table_list">
    <h2>Tables</h2>

    <ul>
      <li v-for="table in tables" :key="table">
        {{ table }}
      </li>
    </ul>
  </div>
  
  <div class="sql_playground">
  <input />
    <div class="sql_result">

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
                 this.tables = json.tables   
               })
  },
  data: function() {
    return {
      tables: []
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
