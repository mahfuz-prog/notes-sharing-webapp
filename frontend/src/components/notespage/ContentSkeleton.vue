<template>
  <div class="frame">
    <div class="side-bar">
      <div class="list">
        <div class="item" />
      </div>
      <div class="list">
        <div class="item" />
      </div>
      <div class="list">
        <div class="item" />
      </div>
      <div class="list">
        <div class="item" />
      </div>
      <div class="list">
        <div class="item" />
      </div>
      <div class="list">
        <div class="item" />
      </div>
      <div class="list">
        <div class="item" />
      </div>
      <div class="list">
        <div class="item" />
      </div>
      <div class="list">
        <div class="item" />
      </div>
      <div class="list">
        <div class="item" />
      </div>
    </div>
    <div class="output-box">
    </div>
  </div>
</template>

<style scoped>
.frame {
  width: 1140px;
  height: calc(100vh - 160px);
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.side-bar {
  width: 360px;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 15px 10px;
  gap: 10px;
  border: 1px solid var(--tertiary-black);
  border-radius: 5px;
}

.output-box {
  width: 100%;
  height: 100%;
  border-radius: 3px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 10px;
  animation: pulse-bg 1s infinite;
}

.list {
  padding: 11px 14px;
  background-color: var(--secondary-black);
  border-radius: 3px;
}

.item {
  height: 18px;
  border-radius: 25px;
  animation: pulse-bg 1s infinite;
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
