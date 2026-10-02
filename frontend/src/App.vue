<script setup lang="ts">
import ChatPanel from './components/ChatPanel.vue';
import AdminPanel from './components/AdminPanel.vue';
const path = window.location.pathname.replace(/\/+$/, '') || '/';
</script>
<template>
  <AdminPanel v-if="path === '/admin'" />
  <ChatPanel v-else-if="path === '/'" />
  <main v-else><h1>页面不存在</h1><a href="/">返回问答</a></main>
</template>
<style>
@font-face{font-family:Inter;src:url('/fonts/inter.ttf') format('truetype');font-weight:100 900;font-display:swap}
@font-face{font-family:'Material Symbols Outlined';src:url('/fonts/symbols.ttf') format('truetype');font-weight:100 700;font-display:block}
.material-symbols-outlined{font-family:'Material Symbols Outlined';font-weight:normal;font-style:normal;font-size:24px;line-height:1;letter-spacing:normal;text-transform:none;display:inline-block;white-space:nowrap;word-wrap:normal;direction:ltr;font-feature-settings:'liga';-webkit-font-smoothing:antialiased}
body{margin:0}button{cursor:pointer}button:disabled{cursor:not-allowed}#app{min-height:100vh}*{overflow-wrap:break-word}@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}}
</style>