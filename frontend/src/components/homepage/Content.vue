<script setup>
import { onErrorCaptured, ref, inject } from 'vue'
import { useRouter } from 'vue-router'
import { viewErrorHandler } from '@/utils/errorHandler'

import HeroSection from "./HeroSection.vue"
import HeroSkeleton from "./HeroSkeleton.vue"
import SectionOne from "./SectionOne.vue"
import SectionTwo from "./SectionTwo.vue"
import SectionThree from "./SectionThree.vue"
import Error from "../templates/Error.vue"

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
  <div class="hero-section">
    <div class="container">
      <div class="hero">
        <h1>Share your NOTES in an easy way</h1>
        <span>Share your thoughts effortlessly. Create notes for public viewing or secure them with a PIN for controlled access—all with just a few clicks.</span>
        <hr>
      </div>
      <!-- skeleton loading -->
      <template v-if="!error">
        <Suspense>
          <template #default>
            <HeroSection />
          </template>
          <template #fallback>
            <HeroSkeleton />
          </template>
        </Suspense>
      </template>
      <Error :err="error" v-if="error" />
      <!-- skeleton loading -->
    </div>
  </div>
  <div class="section-one">
    <SectionOne />
  </div>
  <div class="section-two">
    <SectionTwo />
  </div>
  <div class="section-three">
    <SectionThree />
  </div>
</template>

<style scoped>
.hero-section {
  height: calc(100vh - 65px);
  display: flex;
  justify-content: center;
  background-image: url('@/assets/hero.webp');
  background-size: cover;
  background-position: center center;
  background-repeat: no-repeat;
  position: relative;
  z-index: 0;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.85);
  z-index: 1;
}

.hero-section .container {
  width: 1140px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  gap: 40px;
}

.hero {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 15px;
  position: relative;
  z-index: 2;
}

h1 {
  color: #ffffff;
  font-weight: 700;
}

h2 {
  color: #ffffff;
  font-weight: 700;
  font-size: 30px;
}

span {
  text-align: center;
  width: 350px;
  color: var(--accent);
  font-weight: 500;
}

hr {
  width: 80px;
  border: 0;
  border-top: 5px solid var(--tertiary-black);
  border-radius: 50px;
}

.section-one,
.section-three {
  background-color: black;
  display: flex;
  justify-content: center;
}

.section-two {
  background-color: var(--primary-black);
  display: flex;
  justify-content: center;
}
</style>
