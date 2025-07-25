<script setup>
import { ref, inject, watch, watchEffect } from 'vue'
import { useNotification } from '@kyvg/vue3-notification'
import { useRouter, useRoute } from 'vue-router'

import axios from 'axios'

const { props } = defineProps(['props'])
const store = inject("store")
const notification = useNotification()
const router = useRouter()
const route = useRoute()

const pagination = ref({})
const isChanging = ref(false)


// when an new note select this triger
// pagination = { "currentPage": "", "hasPrev": "", "hasNext": "", "pageList": [] } 
watchEffect(() => {
  pagination.value = props
})


// change pagination pages
const changePage = async(num) => {
  isChanging.value = true
  try {
    const url = `/notes/?page=${num}`
    const { data } = await axios.get(url, { headers: store.authActions.getAuthorizationHeader() })
    if (data.notes.length > 0) {
      // store all notes in reactive obj
      store.notesStateActions.setNotes(data)

      // select active note
      // Ensure noteList is populated before trying to select active note
      if (store.notesState.noteList.size > 0) {
        const [id, firstNote] = store.notesState.noteList.entries().next().value
        store.activeNoteActions.setActiveNote(id, firstNote.title, firstNote.text, firstNote.dateCreated, firstNote.pin)
      }
    }
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
    isChanging.value = false
  }
}


// Handles the click event for pagination buttons
const handlePageClick = (pageNumber) => {
  if (store.tempNoteActions.isEdited) {
    const isConfirmed = confirm("Save the note. Otherwise your edit will be lost.")
    if (!isConfirmed) {
      return
    }
  }

  router.push({ name: 'notes', query: { page: pageNumber } })
}


// trigger if query value changes
watch(() => route.query.page, (newPage, oldPage) => {
  if (newPage && newPage !== oldPage) {
    // Call changePage with the new page number from the URL
    changePage(parseInt(newPage))
  } else if (!newPage && oldPage) {
    // If page query is removed, default to page 1
    changePage(1)
  }
})
</script>
<template>
  <div class="pagination">
    <div class="pages">
      <div v-for="page in pagination.pageList">
        <button class="btn-box" :class="{'active-page' : pagination.currentPage === page, 'deactive': isChanging}" v-if="page" @click="handlePageClick(page)">{{page}}</button>
        <button v-else>...</button>
      </div>
    </div>
    <div class="prev-next-page" v-if="pagination.currentPage">
      <button :disabled="!pagination.hasPrev || isChanging" :class="{'is-disabled' : !pagination.hasPrev, 'deactive': isChanging}" @click="handlePageClick(pagination.currentPage - 1)">Previous</button>
      <button :disabled="!pagination.hasNext || isChanging" :class="{ 'is-disabled' : !pagination.hasNext, 'deactive': isChanging}" @click="handlePageClick(pagination.currentPage + 1)">Next</button>
    </div>
  </div>
</template>

<style scoped>
.pagination {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.pages {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap: 8px;
}

button {
  color: #ffffff;
  background-color: transparent;
  border: 0;
  padding: 0;
}

.btn-box {
  border: 1px solid var(--tertiary-black);
  border-radius: 3px;
  padding: 7px 10px;
  font-size: 12px;
  line-height: 12px;
  cursor: pointer;
}

.active-page {
  background-color: var(--accent);
}

.prev-next-page {
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 3px;
}

.prev-next-page button {
  background-color: var(--accent);
  padding: 7px 15px;
  border-radius: 3px;
  font-size: 12px;
  cursor: pointer;
}

.is-disabled {
  opacity: .5;
  cursor: not-allowed;
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
