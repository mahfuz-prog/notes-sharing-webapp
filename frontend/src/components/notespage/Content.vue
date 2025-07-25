<script setup>
import { ref, inject, nextTick } from 'vue'
import { useNotification } from '@kyvg/vue3-notification'
import { useRouter, useRoute } from 'vue-router'

import axios from 'axios'
import DeleteIcon from '../icons/DeleteIcon.vue'
import Settings from './Settings.vue'
import TitleInput from './TitleInput.vue'
import TextBox from './TextBox.vue'
import Pagination from './Pagination.vue'
import NewNotePopup from './NewNotePopup.vue'

const store = inject("store")
const notification = useNotification()
const router = useRouter()
const route = useRoute()

const isDeleting = ref(false)
const isPopupVisible = ref(false)


// load notes, skeleton loading
try {
  const initialPage = route.query.page ? parseInt(route.query.page) : 1
  const initialUrl = `/notes/?page=${initialPage}`
  const { data } = await axios.get(initialUrl, { headers: store.authActions.getAuthorizationHeader() })

  // Check data.notes exists and has length
  if (data.notes && data.notes.length > 0) {
    store.notesStateActions.setNotes(data)
      // Ensure noteList is populated before trying to select active note
    if (store.notesState.noteList.size > 0) {
      const [id, firstNote] = store.notesState.noteList.entries().next().value
      store.activeNoteActions.setActiveNote(id, firstNote.title, firstNote.text, firstNote.dateCreated, firstNote.pin)
    }
  } else {
    // If no notes, clear states
    store.notesStateActions.resetNotes()
    store.activeNoteActions.clearActiveNote()
  }
} catch (err) {
  throw err
}


// delete note
const deleteNote = async(id) => {
  let confirmationMessage = "Are you sure you want to delete this note?"

  // If there are unsaved edits, append a warning to the confirmation message
  if (store.tempNoteActions.isEdited) {
    confirmationMessage = "You have unsaved edits on the current note. If you proceed, these edits will be lost. Are you sure you want to delete this note?"
  }

  // Display a single confirmation dialog
  const isConfirmed = confirm(confirmationMessage)

  if (!isConfirmed) {
    return
  }

  // Set loading state to true
  isDeleting.value = true
  try {
    const { data } = await axios.post('/notes/delete-note/', { "note_id": id }, { headers: store.authActions.getAuthorizationHeader() })

    // delete the note from reactive obj
    store.notesStateActions.deleteNote(parseInt(data.id))
    notification.notify({
      title: data.title.slice(0, 25),
      text: "Note deleted successfully."
    })

    // if all notes deleted
    if (store.notesState.noteList.size === 0) {
      // this is for remove pagination
      if (!store.notesState.pagination.currentPage || store.notesState.pagination.currentPage === 1) {
        router.go(route.fullPath)
        return
      }

      // if there is next page
      if (store.notesState.pagination.hasNext) {
        router.go(route.fullPath)
        return
      }

      // if only previous page
      if (store.notesState.pagination.hasPrev) {
        router.push({ name: 'notes', query: { page: store.notesState.pagination.currentPage - 1 } })
        return
      }
    }

    // Check if the deleted note was the active one
    if (store.activeNoteState.id === parseInt(data.id)) {
      // Select the first available note if notes still exist
      const [newActiveId, firstNote] = store.notesState.noteList.entries().next().value
      store.activeNoteActions.setActiveNote(newActiveId, firstNote.title, firstNote.text, firstNote.dateCreated, firstNote.pin)
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
    isDeleting.value = false
  }
}

// select note
const selectNote = (id) => {
  // prevent new select if current note is edited
  if (store.tempNoteActions.isEdited) {
    const isConfirmed = confirm("Save the note. Otherwise your edit will be lost.")
    if (!isConfirmed) {
      return
    }
  }

  // select active note
  const selectedNote = store.notesState.noteList.get(id)
  store.activeNoteActions.setActiveNote(id, selectedNote.title, selectedNote.text, selectedNote.dateCreated, selectedNote.pin)
}

// new note
const newNote = () => {
  // prevent new select if current note is edited
  if (store.tempNoteActions.isEdited) {
    const isConfirmed = confirm("Save the note. Otherwise your edit will be lost.")
    if (!isConfirmed) {
      return
    }
  }

  isPopupVisible.value = true
}
</script>
<template>
  <div class="layout">
    <div class="side-bar">
      <!-- btn -->
      <div class="new-note">
        <button @click="newNote" class="btn">New Note</button>
        <span v-if="store.notesState.noteList.size === 0">Please create a note first.</span>
        <NewNotePopup v-if="isPopupVisible" @close="isPopupVisible = false" />
      </div>
      <!-- note list -->
      <div class="notes">
        <TransitionGroup tag="div" name="note-list" :key="store.notesState.pagination.currentPage || ''">
          <template v-for="[id, note] in store.notesState.noteList" :key="id">
            <div class="lists" :class="{ 'border': store.activeNoteState.id === id }">
              <button @click="selectNote(id)"> {{ note.title.slice(0,20) }} ... </button>
              <button @click="deleteNote(id)" :disabled="isDeleting" class="delete-button">
                <DeleteIcon :width="16" :height="18" :iconFillColor="isDeleting ? '#a0a0a0' : '#dc3545'" />
              </button>
            </div>
          </template>
        </TransitionGroup>
      </div>
      <!-- notes pagination -->
      <Pagination :props="store.notesState.pagination" v-if="store.notesState.pagination.currentPage" />
    </div>
    <div class="input-box">
      <Settings :props="store.activeNoteState.pin" />
      <TitleInput :props="store.activeNoteState.title" />
      <TextBox :props="store.activeNoteState.text" />
    </div>
  </div>
</template>

<style scoped>
.layout {
  width: 1140px;
  height: calc(100vh - 160px);
  display: flex;
  gap: 10px;
}

.side-bar {
  width: 360px;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 15px 10px;
  gap: 15px;
  border: 1px solid var(--tertiary-black);
  border-radius: 5px;
  overflow: none;
}

.notes {
  display: flex;
  flex-direction: column;
}

.lists {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--secondary-black);
  border-radius: 3px;
  gap: 10px;
  padding-right: 14px;
  border: 1px solid transparent;
  transition: all 0.3s ease;
  margin-bottom: 10px;
}

.notes > div > .lists:last-of-type {
  margin-bottom: 0;
}

.side-bar button {
  width: 100%;
  background-color: transparent;
  padding: 11px 14px;
  font-size: 14px;
  cursor: pointer;
  color: #ffffff;
  border: 0;
  text-align: left;
}

.delete-button {
  padding: 0;
  width: 0 !important;
}

.input-box {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.new-note {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.side-bar .btn {
  background-color: var(--accent);
  padding: 12px 15px;
  font-size: 14px;
  border-radius: 25px;
  cursor: pointer;
  color: #ffffff;
  border: 0;
  text-align: center;
  margin-bottom: 5px;
}

.border {
  border: 1px solid var(--accent) !important;
}

.new-note {
  display: flex;
  flex-direction: column;
}

.new-note span {
  text-align: center;
  padding-top: 10px;
}


/*animation*/

.note-list-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.note-list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>
