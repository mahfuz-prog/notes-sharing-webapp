<script setup>
import Error from '../components/templates/Error.vue'
import Content from '../components/userprofilepage/Content.vue'
import ContentSkeleton from '../components/userprofilepage/ContentSkeleton.vue'

import { onErrorCaptured, ref, inject } from 'vue'
import { useRouter } from 'vue-router'
import { viewErrorHandler } from '@/utils/errorHandler'

const store = inject("store")
const router = useRouter()

const error = ref("")

const viewErrorHandlerCallback = viewErrorHandler({
  store,
  router,
  errorRef: error
})

// handle error
onErrorCaptured(viewErrorHandlerCallback)
</script>
<template>
  <template v-if="!error">
    <div class="page">
      <Suspense>
        <template #default>
          <Content />
        </template>
        <template #fallback>
          <ContentSkeleton />
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
