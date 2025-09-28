<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterView } from 'vue-router'

import Header from './components/templates/Header.vue'
import Footer from './components/templates/Footer.vue'

const isDesktop = ref(true)
const MOBILE_BREAKPOINT = 1140

// Function to check screen width and update isDesktop
const checkScreenSize = () => {
  isDesktop.value = window.innerWidth > MOBILE_BREAKPOINT
}

// Set up event listeners when the component is mounted
onMounted(() => {
  checkScreenSize()
    // Add event listener for window resize
  window.addEventListener('resize', checkScreenSize)
})

// Clean up event listeners when the component is unmounted
onUnmounted(() => {
  window.removeEventListener('resize', checkScreenSize)
})
</script>
<template>
  <notifications position="top left" classes="notification" />
  <template v-if="isDesktop">
    <Header />
    <main>
      <RouterView />
    </main>
    <Footer />
  </template>
  <template v-else>
    <div class="mobile-not-available">
      <div class="message-box">
        <h2>Dumn!! THIS site is not responsive.</h2>
        <p>Minimum width required: {{ MOBILE_BREAKPOINT + 1 }}px</p>
      </div>
    </div>
  </template>
</template>

<style>
main {
  height: 100%;
  width: 100%;
}

.vue-notification-group {
  top: 80px !important;
  left: 30px !important;
}

.vue-notification-group .notification {
  color: #fff;
  padding: 10px 15px 10px 15px;
  border-radius: 3px;
  background-color: #000;
  border: 1px solid var(--accent);
}

.vue-notification-group .vue-notification-wrapper {
  margin-top: 10px;
}

.mobile-not-available {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: var(--primary-black);
  color: #333;
  text-align: center;
  padding: 20px;
  box-sizing: border-box;
}

.message-box {
  background-color: var(--tertiary-black);
  border: 1px solid var(--accent);
  border-radius: 8px;
  padding: 30px;
  max-width: 400px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.message-box h2 {
  color: red;
  margin-bottom: 15px;
  font-size: 1.8em;
}

.message-box p {
  font-size: 1.1em;
  line-height: 1.6;
  margin-bottom: 10px;
  color: #fff;
}
</style>
