<script setup>
import { ref, watch, inject, onUnmounted, onMounted, useTemplateRef, nextTick } from "vue"
import { useNotification } from '@kyvg/vue3-notification'
import { useRouter, useRoute, onBeforeRouteLeave } from 'vue-router'
import {
  MAX_TITLE_LENGTH,
  MAX_TEXT_LENGTH,
  MAX_PIN_LENGTH,
  isValidTitle,
  isValidText,
  isValidPin
} from '@/utils/validation'

import axios from 'axios'
import CloseIcon from "../icons/CloseIcon.vue"

const store = inject("store")
const router = useRouter()
const route = useRoute()
const notification = useNotification()
const emit = defineEmits(["close"])
const pinRef = useTemplateRef('pinRef')

const isProtected = ref(false)
const isSaving = ref(false)

const newNote = ref({
  title: "",
  text: "",
  pin: ""
})

const validationErrors = ref({
  title: false,
  text: false,
  pin: false
})

// note without pin
const setPublic = () => {
  isProtected.value = false
  newNote.value.pin = ""
  validationErrors.value.pin = false
}

// note with pin
const protect = () => {
  isProtected.value = true
  validationErrors.value.pin = false

  // Wait for the DOM to update after the v-if condition makes the input visible
  nextTick(() => {
    if (pinRef.value) {
      pinRef.value.focus()
    }
  })
}

// title validation
// accept 100 char long string
watch(
  () => newNote.value.title,
  (newVal, oldVal) => {
    if (newNote.value.title.length >= MAX_TITLE_LENGTH + 1) {
      newNote.value.title = newVal.slice(0, MAX_TITLE_LENGTH + 1)
      validationErrors.value.title = true
    } else {
      validationErrors.value.title = false
    }
  }
)

// text
// accept 20000 char long string
watch(
  () => newNote.value.text,
  (newVal, oldVal) => {
    if (newNote.value.text.length >= MAX_TEXT_LENGTH + 1) {
      newNote.value.text = newVal.slice(0, MAX_TEXT_LENGTH + 1)
      validationErrors.value.text = true
    } else {
      validationErrors.value.text = false
    }
  }
)

// pin
// accept 8 char long string
watch(
  () => newNote.value.pin,
  (newVal, oldVal) => {
    if (newNote.value.pin.length >= MAX_PIN_LENGTH + 1) {
      newNote.value.pin = newVal.slice(0, MAX_PIN_LENGTH + 1)
      validationErrors.value.pin = true
    } else {
      validationErrors.value.pin = false
    }
  }
)


const save = async() => {
  // check errors
  let hasError = false

  if (!isValidTitle(newNote.value.title)) {
    validationErrors.value.title = true
    hasError = true
  }

  if (!isValidText(newNote.value.text)) {
    validationErrors.value.text = true
    hasError = true
  }

  if (newNote.value.pin && !isValidPin(newNote.value.pin)) {
    validationErrors.value.pin = true
    hasError = true
  }

  if (hasError) {
    notification.notify({
      title: "Cannot save note.",
      text: "Please correct the highlighted errors."
    })
    return
  }

  isSaving.value = true
  try {
    const { data } = await axios.post('/notes/new-note/', newNote.value, { headers: store.authActions.getAuthorizationHeader() })
    store.notesStateActions.setNewNote(data.id, data.info.title, data.info.text, data.info.pin)
    store.activeNoteActions.setActiveNote(data.id, data.info.title, data.info.text, data.info.dateCreated, data.info.pin)
    newNote.value = {}

    // if there first note created than reload the page to get pagination
    if (store.notesState.noteList.size === 6 && !store.notesState.pagination.currentPage) {
      router.go(route.fullPath)
    }

    emit('close')
    notification.notify({
      title: data.info.title.slice(0, 25),
      text: "New note added."
    })
  } catch (err) {
    // remove the current token, redirect to login page
    if (err.response && err.response.status === 401) {
      store.authActions.resetAuth()
      router.push({ name: "login" })
      return
    }
    notification.notify({
      title: "Something went wrong!",
      text: "Please try again."
    })
  } finally {
    isSaving.value = false
  }
}


