<template>
  <div class="info">
    <div class="card" />
    <div class="card" />
    <div class="card" />
  </div>
</template>

<style scoped>
.info {
  width: 800px;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 10px;
}

.card {
  border: 1px solid var(--accent);
  height: 124px;
  animation: pulse-bg 1s infinite;
  border-radius: 10px;
  z-index: 3;
}

@keyframes pulse-bg {
  0% {
    background-color: rgb(12 187 197 / 15%);
  }
  50% {
    background-color: var(--tertiary-black);
  }
  100% {
    background-color: rgb(12 187 197 / 15%);
  }
}
</style>
