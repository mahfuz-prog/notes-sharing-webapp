<script setup>
import { ref, inject, watch } from 'vue'
import { useNotification } from '@kyvg/vue3-notification'
import { useRouter } from 'vue-router'

const store = inject("store")
const router = useRouter()
const notification = useNotification()


// log out functionality
function logOut() {
  store.authActions.resetAuth()

  // push to homepage
  router.push({ name: "home" })
  notification.notify({ title: 'Signed out.', text: 'Now you have limited access.' })
}
</script>
<template>
  <header>
    <div>
      <RouterLink :to="{ name: 'home' }">
        <h1>EasyString</h1>
      </RouterLink>
    </div>
    <div class="wrapper">
      <nav v-if="store.authState.token">
        <RouterLink :to="{ name: 'home' }">Home</RouterLink>
        <RouterLink :to="{ name: 'notes' }">Notes</RouterLink>
        <RouterLink :to="{ name: 'account' }">Account</RouterLink>
        <button @click="logOut">Log Out</button>
      </nav>
      <nav v-else>
        <RouterLink :to="{ name: 'home' }">Home</RouterLink>
        <RouterLink :to="{ name: 'signup' }">Sign Up</RouterLink>
        <RouterLink :to="{ name: 'login' }">Log In</RouterLink>
      </nav>
    </div>
  </header>
</template>

<style scoped>
header {
  height: 65px;
  padding: 10px 10px 10px 10px;
  width: 1140px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--secondary-black);
}

nav {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 30px;
}

.logo {
  width: 220px;
}

.router-link-active {
  color: var(--accent);
}

img {
  margin-bottom: -6px;
}

button {
  background-color: var(--accent);
  border: 0;
  padding: 8px 35px 8px 35px;
  border-radius: 25px;
  color: #ffffff;
  cursor: pointer;
}

h1 {
  font-weight: 700;
  color: var(--accent);
}

@media (min-width: 768px) {
  header {
    padding: 10px 20px 10px 20px;
    width: 100%;
  }
}
</style>
