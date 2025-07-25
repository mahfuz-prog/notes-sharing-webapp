<template>
  <div class="layout">
    <div class="profile">
      <div class="img" />
      <div class="name" />
      <hr>
    </div>
    <div class="notes">
      <div class="note">
        <div class="title" />
        <div class="date" />
      </div>
      <div class="note">
        <div class="title" />
        <div class="date" />
      </div>
      <div class="note">
        <div class="title" />
        <div class="date" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.layout {
  width: 500px;
  max-height: calc(100vh - 160px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 40px;
  border: 1px solid var(--tertiary-black);
  border-radius: 5px;
  padding: 20px;
}

.profile {
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: center;
  justify-content: center;
}

.notes {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.note {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid var(--tertiary-black);
  border-radius: 5px;
  padding: 10px;
  height: 40px;
}

.title {
  width: 200px;
  height: 13px;
  animation: pulse-bg 1s infinite;
  border-radius: 10px;
}

.date {
  width: 130px;
  height: 13px;
  animation: pulse-bg 1s infinite;
  border-radius: 10px;
}

.img {
  width: 110px;
  height: 110px;
  border-radius: 50%;
  border: 3px solid var(--accent);
  animation: pulse-bg 1s infinite;
}

hr {
  border: none;
  height: 5px;
  width: 60px;
  background-color: var(--tertiary-black);
  border-radius: 5px;
}

.name {
  height: 16px;
  width: 150px;
  animation: pulse-bg 1s infinite;
  border-radius: 10px;
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
