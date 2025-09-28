<script setup>
import { ref, inject } from 'vue'
import { useRouter } from 'vue-router'
import { useNotification } from "@kyvg/vue3-notification"
import { validateEmail, validatePassword } from '@/utils/validation'

import axios from 'axios'

const store = inject("store")
const router = useRouter()
const notification = useNotification()

// Form states
const submitValues = ref({
  email: "",
  password: ""
})

// UI states
// Replaces submitBtn for loading state
const isLoading = ref(false)
const errors = ref({
  email: "",
  password: "",
  general: ""
})

// Handles login form submission
const submitForm = async() => {
  // Clear all previous errors
  errors.value = { email: "", password: "", general: "" }

  let hasError = false

  // Validate all fields
  if (!validateEmail(submitValues.value.email)) {
    errors.value.email = 'Please enter a valid email address.'
    hasError = true
  }
  if (!validatePassword(submitValues.value.password)) {
    errors.value.password = 'Password must be 8-20 characters with lowercase, uppercase, and digit.'
    hasError = true
  }

  // If any client-side validation fails, stop submission
  if (hasError) {
    return
  }

  // Set loading state to true
  isLoading.value = true
  try {
    const { data } = await axios.post('/users/log-in/', submitValues.value)

    // Update the token if successful
    store.authActions.updateToken(data.token)
    store.authActions.setUsername(data.username)
    notification.notify({
      title: "Successfully logged in.",
      text: "Now you have unlimited access."
    })

    // Redirect to account page
    router.push({ name: 'account' })

  } catch (err) {
    // Handle specific API errors
    if (err.response && err.response.status == 401) {
      errors.value.general = "Invalid credentials! Please try again."
      return
    }
    errors.value.general = "An unexpected error occurred. Please try again."
  } finally {
    isLoading.value = false
  }
}
</script>
<template>
  <div class="form">
    <form @submit.prevent="submitForm">
      <h4>Log In</h4>
      <input type="email" v-model.trim="submitValues.email" placeholder="Your Email" required :disabled="isLoading" />
      <span v-if="errors.email">● {{ errors.email }}</span>
      <input type="password" v-model.trim="submitValues.password" placeholder="Password" required :disabled="isLoading" />
      <span v-if="errors.password">● {{ errors.password }}</span>
      <span v-if="errors.general">● {{ errors.general }}</span>
      <button type="submit" :class="{ 'deactive': isLoading }" :disabled="isLoading">
        {{ isLoading ? 'Submitting...' : 'Log In' }}
      </button>
      <button type="button" class="reset-btn" @click="router.push({name: 'reset-password'})">Reset Password</button>
    </form>
  </div>
</template>

<style scoped>
.form {
  border-radius: 5px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 15px;
  padding: 30px;
  width: 350px;
  background-color: var(--secondary-black);
}

form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 15px;
}

input {
  color: #fff;
  border: 0;
  border-radius: 3px;
  width: 100%;
  padding: 10px 15px 10px 15px;
  background-color: var(--tertiary-black);
}

input:focus-visible {
  outline: none;
  color: #fff;
}

button {
  border: 0;
  background-color: var(--accent);
  border-radius: 25px;
  padding: 9px;
  color: #fff;
  cursor: pointer;
}

button:disabled {
  background-color: var(--tertiary-black);
  cursor: not-allowed;
}

.reset-btn {
  background-color: var(--tertiary-black);
}

.deactive {
  animation: btn-bg 1s infinite;
}

span {
  color: red;
  padding-left: 5px;
  margin-top: -10px;
  font-size: 12px;
  font-weight: 400;
}

h4 {
  color: #fff;
  text-align: center;
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 15px;
}

@keyframes btn-bg {
  0% {
    background-color: var(--tertiary-black);
  }
  50% {
    background-color: rgb(145 145 145 / 64%);
  }
  100% {
    background-color: var(--tertiary-black);
  }
}
</style>
