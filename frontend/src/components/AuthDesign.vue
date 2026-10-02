<script setup lang="ts">
import {ref} from 'vue';const credential=defineModel<string>({required:true});defineProps<{busy:boolean;error:string}>();defineEmits<{unlock:[]}>();const showHelp=ref(false);
</script>
<template><div class="design-auth"><div class="design-body h-full flex flex-col justify-between text-ink selection:bg-blue-100 selection:text-primary">

<header class="w-full border-b border-black/[0.05] bg-white/70 backdrop-blur-xl sticky top-0 z-50">
<div class="max-w-5xl mx-auto px-6 h-14 flex items-center justify-between">
<div class="flex items-center gap-3">
<div class="w-6 h-6 rounded-md bg-ink flex items-center justify-center text-white text-[11px] font-bold tracking-tight">
          KB
        </div>
<span class="text-sm font-semibold tracking-tight text-ink">Knowledge&nbsp; Base</span>
</div>
<div>
<a class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium text-primary-container hover:text-primary bg-blue-50/60 hover:bg-blue-50 border border-blue-100/70 transition-all duration-150 group" href="/">
<span class="">Go to Chat</span>
<span class="text-xs transition-transform duration-150 group-hover:translate-x-0.5 group-hover:-translate-y-0.5">↗</span>
</a>
</div>
</div>
</header>

<main class="w-full max-w-4xl mx-auto px-6 py-12 md:py-16 flex-1 flex flex-col items-center justify-center">

<div class="text-center max-w-xl mx-auto mb-10 space-y-3" data-purpose="header-section">
<h1 class="text-3xl sm:text-4xl font-semibold tracking-tight text-ink leading-tight">
        Knowledge Base</h1>
<p class="text-base text-body-muted font-normal leading-relaxed">
        Internal documents configured for public and team Q&amp;A.
      </p>
</div>

<div class="w-full max-w-[440px]" data-purpose="security-card">
<div class="bg-white rounded-[24px] border border-black/[0.06] shadow-apple-float p-8 sm:p-10 transition-all duration-300">

<div class="flex flex-col items-center text-center pb-8">
<div class="w-12 h-12 rounded-2xl bg-surface-pearl border border-black/[0.04] flex items-center justify-center text-ink shadow-sm mb-4">
<span class="material-symbols-outlined text-[22px] text-ink-muted-80">lock</span>
</div>
<span class="text-[11px] font-semibold uppercase tracking-[0.08em] text-ink-muted-48">
            Administrator Credentials
          </span>
<p class="text-xs text-body-muted mt-1">
            Authentication required to inspect or modify knowledge indices.
          </p>
</div>

<form @submit.prevent="$emit('unlock')" class="space-y-5">
<div class="space-y-2">
<label class="block text-xs font-medium text-ink-muted-80 tracking-tight sr-only" for="admin-token">
              Admin Access Key
            </label>
<div class="relative">
<input autocomplete="off" class="w-full h-12 px-4 bg-surface-pearl/80 hover:bg-surface-pearl focus:bg-white border border-black/[0.08] focus:border-primary-focus rounded-xl text-ink text-sm placeholder:text-body-muted focus:outline-none focus:ring-4 focus:ring-blue-500/15 shadow-apple-input transition-all duration-200" id="admin-token" v-model="credential" :disabled="busy" name="admin-token" placeholder="Enter admin access key..." required type="password">
<div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none text-ink-muted-48">
<span class="material-symbols-outlined text-[18px]">key</span>
</div>
</div>
</div>

<button class="w-full h-12 rounded-xl bg-ink hover:bg-black text-white font-medium text-sm flex items-center justify-center gap-2 shadow-sm spring-press focus:outline-none focus:ring-4 focus:ring-black/10 cursor-pointer" type="submit" :disabled="busy">
<span class="">{{busy?'Authenticating…':'Authenticate & Enter'}}</span>
<span class="material-symbols-outlined text-[18px]">arrow_forward</span>
</button>
<p v-if="error" role="alert" class="text-sm text-red-700">{{error}}</p></form>

<div class="mt-7 pt-5 border-t border-hairline/60 text-center">
<p class="text-[12px] text-body-muted leading-relaxed flex items-center justify-center gap-1.5">
<span class="material-symbols-outlined text-[14px] text-ink-muted-48 inline-block">verified_user</span>
<span class="">Credentials are saved in local session memory and reset upon browser refresh.</span>
</p>
</div>
</div>
<p v-if="showHelp" id="access-note" class="mt-4 text-xs text-body-muted text-center">Use the administrator key configured for this installation. Ask the site owner if you do not have access.</p>
<div class="mt-6 text-center">
<a class="text-xs text-body-muted hover:text-ink font-medium tracking-tight transition-colors inline-flex items-center gap-1" href="#access-note" @click.prevent="showHelp=!showHelp">
<span class="">Need admin authorization?</span>
<span class="underline underline-offset-2">Ask the administrator</span>
</a>
</div>
</div>
</main>

<footer class="w-full py-8 border-t border-black/[0.04] text-center text-xs text-body-muted">
<div class="max-w-5xl mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-3">
<p class="">© Knowledge Base System · Administration</p>
<div class="flex items-center gap-6 text-[12px] text-body-muted">
<span class="inline-flex items-center gap-1.5">
<span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
          Access Controlled
        </span>
<span class="hover:text-ink cursor-pointer transition-colors">Key held in memory</span>
<span class="hover:text-ink cursor-pointer transition-colors">Refresh to lock</span>
</div>
</div>
</footer>


</div></div></template>
<style scoped>

    .design-body {
      background-color: #fbfbfd;
      background-image: 
        radial-gradient(at 10% 20%, rgba(235, 244, 255, 0.7) 0px, transparent 50%),
        radial-gradient(at 90% 10%, rgba(240, 243, 255, 0.6) 0px, transparent 40%),
        radial-gradient(at 50% 90%, rgba(245, 245, 247, 0.8) 0px, transparent 50%);
      background-attachment: fixed;
    }
    .spring-press {
      transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s ease, background-color 0.2s ease;
    }
    .spring-press:active {
      transform: scale(0.975);
    }
  
.design-body{min-height:100vh}button:disabled{cursor:not-allowed;opacity:.55}button:focus-visible,a:focus-visible{outline:2px solid #0071e3;outline-offset:3px}
</style>

