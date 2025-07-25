<script setup>
import { ref, inject, onErrorCaptured } from "vue"
import { useRouter } from "vue-router"
import { useNotification } from "@kyvg/vue3-notification"
import { viewErrorHandler } from '@/utils/errorHandler'

import Error from "../components/templates/Error.vue"
import Content from "../components/accountpage/Content.vue"

const store = inject("store")
const router = useRouter()
const notification = useNotification()

const error = ref("")
const viewErrorHandlerCallback = viewErrorHandler({
  store,
  router,
  errorRef: error
})


// handle error
onErrorCaptured(viewErrorHandlerCallback)

// if there is no auth token than return login page
if (!store.authState.token) {
  router.push({ name: "login" })
  notification.notify({ title: "Log in required!", text: "Please log in to access this page." })
}
</script>
<template>
  <template v-if="!error">
    <div class="page">
      <Suspense>
        <template #default>
          <Content />
        </template>
        <template #fallback>
          <span>Loading...</span>
        </template>
      </Suspense>
    </div>
  </template>
  <Error :err="error" v-if="error" />
</template>

<style scoped>
.page {
  height: calc(100vh - 65px - 42px);
  display: grid;
  place-items: center;
  background-color: var(--primary-black);
}
</style>
