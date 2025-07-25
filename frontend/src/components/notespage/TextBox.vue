<script setup>
import { ref, inject, watch, watchEffect } from 'vue'
import { MAX_TEXT_LENGTH } from '@/utils/validation'

const store = inject("store")
const { props } = defineProps(['props'])

const text = ref("")
const isInvalid = ref(false)

watchEffect(() => {
  text.value = props
})

// check and validate input text.
watch(text, (newVal, oldVal) => {
  if (newVal === "") {
    isInvalid.value = true
  } else if (text.value.length >= MAX_TEXT_LENGTH + 1) {
    text.value = newVal.slice(0, MAX_TEXT_LENGTH + 1)
    isInvalid.value = true
  } else {
    isInvalid.value = false
  }
  store.tempNoteActions.editText(text.value)
})
</script>
<template>
  <textarea id="text" v-model.trim="text" placeholder="What's on your MIND?" :class="{ 'invalid-border': isInvalid }" spellcheck="false" :disabled="store.notesState.noteList.size === 0" />
</template>

<style scoped>
textarea#text {
  height: 100%;
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

.invalid-border {
  padding: 9px !important;
  border: 1px solid red !important;
}
</style>
