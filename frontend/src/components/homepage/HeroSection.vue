<script setup>
import { ref, reactive } from 'vue'

import axios from 'axios'
import gsap from 'gsap'

const info = ref({
  totalUser: '',
  totalNotes: '',
  totalChar: ''
})

const tweened = reactive({
  totalUser: 0,
  totalNotes: 0,
  totalChar: 0

})

try {
  const { data } = await axios.get('/main/home/')
  info.value.totalUser = data.totalUser
  info.value.totalNotes = data.totalNotes
  info.value.totalChar = data.totalChar

  gsap.to(tweened, { duration: 1, totalUser: Number(data.totalUser) || 0 })
  gsap.to(tweened, { duration: 1, totalNotes: Number(data.totalNotes) || 0 })
  gsap.to(tweened, { duration: 1, totalChar: Number(data.totalChar) || 0 })
    // handle error
} catch (err) {
  // check the status code of error
  if (err.response) {
    throw new Error(err.response.status)
  } else {
    // general error
    throw new Error(500)
  }
}
</script>
<template>
  <div class="info">
    <div class="card">
      <h2>{{ tweened.totalUser.toFixed(0) }}</h2>
      <h4>Total User</h4>
    </div>
    <div class="card">
      <h2>{{ tweened.totalNotes.toFixed(0) }}</h2>
      <h4>Total notes</h4>
    </div>
    <div class="card">
      <h2>{{ tweened.totalChar.toFixed(0) }}</h2>
      <h4>Total charecter</h4>
    </div>
  </div>
</template>

<style scoped>
.info {
  width: 800px;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 10px;
  z-index: 3;
}

.card {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 10px;
  padding: 20px;
  border: 1px solid var(--accent);
  border-radius: 10px;
  background-color: rgba(0, 0, 0, 0.5);
}

h2 {
  color: #ffffff;
  font-weight: 700;
  font-size: 30px;
}

h4 {
  color: #ffffff;
}
</style>
