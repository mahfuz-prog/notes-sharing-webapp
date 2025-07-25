<script setup>
import Content from '../components/homepage/Content.vue'
</script>
<template>
  <div class="page">
    <Content />
  </div>
</template>

<style scoped>
.page {
  scrollbar-color: var(--accent) transparent;
  scrollbar-width: thin;
  background-color: var(--primary-black);
}
</style>
