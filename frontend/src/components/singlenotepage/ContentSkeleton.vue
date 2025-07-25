<template>
  <div class="frame">
    <div class="header" />
    <hr>
    <div class="title" />
    <div class="text1" />
    <div class="text2" />
  </div>
</template>

<style scoped>
.frame {
  width: 1140px;
  height: calc(100vh - 150px);
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  border: 1px solid var(--tertiary-black);
  border-radius: 5px;
  padding: 20px;
}

.header {
  height: 21px;
  width: 400px;
  border-radius: 20px;
  animation: pulse-bg 1s infinite;
}

.title {
  height: 22px;
  width: 700px;
  border-radius: 20px;
  animation: pulse-bg 1s infinite;
}

hr {
  border: 0;
  border-top: 1px solid;
  animation: pulse-border 1s infinite;
}

.text1,
.text2 {
  height: 12px;
  width: 100%;
  border-radius: 20px;
  animation: pulse-bg 1s infinite;
}

.text2 {
  width: 60%;
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

@keyframes pulse-border {
  0% {
    border-top-color: rgb(12 187 197 / 15%);
  }
  50% {
    border-top-color: var(--tertiary-black);
  }
  100% {
    border-top-color: rgb(12 187 197 / 15%);
  }
}
</style>
