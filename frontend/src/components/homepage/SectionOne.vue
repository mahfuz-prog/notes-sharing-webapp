<script setup>
</script>
<template>
  <div class="container">
    <div class="left">
      <h2>Notes management dashboard</h2>
      <hr />
      <span>
        Manage your notes effortlessly with our user-friendly dashboard. Create, delete, update, and secure your notes with ease. Options include making notes private, accessible via PIN, or generating a shareable URL—all in just a few clicks.
      </span>
    </div>
    <div class="right">
      <img src="@/assets/notedashboard.png">
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

.left {
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
  color: #ffffff;
  width: 70%;
}
</style>
