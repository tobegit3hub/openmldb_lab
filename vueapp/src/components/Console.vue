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
      <li>t1</li>
      <li>t2</li>
      <li>t3</li>
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
