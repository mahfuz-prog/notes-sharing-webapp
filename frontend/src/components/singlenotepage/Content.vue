<script setup>
import { ref, inject } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useNotification } from '@kyvg/vue3-notification'
import { validateName } from '@/utils/validation'
import { copyToClipboard } from '@/utils/helper'

import axios from 'axios'
import Popup from '../singlenotepage/Popup.vue'
import UserIcon from '../icons/UserIcon.vue'
import CalenderIcon from '../icons/CalenderIcon.vue'
import CopyIcon from '../icons/CopyIcon.vue'
import Error from "../templates/Error.vue"

const store = inject("store")
const route = useRoute()
const router = useRouter()
const pinRequired = ref(false)
const notification = useNotification()
const hasPreRequestError = ref(false)

const note = ref({
  username: "",
  date: "",
  title: "",
  text: ""
})

const payload = ref({
  "username": route.params.username,
  "note_id": route.params.id,
})

// date formate
const getDate = (dateString) => {
  const date = new Date(dateString)
  const options = { weekday: "short", year: "numeric", month: "short", day: "numeric", }
  const formatter = new Intl.DateTimeFormat('en-US', options)
  return formatter.format(date)
}


// Validate payload.value.username
if (!payload.value.username || !validateName(payload.value.username) || payload.value.username.includes(' ')) {
  hasPreRequestError.value = true
}

// Validate payload.value.note_id
if (!payload.value.note_id || String(payload.value.note_id).length > 10) {
  hasPreRequestError.value = true
}

// skeleton loading
try {
  if (!hasPreRequestError.value) {
    const { data } = await axios.post('/main/single-note/', payload.value)

    note.value.username = data.username
    note.value.date = getDate(data.date)
    note.value.title = data.title
    note.value.text = data.text
  }
} catch (err) {
  // pin required note
  if (err.response && err.response.status === 401) {
    pinRequired.value = true
  } else {
    throw err
  }
}


// handle pin submit
const handlePopup = (data) => {
  note.value.username = data.username
  note.value.date = getDate(data.date)
  note.value.title = data.title
  note.value.text = data.text

  pinRequired.value = false
}


// url copy clipboard
const copy = () => {
  copyToClipboard(note.value.text)
    .then(() => {
      notification.notify({ title: "Text copied to clipboard!", text: note.value.text.slice(0, 25) })
    })
    .catch(err => {
      notification.notify({ title: "Failed to copy!", text: note.value.text.slice(0, 25) })
    })
}
</script>
<template>
  <template v-if="!hasPreRequestError">
    <Popup v-if="pinRequired" :payload="payload" @success="handlePopup" />
    <div class="container">
      <div class="head">
        <div class="left">
          <div class="user">
            <UserIcon width="14" />
            <a :href="`${store.authState.FRONTEND}/user/${ note.username }/`">
          {{ note.username.replace(/\b\w/g, char => char.toUpperCase()).replace('-', ' ') }}
        </a>
          </div>
          <div class="clock">
            <CalenderIcon width="22" height="22" />
            <p>{{ note.date }}</p>
          </div>
        </div>
        <div class="right">
          <CopyIcon :width="20" :height="20" @click="copy" />
        </div>
      </div>
      <hr>
      <div class="content">
        <h4>{{ note.title }}</h4>
        <span>{{ note.text }}</span>
      </div>
    </div>
  </template>
  <template v-else>
    <Error :err="'Invalid username and id.'" />
  </template>
</template>

<style scoped>
.container {
  width: 1140px;
  height: calc(100vh - 150px);
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  border: 1px solid var(--tertiary-black);
  border-radius: 5px;
  padding: 20px;
}

.content {
  display: block;
  word-wrap: break-word;
  overflow-wrap: break-word;
  white-space: pre-wrap;
  line-height: 1.5;
  overflow: scroll;
  scrollbar-color: var(--accent) transparent;
  scrollbar-width: thin;
  height: 100%;
}

.head {
  display: flex;
  justify-content: space-between;
}

h4 {
  color: #ffffff;
  font-weight: 500;
  font-size: 19px;
  line-height: 23px;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.left .user,
.clock {
  display: flex;
  align-items: center;
  gap: 8px;
}

a,
p {
  font-size: 13px;
  color: #ebebeba3;
}

.right svg {
  cursor: pointer;
}

span {
  color: #ffffff;
}

hr {
  border: 0;
  border-top: 1px solid var(--accent) !important;
}
</style>
