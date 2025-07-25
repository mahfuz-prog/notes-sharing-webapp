<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useNotification } from "@kyvg/vue3-notification"
import { validateName, validateEmail, validatePassword, validateOtp } from '@/utils/validation'

import axios from 'axios'

const notification = useNotification()
const router = useRouter()

// Form states
const submitValues = ref({
  name: "",
  email: "",
  password: "",
  otp: ""
})

// UI states
const formStep = ref('signup') // 'signup', 'otp'
const isLoading = ref(false)
const isResending = ref(false)
const countdown = ref(120)
let countdownInterval = null

// errors
const errors = ref({
  name: '',
  email: '',
  password: '',
  otp: '',
  general: ''
})


// Handles initial sign-up form submission
const handleSignUpSubmit = async() => {
  // Clear all previous errors
  errors.value = { name: '', email: '', password: '', otp: '', general: '' }

  let hasError = false

  // Validate all fields
  if (!validateName(submitValues.value.name)) {
    errors.value.name = 'Only 3-20 characters (a-Z, 0-9, _, -, single space).'
    hasError = true
  }
  if (!validateEmail(submitValues.value.email)) {
    errors.value.email = 'Please enter a valid email address.'
    hasError = true
  }
  if (!validatePassword(submitValues.value.password)) {
    errors.value.password = 'Password must be 8-20 characters with lowercase, uppercase, and digit.'
    hasError = true
  }

  // validation fails, stop submission
  if (hasError) {
    return
  }

  try {
    isLoading.value = true
    const { data } = await axios.post('/users/sign-up/', submitValues.value)

    if (data.message) {
      // Move to OTP verification step
      formStep.value = 'otp'
      notification.notify({
          title: "Please verify OTP.",
          text: "A 6-digit code has been sent to your email."
        })
        // Start the OTP countdown
      startCountdown()
    }
  } catch (err) {
    // username or email conflict
    if (err.response && err.response.status === 409) {
      // name Conflict
      if (err.response.data.nameStatus) {
        errors.value.name = err.response.data.nameStatus
      }
      // email conflict
      if (err.response.data.emailStatus) {
        errors.value.email = err.response.data.emailStatus
      }
      return
    }

    // otp send fail
    if (err.response && err.response.status === 500) {
      errors.value.general = "Failed to send OTP. Please try again."
      notification.notify({
        title: "OTP Send Failed.",
        text: "Please try submitting the form again."
      })
      return
    }
    errors.value.general = "An unexpected error occurred. Please try again."
  } finally {
    isLoading.value = false
  }
}


// Handles OTP verification form submission
const handleOtpSubmit = async() => {
  // Clear previous OTP error
  errors.value.otp = ''

  // otp validation
  if (!validateOtp(submitValues.value.otp)) {
    errors.value.otp = 'Please enter a valid 6-digit code.'
    return
  }

  isLoading.value = true
  try {
    const { data } = await axios.post('/users/verify/', submitValues.value)

    notification.notify({
      title: "Account Created 🎉",
      text: "Now you can log in."
    })
    router.push({ name: "login" })
  } catch (err) {
    errors.value.otp = "An unexpected error occurred. Please try again."
  } finally {
    isLoading.value = false
  }
}


// Resends the OTP code
const resendCode = async() => {
  // Reset OTP input and error
  submitValues.value.otp = ''
  errors.value.otp = ''

  // Reset countdown and clear previous interval
  clearInterval(countdownInterval)
  countdown.value = 120

  // button loading
  isResending.value = true

  // Re-trigger the initial sign-up process to send a new OTP
  await handleSignUpSubmit()
  isResending.value = false
}

// Starts the countdown timer for OTP
const startCountdown = () => {
  if (countdownInterval) {
    // Clear any existing interval
    clearInterval(countdownInterval)
  }
  countdownInterval = setInterval(() => {
    countdown.value--
      if (countdown.value <= 0) {
        clearInterval(countdownInterval)
      }
  }, 1000)
}
</script>
<template>
  <div class="form">
    <!-- user form -->
    <form @submit.prevent="handleSignUpSubmit" v-if="formStep === 'signup'">
      <h4>Create Account</h4>
      <input type="text" v-model.trim="submitValues.name" placeholder="Your Name" required :disabled="isLoading" />
      <span v-if="errors.name">● {{ errors.name }}</span>
      <input type="email" v-model.trim="submitValues.email" placeholder="Your Email" required :disabled="isLoading" />
      <span v-if="errors.email">● {{ errors.email }}</span>
      <input type="password" v-model.trim="submitValues.password" placeholder="Password" required :disabled="isLoading" />
      <span v-if="errors.password">● {{ errors.password }}</span>
      <span v-if="errors.general">● {{ errors.general }}</span>
      <button type="submit" :class="{ 'deactive': isLoading }" :disabled="isLoading">
        {{ isLoading ? 'Submitting...' : 'Sign Up' }}
      </button>
    </form>
    <!-- otp form -->
    <form @submit.prevent="handleOtpSubmit" v-else-if="formStep === 'otp'">
      <h4>Please enter the OTP from your email</h4>
      <input type="text" v-model.trim="submitValues.otp" placeholder="6-digit code" required :disabled="isLoading" />
      <span v-if="errors.otp">● {{ errors.otp }}</span>
      <button type="submit" :class="{ 'deactive': isLoading && !isResending }" :disabled="isLoading">
        {{ isLoading && !isResending ? 'Verifying...' : 'Verify' }}
      </button>
      <button type="button" class="resend-btn" @click="resendCode" :class="{ 'deactive': isResending }" :disabled="countdown > 0 || isLoading">
        Resend Code {{ countdown > 0 ? `(${countdown})` : '' }}
      </button>
    </form>
  </div>
</template>

<style scoped>
.form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  border-radius: 5px;
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

.resend-btn {
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
