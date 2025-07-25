<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from "vue-router"
import { useNotification } from "@kyvg/vue3-notification"
import { validateEmail, validatePassword, validateOtp } from '@/utils/validation'

const notification = useNotification()
const router = useRouter()

const formStep = ref('email')
const countdown = ref(120)
  // To store the interval ID for clearing
let countdownInterval = null
const isResending = ref(false)
const isLoading = ref(false)

// Form states
const formState = ref({
  email: "",
  otp: "",
  password: "",
  confirmPassword: ""
})

// UI states
const errors = ref({
  email: '',
  otp: '',
  password: ''
})


// Email submission
const handleEmailSubmit = async() => {
  errors.value.email = ''

  // email validation
  if (!validateEmail(formState.value.email)) {
    errors.value.email = 'Please enter a valid email address.'
    return
  }

  try {
    isLoading.value = true
    const { data } = await axios.post('/users/reset-password/', { email: formState.value.email })

    if (data.message) {
      formStep.value = 'otp'
      notification.notify({
          title: data.message,
          text: "Check your email for the verification code."
        })
        // Start the OTP countdown
      startCountdown()
    }
  } catch (err) {
    errors.value.email = "Failed to send OTP. Please try again."
  } finally {
    isLoading.value = false
  }
}


// OTP verification
const handleOtpSubmit = async() => {
  errors.value.otp = ''

  // otp validation
  if (!validateOtp(formState.value.otp)) {
    errors.value.otp = 'Please enter a valid 6-digit code.'
    return
  }

  try {
    isLoading.value = true
    const { data } = await axios.post("/users/verify-reset-otp/", {
      email: formState.value.email,
      otp: formState.value.otp
    })

    // success otp clear clearInterval
    if (data.message) {
      formStep.value = 'password'
      clearInterval(countdownInterval)
    }
  } catch (err) {
    errors.value.otp = "Invalid OTP. Please try again."
  } finally {
    isLoading.value = false
  }
}

// Password submission
const handlePasswordSubmit = async() => {
  errors.value.password = ''

  // email validation
  if (!validatePassword(formState.value.password)) {
    errors.value.password = 'Password must be 8-20 characters with uppercase, lowercase, and number.'
    return
  }

  // confirm password
  if (formState.value.password !== formState.value.confirmPassword) {
    errors.value.password = "Passwords don't match."
    return
  }

  try {
    isLoading.value = true
    const { data } = await axios.post("/users/new-password/", {
      email: formState.value.email,
      otp: formState.value.otp,
      password: formState.value.password
    })

    if (data.message) {
      notification.notify({
        title: data.message,
        text: "Password changed successfully."
      })
      router.push({ name: "login" })
    }
  } catch (err) {
    errors.value.password = "Something went wrong! please try again after sometime."
  } finally {
    isLoading.value = false
  }
}


// Resends the OTP code
const resendCode = async() => {
  // Reset countdown and clear previous interval
  clearInterval(countdownInterval)

  // Reset countdown to 2 minutes
  countdown.value = 120

  // Set resending specific loading state
  isResending.value = true
  try {
    // Re-trigger the initial email submission to send a new OTP
    await handleEmailSubmit()
  } finally {
    isResending.value = false
  }
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
    <!-- Email Step -->
    <form @submit.prevent="handleEmailSubmit" v-if="formStep === 'email'">
      <h4>Reset Your Password</h4>
      <input type="email" v-model.trim="formState.email" placeholder="Your Email" required :disabled="isLoading" />
      <span v-if="errors.email">● {{ errors.email }}</span>
      <button type="submit" :class="{ 'deactive' : isLoading }" :disabled="isLoading">
        {{ isLoading ? 'Sending...' : 'Send OTP' }}
      </button>
    </form>
    <!-- OTP Step -->
    <form @submit.prevent="handleOtpSubmit" v-else-if="formStep === 'otp'">
      <h4>Enter Verification Code</h4>
      <input type="text" v-model.trim="formState.otp" placeholder="6-digit code" required :disabled="isLoading || isResending" />
      <span v-if="errors.otp">● {{ errors.otp }}</span>
      <button type="submit" :class="{ 'deactive' : isLoading && !isResending }" :disabled="isLoading || isResending">
        {{ isLoading ? 'Verifying...' : 'Verify Code' }}
      </button>
      <button type="button" class="resend-btn" @click="resendCode" :class="{ 'deactive': isResending }" :disabled="countdown > 0 || isLoading || isResending">
        Resend Code {{ countdown > 0 ? `(${countdown})` : '' }}
      </button>
    </form>
    <!-- Password Step -->
    <form @submit.prevent="handlePasswordSubmit" v-else>
      <h4>Set New Password</h4>
      <input type="password" v-model.trim="formState.password" placeholder="New Password" required :disabled="isLoading" />
      <input type="password" v-model.trim="formState.confirmPassword" placeholder="Confirm Password" required :disabled="isLoading" />
      <span v-if="errors.password">● {{ errors.password }}</span>
      <button type="submit" :class="{ 'deactive' : isLoading }" :disabled="isLoading">
        {{ isLoading ? 'Updating...' : 'Update Password' }}
      </button>
    </form>
  </div>
</template>

<style scoped>
.form {
  background-color: var(--secondary-black);
  width: 350px;
  padding: 30px;
  border-radius: 5px;
  display: flex;
  flex-direction: column;
}

form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

input {
  color: #fff;
  border: 0;
  border-radius: 3px;
  width: 100%;
  padding: 10px 15px;
  background-color: var(--tertiary-black);
}

input:focus-visible {
  outline: none;
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

span {
  color: red;
  font-size: 12px;
  margin-top: -10px;
  padding-left: 5px;
}

h4 {
  color: #fff;
  text-align: center;
  margin-bottom: 15px;
}

.deactive {
  animation: btn-bg 1s infinite;
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
