<script setup>
import Content from '../components/signuppage/Content.vue'

import { inject } from 'vue'
import { useRouter } from 'vue-router'
import { useNotification } from '@kyvg/vue3-notification'

// reactive store object
const store = inject("store")
const router = useRouter()
const notification = useNotification()

// check if the user already has a jwt token
if (store.authState.token) {
  router.push({ name: "home" })
  notification.notify({ title: "Sign up not allowed.", text: "You are already logged in." })
}
</script>
<template>
  <div class="page">
    <Content />
  </div>
</template>

<style scoped>
.page {
  height: calc(100vh - 65px - 42px);
  display: grid;
  place-items: center;
  background-color: var(--primary-black);
}
</style>
