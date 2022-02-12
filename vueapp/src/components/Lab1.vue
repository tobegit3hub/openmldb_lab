<template>
<div class="Lab">
  <LabTemplate :title="title" :subtitle="subtitle" :labFile="labFile"></LabTemplate>
</div>
</template>

<script>
import LabTemplate from './LabTemplate.vue'
  
export default {
  name: 'Lab1',
  components: {
    LabTemplate
  },
  data() {
    return {
      title: "Lab1: Basic SQL",
      subtitle: "Introduction: use basic SQL operations.",
      labFile: "lab1.json"
    }
  }
}
</script>