// close popup. prevent edits lost
const closePopup = () => {
  if (newNote.value.title || newNote.value.text || newNote.value.pin) {
    const isConfirmed = confirm("Your edit will be lost.")
    if (!isConfirmed) {
      return
    }
  }
  emit("close")
}


// --- NAVIGATION GUARD: Prevent leaving page if there are unsaved changes ---
onBeforeRouteLeave((to, from, next) => {
  if (newNote.value.title || newNote.value.text || newNote.value.pin) {
    const confirmed = confirm("You have unsaved changes. Do you want to leave without saving?")
    if (confirmed) {
      next()
    } else {
      // User cancelled, prevent navigation
      next(false)
    }
  } else {
    // No unsaved changes, allow navigation immediately
    next()
  }
})

// prevent new window, reload page if there is any changes
onMounted(() => {
  window.onbeforeunload = (event) => {
    if (newNote.value.title || newNote.value.text || newNote.value.pin) {
      event.preventDefault()
      event.returnValue = "Your edit will be lost."
      return event.returnValue
    }
  }
})

// prevent close popup if there is any changes
onUnmounted(() => {
  window.onbeforeunload = null
})
</script>
<template>
  <div class="popup-overlay" @click="closePopup">
    <div class="popup-content" @click.stop>
      <div class="top-bar">
        <div class="setting">
          <div class="left">
            <button @click="save" :class="{ 'deactive': isSaving }" :disabled="isSaving">Save Note</button>
          </div>
          <div class="right">
            <button class="btn-left" :class="{'active' : !isProtected}" @click="setPublic">Public</button>
            <button class="btn-right" :class="{'active' : isProtected}" @click="protect">Protect</button>
            <input ref="pinRef" v-if="isProtected" v-model="newNote.pin" type="text" placeholder="3-8 char PIN" class="pin" :class="{ 'invalid-pin': validationErrors.pin }">
          </div>
        </div>
        <div class="icon">
          <CloseIcon @click="closePopup" />
        </div>
      </div>
      <div class="input-area">
        <input type="text" v-model.trim="newNote.title" :class="{ 'invalid-border': validationErrors.title }" placeholder="Please give a title" spellcheck="false">
        <textarea id="text" v-model.trim="newNote.text" placeholder="What's on your MIND?" :class="{ 'invalid-border': validationErrors.text }" spellcheck="false" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.popup-content {
  width: 1100px;
  height: 700px;
  background-color: var(--primary-black);
  padding: 20px;
  border: 1px solid var(--accent);
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon svg:hover {
  cursor: pointer;
}

.input-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.invalid-border {
  padding: 9px 14px;
  border: 1px solid red !important;
}

input:focus-visible {
  outline: none;
  color: #fff;
}

input {
  width: 100%;
  color: #ffffff;
  font-size: 14px;
  padding: 10px 15px;
  background-color: var(--secondary-black);
  border-radius: 5px;
  border: 0;
}

textarea#text {
  width: 100%;
  height: 565px;
  padding: 10px;
  border-radius: 5px;
  border: 0;
  color: #ffffff;
  background-color: var(--secondary-black);
  resize: none;
  scrollbar-color: var(--accent) transparent;
  scrollbar-width: thin;
  font-size: 14px;
  font-family: Arial;
}

textarea:focus-visible {
  outline: none;
  color: #fff;
}

.setting {
  display: flex;
  gap: 20px;
}

.right button {
  color: #ffffff;
  border-radius: 0;
  background-color: var(--tertiary-black);
  cursor: pointer;
}

.pin {
  margin-left: 8px;
  width: 120px;
  padding: 7px 15px;
}

.right .btn-left {
  border-radius: 5px 0px 0px 5px;
}

.right .btn-right {
  border-radius: 0px 5px 5px 0px;
}

.left {
  display: flex;
  align-items: center;
  gap: 10px;
}

button {
  border: 0;
  background-color: var(--accent);
  border-radius: 50px;
  padding: 8px 25px;
  cursor: pointer;
  color: #ffffff;
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

.active {
  background-color: var(--accent) !important;
}

.invalid-border {
  padding: 9px 14px;
  border: 1px solid red;
}

.invalid-pin {
  padding: 6px 14px;
  border: 1px solid red;
}

.deactive {
  animation: btn-bg 1s infinite;
}
</style>
