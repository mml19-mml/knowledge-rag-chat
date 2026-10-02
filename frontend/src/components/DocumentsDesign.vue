<script setup lang="ts">
import {ref,watch} from 'vue';import type {DocumentRead} from '../api/client';const props=defineProps<{busy:boolean;error:string;notice:string;file:File|null;documents:DocumentRead[]}>();defineEmits<{refresh:[];lock:[];select:[file:File|null];upload:[];reindex:[id:string];remove:[doc:DocumentRead]}>();const input=ref<HTMLInputElement|null>(null);watch(()=>props.file,value=>{if(!value&&input.value)input.value.value=''})
</script>
<template><div class="design-documents"><div class="design-body text-ink antialiased selection:bg-blue-100 selection:text-blue-900">

<main class="max-w-3xl mx-auto px-6 py-12 md:py-24 flex flex-col justify-start">

<header class="flex flex-col md:flex-row md:items-start justify-between gap-4 mb-10" data-purpose="page-header">

<div>
<h1 class="text-3xl md:text-[38px] leading-tight font-semibold tracking-[-0.025em] text-ink font-display flex items-center gap-3">
          Knowledge Base Admin
        </h1>
<p class="mt-2 text-[17px] text-body-muted font-normal leading-relaxed tracking-[-0.01em]">
          Materials indexed here are utilized for verified Q&amp;A generation.
        </p>
</div>

<div class="pt-1.5 shrink-0">
<a class="inline-flex items-center gap-1.5 text-sm font-medium text-[#0066cc] hover:text-[#0071e3] transition-colors group px-3.5 py-1.5 rounded-full hover:bg-blue-50/70" data-purpose="link-to-qa" href="/">
<span class="">Go to Chat</span>
<span class="text-xs transition-transform duration-200 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 font-semibold">↗</span>
</a>
</div>
</header>


<section class="flex items-center justify-between mb-5" data-purpose="toolbar">

<div class="flex items-center gap-2.5 bg-white/70 border border-hairline/80 px-3 py-1.5 rounded-full shadow-sm">
<span class="inline-flex h-2 w-2 rounded-full bg-slate-400"></span>
<span class="text-sm font-medium text-ink tracking-tight">{{documents.length}} Documents</span>
</div>

<div class="flex items-center gap-2.5" data-purpose="action-buttons">
<button class="spring-press inline-flex items-center gap-1.5 px-3.5 py-1.5 text-sm font-medium text-ink bg-white/80 hover:bg-white border border-hairline shadow-sm rounded-lg backdrop-blur-md transition-all duration-200 hover:shadow" id="btn-refresh" @click="$emit('refresh')" :disabled="busy" type="button">
<span class="material-symbols-outlined text-base text-ink-muted-48">refresh</span>
<span class="">Refresh</span>
</button>
<button class="spring-press inline-flex items-center gap-1.5 px-3.5 py-1.5 text-sm font-medium text-ink bg-white/80 hover:bg-white border border-hairline shadow-sm rounded-lg backdrop-blur-md transition-all duration-200 hover:shadow" id="btn-lock" @click="$emit('lock')" :disabled="busy" type="button">
<span class="material-symbols-outlined text-base text-ink-muted-48">lock</span>
<span class="">Sign Out</span>
</button>
</div>
</section>


<section class="apple-glass rounded-2xl p-6 md:p-8 shadow-apple-card transition-shadow duration-300 hover:shadow-apple-elevated border border-black/[0.04] mb-8" data-purpose="upload-container">

<div class="mb-4 flex items-center justify-between">
<h2 class="text-base font-semibold text-ink tracking-tight font-display">
          Add PDF Document (Max 50 MB)
        </h2>
<span class="text-xs text-body-muted font-normal">PDF format only</span>
</div>

<div class="relative w-full mb-5">

