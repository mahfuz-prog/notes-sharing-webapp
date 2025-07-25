<script setup>
const props = defineProps(['err'])
</script>
<template>
  <div class="page">
    <i><h1>{{ props.err }}</h1></i>
  </div>
</template>

<style scoped>
.page {
  height: calc(100vh - 65px - 42px);
  display: grid;
  place-items: center;
}

h1 {
  font-weight: 700;
  text-align: center;
}
</style>
