<script setup>
import { inject } from 'vue'
import { useRouter } from 'vue-router'
import { useNotification } from '@kyvg/vue3-notification'

import Content from '../components/resetpasswordpage/Content.vue'

const store = inject("store")
const router = useRouter()
const notification = useNotification()

if (store.authState.token) {
  router.push({ name: "home" })
  notification.notify({ title: 'Reset password not allowed.', text: 'Logout to reset password.' })
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