<input accept="application/pdf" aria-label="Select PDF file" class="sr-only" id="pdf-file-input" ref="input" :disabled="busy" @change="$emit('select',($event.target as HTMLInputElement).files?.[0] ?? null)" type="file">

<label class="flex items-center w-full p-2 bg-canvas-parchment border border-hairline hover:border-slate-300 rounded-xl cursor-pointer shadow-subtle-inner transition-colors duration-150 group" for="pdf-file-input">

<span class="inline-flex items-center justify-center px-4 py-1.5 text-sm font-medium text-ink bg-white hover:bg-slate-50 border border-black/10 rounded-lg shadow-sm transition-all mr-3.5 select-none shrink-0 group-hover:border-black/20">
            Choose File
          </span>

<span class="text-sm text-body-muted font-normal truncate select-none group-hover:text-ink-muted-80" id="file-name-display">
            {{file?.name || 'No file selected'}}
          </span>
</label>
</div>

<div>
<button class="spring-press w-full py-3 px-5 rounded-xl text-white font-medium text-[15px] bg-ink hover:bg-neutral-800 active:bg-black shadow-sm hover:shadow transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-ink/40 flex items-center justify-center gap-2" id="btn-upload" @click="$emit('upload')" :disabled="busy" type="button">
<span class="material-symbols-outlined text-[19px]">cloud_upload</span>
<span class="">{{busy?'Processing…':'Upload & Process'}}</span>
</button>
</div>
</section>

<p v-if="busy" role="status" class="text-sm text-body-muted mb-4">Processing documents. Large PDFs may take several minutes; please keep this page open.</p><p v-if="error" role="alert" class="text-sm text-red-700 mb-4 break-words">{{error}}</p><p v-if="notice" role="status" class="text-sm text-emerald-700 mb-4">{{notice}}</p>
<article v-for="doc in documents" :key="doc.id" class="bg-white/80 border border-hairline rounded-2xl p-5 mb-4 shadow-apple-card"><div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4"><div class="min-w-0"><h3 class="font-semibold text-sm break-words">{{doc.filename}}</h3><p class="text-xs text-body-muted mt-1">{{doc.total_chunks}} chunks · {{doc.status}}</p></div><div class="flex gap-2 shrink-0"><button class="px-3 py-1.5 text-xs border border-hairline rounded-lg bg-white" :disabled="busy || doc.status!=='processed'" @click="$emit('reindex',doc.id)">Rebuild index</button><button class="px-3 py-1.5 text-xs border border-hairline rounded-lg bg-white text-red-700" :disabled="busy" @click="$emit('remove',doc)">Delete</button></div></div><p v-if="doc.error_message" class="text-xs text-red-700 mt-3 break-words">{{doc.error_message}}</p></article>

<div class="flex items-center gap-3 px-4 py-3 rounded-xl bg-white/40 border border-hairline/60 text-body-muted text-sm" data-purpose="empty-state" v-if="!documents.length">
<span class="material-symbols-outlined text-lg text-ink-muted-48 shrink-0">description</span>
<span class="tracking-tight">No documents indexed yet. Upload a PDF file to begin building your knowledge base.</span>
</div>

</main>






</div></div></template>
<style scoped>

    .design-body {
      background: linear-gradient(180deg, #fbfbfd 0%, #f4f6fa 100%);
      min-height: 100vh;
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", "Inter", sans-serif;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }
    
    .apple-glass {
      background: rgba(255, 255, 255, 0.88);
      backdrop-filter: blur(28px);
      -webkit-backdrop-filter: blur(28px);
      border: 1px solid rgba(255, 255, 255, 0.95);
    }
    
    .spring-press {
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .spring-press:active {
      transform: scale(0.98);
    }
  
#pdf-file-input:focus-visible+label{outline:2px solid #0071e3;outline-offset:3px}
.design-body{min-height:100vh}button:disabled{cursor:not-allowed;opacity:.55}button:focus-visible,a:focus-visible{outline:2px solid #0071e3;outline-offset:3px}
</style>
