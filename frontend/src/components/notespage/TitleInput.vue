<script setup>
import { ref, watch, inject, watchEffect } from 'vue'
import { MAX_TITLE_LENGTH } from '@/utils/validation'

const store = inject("store")
const { props } = defineProps(['props'])

const title = ref("")
const isInvalid = ref(false)

watchEffect(() => {
  title.value = props
})

// check and validate input text.
watch(title, (newVal, oldVal) => {
  if (newVal === "") {
    isInvalid.value = true
  } else if (title.value.length >= MAX_TITLE_LENGTH + 1) {
    title.value = newVal.slice(0, MAX_TITLE_LENGTH + 1)
    isInvalid.value = true
  } else {
    isInvalid.value = false
  }
  store.tempNoteActions.editTitle(title.value)
})
</script>
<template>
  <div class="title">
    <input type="text" v-model.trim="title" :class="{ 'invalid-border': isInvalid }" placeholder="Please give a title" spellcheck="false" :disabled="store.notesState.noteList.size === 0">
  </div>
</template>

<style scoped>
.title input {
  width: 100%;
  color: #ffffff;
  font-size: 14px;
  padding: 10px 15px;
  background-color: var(--secondary-black);
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
</style>
