<script setup>
</script>
<template>
  <div class="container">
    <div class="left">
      <img src="@/assets/single-note.png">
    </div>
    <div class="right">
      <h2>Note public view</h2>
      <hr />
      <span>
        Share your notes effortlessly. Anyone with the URL can view your public notes. For PIN-protected notes, simply enter the correct PIN to access. Plus, easily copy note content with a single click.
      </span>
    </div>
  </div>
</template>

<style scoped>
.container {
  padding: 60px 0px;
  display: flex;
  width: 1140px;
  gap: 30px;
}

.left,
.right {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.right {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

hr {
  width: 80px;
  border: 0;
  border-top: 5px solid var(--tertiary-black);
  border-radius: 50px;
}

h2 {
  color: #ffffff;
  font-weight: 700;
  font-size: 30px;
}

img {
  width: 100%;
}

span {
  width: 70%;
  color: #ffffff;
}
</style>
