<script setup>
import { ref, watch, useTemplateRef, onMounted } from 'vue'
import { useNotification } from '@kyvg/vue3-notification'
import { MAX_PIN_LENGTH, MIN_PIN_LENGTH } from '@/utils/validation'

import axios from 'axios'

const props = defineProps(["payload"])
const emit = defineEmits(['success'])
const pinRef = useTemplateRef('pinRef')
const notification = useNotification()

const pin = ref("")
const isInvalid = ref(false)
const isSubmiting = ref(false)

const payload = ref({
  "username": "",
  "note_id": "",
  "pin": ""
})

// if props than assign props value
if (props.payload) {
  payload.value.username = props.payload.username
  payload.value.note_id = props.payload.note_id
}


// validate pin
watch(pin, (newVal, oldVal) => {
  if (pin.value.length >= MAX_PIN_LENGTH + 1) {
    pin.value = newVal.slice(0, MAX_PIN_LENGTH + 1)
    isInvalid.value = true
  } else {
    isInvalid.value = false
  }
})


// submit with pin
const submit = async() => {
  // stop empty pin request sent
  if (!pin.value || pin.value.length < MIN_PIN_LENGTH || pin.value.length > MAX_PIN_LENGTH) {
    isInvalid.value = true
    return
  }

  // sent request
  isSubmiting.value = true
  try {
    // add pin to payload
    payload.value.pin = pin.value
    const { data } = await axios.post('/main/single-note/', payload.value)
    emit('success', data)
  } catch (err) {
    // invalid pin
    if (err.response && err.response.status === 403) {
      isInvalid.value = true
      notification.notify({
        title: err.response.data.error,
        text: "Please try again."
      })
      return
    }

    // other error
    notification.notify({
      title: "Something went wrong!",
      text: "Please try again."
    })
  } finally {
    isSubmiting.value = false
  }
}

// cursor on input box
onMounted(() => {
  pinRef.value.focus()
})
</script>
<template>
  <div class="background">
    <div class="popup">
      <form class="form" @submit.prevent="submit">
        <div class="input">
          <h5>Insert pin to access this note.</h5>
          <input type="text" ref="pinRef" v-model.trim="pin" :class="{ 'invalid-border': isInvalid }" placeholder="Input pin" spellcheck="false">
          <span v-if="isInvalid">Invalid pin!</span>
        </div>
        <div>
          <button class="btn" type="submit" :class="{'submiting': isSubmiting}">Submit</button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.background {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  background-color: #000000eb;
}

.popup {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 250px;
  background-color: var(--secondary-black);
  border-radius: 5px;
  padding-top: 20px;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input {
  padding: 0px 20px;
}

.btn {
  color: #fff;
  width: 100%;
  border: 0;
  padding-top: 8px;
  padding-bottom: 8px;
  cursor: pointer;
  border-radius: 0px 0px 5px 5px;
  background-color: var(--accent);
}

span {
  color: red;
  font-size: 11px;
}

h5 {
  color: #ffffff;
  padding-bottom: 10px;
  text-align: center;
  font-size: 13px;
}

input {
  width: 100%;
  color: #ffffff;
  font-size: 14px;
  padding: 10px 15px;
  background-color: var(--tertiary-black);
  border-radius: 5px;
  border: 0;
}

input:focus-visible {
  outline: none;
  color: #fff;
}

.invalid-border {
  padding: 9px 14px !important;
  border: 1px solid red !important;
}

.submiting {
  animation: pulse-bg 1s infinite;
}

@keyframes pulse-bg {
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
