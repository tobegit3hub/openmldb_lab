<template>
<div class="Lab">
  <LabTemplate :title="title" :subtitle="subtitle" :labFile="labFile"></LabTemplate>
</div>
</template>

<script>
import LabTemplate from './LabTemplate.vue'
  
export default {
  name: 'Lab3',
  components: {
    LabTemplate
  },
  data() {
    return {
      title: "Lab1: End-to-end Demo",
      subtitle: "Introduction: Use OpenMLDB in end-to-end application.",
      labFile: "lab3.json"
    }
  }
}
</script>