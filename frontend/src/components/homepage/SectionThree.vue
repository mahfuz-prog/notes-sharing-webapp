<script setup>
</script>
<template>
  <div class="container">
    <div class="left">
      <h2>Profile view</h2>
      <hr />
      <span>
        Your public profile is accessible via a unique URL. Anyone can view it and see all the notes you've made public.
      </span>
    </div>
    <div class="right">
      <img src="@/assets/profile.png">
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
