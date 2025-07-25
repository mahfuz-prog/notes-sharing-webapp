<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { validateName } from '@/utils/validation'

import axios from 'axios'
import LockIcon from '../icons/LockIcon.vue'
import Error from "../templates/Error.vue"

const route = useRoute()

const info = ref({})
const hasPreRequestError = ref(false)
const username = ref(route.params.username || "")

// Validate payload.value.username
if (!username.value || !validateName(username.value) || username.value.includes(' ')) {
  hasPreRequestError.value = true
}

if (!hasPreRequestError.value) {
  try {
    const { data } = await axios.get(`/main/user-profile/${username.value}/`)
    info.value = data
  } catch (err) {
    throw err
  }
}

// date formate
const getDate = (dateString) => {
  const date = new Date(dateString)
  const options = { weekday: "short", year: "numeric", month: "short", day: "numeric", }
  const formatter = new Intl.DateTimeFormat('en-US', options)
  return formatter.format(date)
}
</script>
<template>
  <template v-if="!hasPreRequestError">
    <div class="layout">
      <div class="profile">
        <img src="@/assets/user-icon.png" width="110">
        <span class="name"> {{ username.replace(/\b\w/g, char => char.toUpperCase()).replace('-', ' ') }} </span>
        <hr>
      </div>
      <div class="notes" v-if="info.length > 0">
        <template v-for="note in info">
          <router-link :to="{ name: 'singlenote', params: { username: note.username, id: note.id } }" target="_blank" rel="noopener noreferrer">
            <div class="note">
              <span> {{ note.title.slice(0, 40) }} ... </span>
              <div class="meta">
                <template v-if="note.isLocked">
                  <LockIcon width="20" height="20" />
                </template>
                <span> {{ getDate(note.dateCreated) }} </span>
              </div>
            </div>
          </router-link>
        </template>
      </div>
      <template v-else>
        <span>No Notes found!</span>
      </template>
    </div>
  </template>
  <template v-else>
    <Error :err="'Invalid username.'" />
  </template>
</template>

<style scoped>
.layout {
  width: 500px;
  max-height: calc(100vh - 160px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 40px;
  border: 1px solid var(--tertiary-black);
  border-radius: 5px;
  padding: 20px;
}

.profile {
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: center;
  justify-content: center;
}

.notes {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 8px;
  overflow: scroll;
  scrollbar-width: none;
  -ms-overflow-style: none;
  &::-webkit-scrollbar {
    display: none;
  }
}

.note {
  display: flex;
  justify-content: space-between;
  border: 1px solid var(--tertiary-black);
  border-radius: 5px;
  padding: 10px;
}

span {
  font-size: 13px;
}

.meta {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

img {
  border-radius: 50%;
  border: 3px solid var(--accent);
  width: 110px;
  height: 110px;
}

hr {
  border: none;
  height: 5px;
  width: 60px;
  background-color: var(--tertiary-black);
  border-radius: 5px;
}

.name {
  font-size: 18px;
  color: #ffffff;
}
</style>
