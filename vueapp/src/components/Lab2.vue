<template>
<div class="Lab">
  <LabTemplate :title="title" :subtitle="subtitle" :labFile="labFile"></LabTemplate>
</div>
</template>

<script>
import LabTemplate from './LabTemplate.vue'
  
export default {
  name: 'Lab2',
  components: {
    LabTemplate
  },
  data() {
    return {
      title: "Lab2: Online/Offline Mode",
      subtitle: "Introduction: Use SQL in online mode and offline mode.",
      labFile: "lab2.json"
    }
  }
}
</script>