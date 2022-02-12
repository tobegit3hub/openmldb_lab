<template>

<div class="TaskManager">

    <h2>OpenMLDB Task Manager</h2>
    
    <div>
      
      <el-button type="primary" @click="refreshTaskList" icon="el-icon-refresh">Refresh</el-button>
      
      <div id="task_list">
        <el-table
          :data="taskDataList"
          @row-click="handleSelectTask"
          stripe
          border
          style="width: 100%">
        
          <template v-for='(schema) in taskSchemaList'>
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
      
      <!-- TODO: the direction of btt does not work -->
      <el-drawer
        :title="logDrawerTitle"
        :visible.sync="showLogDrawer"
        :direction="btt">
        <div><p>{{ logDrawerContent }}</p></div>
      </el-drawer>
      
    </div>
</div>

</template>

<script>
export default {
  name: 'TaskManager',
  props: {},
  created() {
    this.refreshTaskList()
  },
  data() {
    return {
      taskDataList: [],
      taskSchemaList: [],
      showLogDrawer: false,
      logDrawerTitle: "",
      logDrawerContent: "",
    }
  },
  
  methods: {
  
    refreshTaskList() {
      fetch("http://127.0.0.1:5000/api/tasks")
        .then(response => response.json())
        .then(json => {
          if (json.success == false) {
            this.$message.error(json.error);
          } else {
            this.$message({
              message: "Refresh task list",
              type: "success"
            });

            this.taskDataList = json.rows
            this.taskSchemaList = json.schema
          }
        })
    },
    
    handleSelectTask(row, column, event) {
      var taskId = row.id
      
      this.showLogDrawer = true
      this.logDrawerTitle = "Log of Task " + taskId
      // TODO: support get log from Python SDK
      this.logDrawerContent = "This function will be add later"
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

#task_list {
  margin-top: 30px;
  margin-left: 50px;
  margin-right: 50px;
}
</style>
