<script setup>
import { ref, inject, watchEffect, watch, useTemplateRef, onMounted, onUnmounted, nextTick } from 'vue'
import { useNotification } from '@kyvg/vue3-notification'
import { useRouter, onBeforeRouteLeave } from 'vue-router'
import {
  MAX_TITLE_LENGTH,
  MAX_TEXT_LENGTH,
  MAX_PIN_LENGTH,
  MIN_PIN_LENGTH,
  isValidTitle,
  isValidText,
  isValidPin
} from '@/utils/validation'
import { copyToClipboard } from '@/utils/helper'

import axios from 'axios'

const store = inject("store")
const { props } = defineProps(['props'])
const notification = useNotification()
const pinRef = useTemplateRef('pinRef')
const router = useRouter()

const pin = ref("")
const isInvalid = ref(false)
const isProtected = ref(false)
const isSaving = ref(false)


// when an new note select this triger
watchEffect(() => {
  if (props) {
    pin.value = props
    isProtected.value = true
  } else {
    pin.value = ""
    isProtected.value = false
  }
  isInvalid.value = false
})

// check and validate input pin
watch(pin, (newVal, oldVal) => {
  if (pin.value.length >= MAX_PIN_LENGTH + 1) {
    pin.value = newVal.slice(0, MAX_PIN_LENGTH + 1)
    isInvalid.value = true
  } else {
    isInvalid.value = false
  }
  store.tempNoteActions.editPin(pin.value)
})


// protect to public
const setPublic = () => {
  isProtected.value = false
  store.tempNoteActions.editPin("")
}

// protect to public
const protect = () => {
  // check if there is a note to protect
  if (!store.activeNoteState.id) {
    return
  }

  isProtected.value = true
  pin.value = store.activeNoteState.pin

  // Wait for the DOM to update after the v-if condition makes the input visible
  nextTick(() => {
    if (pinRef.value) {
      pinRef.value.focus()
    }
  })
}


// update note
const save = async() => {
  // if empty notes
  if (store.notesState.noteList.size === 0) {
    notification.notify({
      title: "Note not found!",
      text: "Please create a new note first."
    })
    return
  }

  // pin validation
  if (isProtected.value && !isValidPin(pin.value)) {
    isInvalid.value = true
    notification.notify({
      title: "Please enter a perfect pin.",
      text: `You have to set ${MIN_PIN_LENGTH} - ${MAX_PIN_LENGTH} character long pin.`
    })
    return
  }

  // title validation.
  if (!isValidTitle(store.tempNoteState.title)) {
    notification.notify({
      title: "Please enter a perfect title.",
      text: `Title can't be empty or more than ${MAX_TITLE_LENGTH} character.`
    })
    return
  }

  // text validation
  if (!isValidText(store.tempNoteState.text)) {
    notification.notify({
      title: "Cannot save note.",
      text: `Text can't be empty or more than ${MAX_TEXT_LENGTH} character.`
    })
    return
  }

  // if the note is updated only than sent update req to backend
  if (store.tempNoteActions.isEdited) {
    isSaving.value = true
    try {
      const payload = {
        "note_id": store.activeNoteState.id,
        "title": store.tempNoteState.title,
        "text": store.tempNoteState.text,
        "pin": store.tempNoteState.pin
      }
      const { data } = await axios.post('/notes/update-note/', payload, { headers: store.authActions.getAuthorizationHeader() })
        // add updated data in store map
      store.notesStateActions.updateNote(data.id, data.title, data.text, data.pin)
      store.activeNoteActions.setActiveNote(data.id, data.title, data.text, store.activeNoteState.dateCreated, data.pin)

      notification.notify({
        title: store.tempNoteState.title.slice(0, 25),
        text: "Note successfuly updated."
      })
    } catch (err) {
      // remove the current token, redirect to login page
      if ((err.response && err.response.status === 401) || (err.response && err.response.status === 403)) {
        store.authActions.resetAuth()
        router.push({ name: "login" })
        return
      }

      let errMsg = "Something went wrong."
      if (err.response.data.error) {
        errMsg = err.response.data.error
      }
      notification.notify({
        title: errMsg,
        text: "Please try again."
      })
    } finally {
      isSaving.value = false
    }
  } else {
    notification.notify({
      title: "No changes made!",
      text: "You can save only after update."
    })
  }
}


// url copy clipboard
const copy = () => {
  const url = `${store.authState.FRONTEND}/${store.authState.username}/${store.activeNoteState.id}/`
  copyToClipboard(url)
    .then(() => {
      notification.notify({ title: "Text copied to clipboard!", text: url })
    })
    .catch(err => {
      notification.notify({ title: "Failed to copy!", text: url })
    })
}


// --- NAVIGATION GUARD: Prevent leaving page if there are unsaved changes ---
onBeforeRouteLeave((to, from, next) => {
  if (store.tempNoteActions.isEdited) {
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


// Prevent closing tab/window if there are unsaved changes ---
const handleBeforeUnload = (event) => {
  if (store.tempNoteActions.isEdited) {
    event.preventDefault()
    event.returnValue = "Your edits will be lost."
    return "Your edits will be lost."
  }
}

onMounted(() => {
  // Add the event listener when the component is mounted
  window.addEventListener('beforeunload', handleBeforeUnload)
})

onUnmounted(() => {
  // Remove the event listener when the component is unmounted to prevent memory leaks
  window.removeEventListener('beforeunload', handleBeforeUnload)
  window.onbeforeunload = null
})
</script>
<template>
  <div class="setting">
    <div class="left">
      <button class="btn-left" :class="{'active' : !isProtected}" @click="setPublic">Public</button>
      <button class="btn-right" :class="{'active' : isProtected}" @click="protect">Protect</button>
      <input v-if="isProtected" v-model="pin" type="text" placeholder="3-8 char PIN" ref="pinRef" @click="pinRef.select()" class="pin" :class="{ 'invalid-border': isInvalid }">
    </div>
    <div class="right">
      <span v-if="store.activeNoteState.id" @click="copy">{{store.authState.FRONTEND}}/{{store.authState.username}}/{{store.activeNoteState.id}}/</span>
      <button @click="save" :class="{ 'deactive': isSaving }" :disabled="isSaving">Save Note</button>
    </div>
  </div>
</template>

<style scoped>
.setting {
  display: flex;
  justify-content: space-between;
}

.left button {
  color: #ffffff;
  border-radius: 0;
  background-color: var(--tertiary-black);
  cursor: pointer;
}

.pin {
  margin-left: 8px;
  width: 120px;
}

.left .btn-left {
  border-radius: 5px 0px 0px 5px;
}

.left .btn-right {
  border-radius: 0px 5px 5px 0px;
}

.right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.right span {
  background-color: var(--tertiary-black);
  padding: 3px 15px;
  border-radius: 3px;
  cursor: pointer;
  color: #ebebeba3;
}

input {
  color: #ffffff;
  border-radius: 5px;
  border: 0;
  background-color: var(--tertiary-black);
  padding: 8px 15px;
}

input:focus-visible {
  outline: none;
  color: #fff;
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
  padding: 7px 15px;
  border: 1px solid red !important;
}

.deactive {
  animation: btn-bg 1s infinite;
}
</style>
