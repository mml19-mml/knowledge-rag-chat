<script setup lang="ts">
import ThemeSwitch from "./ThemeSwitch.vue";
import type {RagSource} from '../api/client';
const question=defineModel<string>({required:true});defineProps<{busy:boolean;error:string;messages:{role:string;text:string;time:string;sources?:RagSource[]}[];model:string;sourceCount:number}>();
const emit=defineEmits<{send:[];clear:[]}>();function keyboard(e:KeyboardEvent){if((e.metaKey||e.ctrlKey)&&e.key==='Enter'&&!e.isComposing){e.preventDefault();emit('send')}}
</script>
<template><div class="design-conversation"><div class="design-body min-h-screen bg-canvas text-ink antialiased selection:bg-blue-100 selection:text-primary flex flex-col justify-between font-sans">

<header class="sticky top-0 z-40 w-full backdrop-blur-xl bg-canvas/80 border-b border-hairline/80 transition-all duration-200">
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">

<div class="flex items-center space-x-3">
<div class="flex items-center space-x-2">
<div class="w-8 h-8 rounded-full ui-logo flex items-center justify-center shadow-sm">
<span class="material-symbols-outlined text-[18px]">smart_toy</span>
</div>
<h1 class="text-base sm:text-lg font-semibold tracking-[-0.015em] text-ink flex items-center gap-2">
        Knowledge Chat
      </h1>
</div>

<div class="ui-chat-status flex items-center space-x-1.5 px-2.5 py-0.5 rounded-full bg-emerald-50 border border-emerald-200/80 text-[11px] font-medium text-emerald-700">
<span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
<span class="">{{busy ? 'Working' : 'Chat'}}</span>
</div>
</div>

<div class="header-actions"><ThemeSwitch /><button class="apple-btn-spring group flex items-center space-x-1.5 px-3.5 py-1.5 rounded-full text-xs font-medium text-ink-subtle bg-surface border border-hairline hover:border-slate-300 hover:text-ink hover:bg-surface-secondary shadow-sm" aria-label="Clear Conversation" id="clearChatBtn" @click="$emit('clear')" :disabled="busy" title="Clear this chat history">
<span class="material-symbols-outlined text-[15px] text-ink-muted group-hover:text-red-500 transition-colors">delete_outline</span>
<span class="">Clear Conversation</span>
</button></div>
</div>
</header>

<div class="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 lg:py-8 flex-1 flex flex-col justify-start">
<div class="grid grid-cols-1 lg:grid-cols-12 gap-6 h-full items-stretch">

<div class="lg:col-span-7 flex flex-col gap-5 h-full">

<div class="bg-surface rounded-[24px] border border-hairline shadow-apple-card overflow-hidden flex flex-col transition-all duration-200 flex-1">

<div data-purpose="chat-heading" class="px-5 py-4 border-b border-hairline/80 flex items-center justify-between bg-surface/90 backdrop-blur-md">
<div class="flex items-center space-x-2.5">
<span class="text-lg font-bold text-ink-muted select-none">#</span>
<span class="text-base font-semibold text-ink tracking-tight">knowledge-base</span>
<span class="inline-flex items-center space-x-1.5 ml-2 px-2.5 py-0.5 rounded-full bg-emerald-50 border border-emerald-200/80 text-[11px] font-medium text-emerald-700">
<span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
<span class="">{{busy ? 'Searching' : 'Ready'}}</span>
</span>
</div>
<div class="text-xs text-ink-muted flex items-center gap-1.5">
<span class="material-symbols-outlined text-[15px]">lock_outline</span>
<span class="">Internal RAG</span>
</div>
</div>

<div class="p-5 sm:p-6 space-y-6 flex-1 overflow-y-auto" data-purpose="chat-stream-container" aria-live="polite" aria-label="Conversation">
<template v-for="(message,i) in messages" :key="i">
<div v-if="message.role==='你'" class="flex items-start space-x-3" data-purpose="user-message"><div class="w-8 h-8 rounded-full bg-gradient-to-tr from-slate-200 to-slate-100 border border-slate-300 flex items-center justify-center text-xs font-semibold text-slate-700 flex-shrink-0 shadow-sm">You</div><div class="flex-1 min-w-0 space-y-1"><div class="flex items-center space-x-2"><span class="text-sm font-semibold text-ink">You</span><span class="text-xs text-ink-muted tabular-nums">{{message.time}}</span></div><p class="text-[15px] leading-relaxed text-slate-800 whitespace-pre-wrap break-words"><span class="text-primary font-medium">@Atlas</span> {{message.text}}</p></div></div>
<div v-else class="flex items-start space-x-3" data-purpose="assistant-message"><div class="w-8 h-8 rounded-full ui-logo border border-hairline flex items-center justify-center flex-shrink-0 shadow-sm"><span class="material-symbols-outlined text-[17px]">smart_toy</span></div><div class="flex-1 min-w-0 space-y-2"><div class="flex items-center space-x-2"><span class="text-sm font-semibold text-ink">Atlas</span><span class="px-1.5 py-0.5 text-[9px] font-bold tracking-wider text-slate-600 bg-badge-agent rounded uppercase border border-slate-200/80">AGENT</span><span class="text-xs text-ink-muted tabular-nums">{{message.time}}</span></div><div class="bg-surface-secondary rounded-2xl p-4 border border-hairline/80 space-y-2.5"><p class="text-[15px] text-slate-700 leading-relaxed font-normal whitespace-pre-wrap break-words">{{message.text}}</p><ol v-if="message.sources?.length" aria-label="Answer sources" class="pt-1 flex flex-wrap items-center gap-2"><li v-for="(source,j) in message.sources" :key="j" class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-50 border border-blue-100 text-xs font-medium text-primary max-w-full"><span class="material-symbols-outlined text-[14px]">description</span><span class="break-words min-w-0">[{{j+1}}] {{source.filename}} · p. {{source.page_start}}<template v-if="source.page_end!==source.page_start">–{{source.page_end}}</template></span></li></ol></div></div></div>
</template><p v-if="busy" role="status" class="text-sm text-ink-subtle">Searching your knowledge base and preparing an answer…</p><p v-if="error" role="alert" class="text-sm text-red-700">{{error}}</p>

</div>
</div>

<footer class="w-full">
<div class="bg-surface rounded-[22px] border border-hairline shadow-apple-card p-4 sm:p-5 transition-all duration-300 focus-within:border-blue-400 focus-within:ring-4 focus-within:ring-blue-500/10" data-purpose="question-input-card">
<div class="text-[11px] font-bold uppercase tracking-wider text-ink-muted mb-2 select-none flex items-center justify-between">
<span class="">Your Question</span>
<span class="text-[10px] font-normal lowercase text-slate-400 tracking-normal hidden sm:inline">Ctrl / ⌘ + Enter to submit</span>
</div>
<div class="relative">
<textarea class="w-full bg-transparent border-0 p-0 text-ink placeholder-ink-muted/60 text-[15px] resize-none focus:ring-0 leading-relaxed min-h-[64px]" id="questionInput" v-model="question" maxlength="1000" :disabled="busy" @keydown="keyboard" aria-label="Your Question" placeholder="Ask a complete question about the knowledge base..." rows="2"></textarea>
</div>
<div class="pt-3 mt-1 border-t border-hairline/80 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
<p class="text-xs text-ink-muted select-none flex items-center gap-1.5">
<span class="material-symbols-outlined text-[14px] text-slate-400">verified_user</span>
<span class="">Grounded in uploaded knowledge.</span>
</p>
<div class="flex justify-end">
<button class="ui-primary-action apple-btn-spring inline-flex items-center justify-center space-x-1.5 px-4 sm:px-5 py-2 sm:py-2.5 bg-action hover:bg-action-hover active:bg-action-hover text-on-action font-medium text-sm rounded-xl shadow-button-tap transition-all" id="sendBtn" @click="$emit('send')" :disabled="busy || !question.trim()" type="button">
<span class="">{{busy?'Processing…':'Send Question'}}</span>
<span class="text-sm font-semibold tracking-tighter">↗</span>
</button>
</div>
</div>
</div>
</footer>
</div>

<div class="lg:col-span-5 h-full">
<div class="ui-companion bg-surface rounded-[24px] border border-hairline shadow-apple-card overflow-hidden flex flex-col p-6 sm:p-7 relative transition-all duration-200 h-full justify-between">

<div class="flex items-start justify-between mb-5">
<div>
<h2 class="text-2xl font-bold tracking-tight text-ink">Atlas</h2>
<p class="text-sm text-ink-muted mt-0.5">Knowledge Copilot &amp; Research Agent</p>
</div>
<span class="px-2.5 py-1 rounded-full bg-blue-50 text-primary font-semibold text-xs border border-blue-100 shadow-sm">
            @atlas
          </span>
</div>

<div class="mb-6">
<span class="block text-[10px] font-bold uppercase tracking-wider text-ink-muted mb-2.5">KNOWLEDGE &amp; CONNECTIONS</span>
<div class="flex flex-wrap gap-2">
<div class="inline-flex items-center space-x-1.5 px-2.5 py-1.5 rounded-lg border border-hairline bg-surface hover:bg-surface-secondary text-xs font-medium text-ink transition-colors shadow-sm">
<span class="material-symbols-outlined text-[15px] text-blue-600">description</span>
<span class="">Docs</span>
</div>
<div class="inline-flex items-center space-x-1.5 px-2.5 py-1.5 rounded-lg border border-hairline bg-surface hover:bg-surface-secondary text-xs font-medium text-ink transition-colors shadow-sm">
<span class="material-symbols-outlined text-[15px] text-slate-800">code</span>
<span class="" title="Not connected">GitHub · —</span>
</div>
<div class="inline-flex items-center space-x-1.5 px-2.5 py-1.5 rounded-lg border border-hairline bg-surface hover:bg-surface-secondary text-xs font-medium text-ink transition-colors shadow-sm">
<span class="material-symbols-outlined text-[15px] text-ink-muted">linear_scale</span>
<span class="" title="Not connected">Linear · —</span>
</div>
<div class="inline-flex items-center space-x-1.5 px-2.5 py-1.5 rounded-lg border border-hairline bg-surface hover:bg-surface-secondary text-xs font-medium text-ink transition-colors shadow-sm">
<span class="material-symbols-outlined text-[15px] text-ink-muted">article</span>
<span class="" title="Not connected">Notion · —</span>
</div>
</div>
</div>

<div class="relative rounded-2xl overflow-hidden bg-slate-900 border border-hairline/80 mb-6 aspect-[4/3] group"><img alt="Atlas AI Assistant Mascot" class="w-full h-full object-cover object-center select-none transform transition-transform duration-500 group-hover:scale-105" src="/robot-companion.png"><div class="absolute bottom-2.5 left-2.5 bg-surface/85 backdrop-blur-md px-2.5 py-1 rounded-full border border-hairline/80 text-[11px] font-medium text-ink-subtle flex items-center space-x-1.5 shadow-sm"><span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span><span class="">Knowledge Assistant</span></div></div>

<div class="grid grid-cols-2 gap-3 pt-1 border-t border-hairline/80">
<div class="ui-stat p-3 rounded-xl bg-surface-secondary/70 border border-hairline/60">
<div class="text-[10px] uppercase font-bold text-ink-muted tracking-wider">Cited Sources</div>
<div class="text-base font-semibold text-ink mt-0.5">{{sourceCount}} Documents</div>
</div>
<div class="ui-stat p-3 rounded-xl bg-surface-secondary/70 border border-hairline/60">
<div class="text-[10px] uppercase font-bold text-ink-muted tracking-wider">Response Model</div>
<div class="text-base font-semibold text-ink mt-0.5">{{model || 'Awaiting response'}}</div>
</div>
</div>
</div>
</div>
</div>
</div>

















</div></div></template>
<style scoped>

    /* Apple Spring Click Damping */
    .apple-btn-spring {
      transition: transform 0.18s cubic-bezier(0.34, 1.56, 0.64, 1), background-color 0.15s ease, box-shadow 0.18s ease;
    }
    .apple-btn-spring:active {
      transform: scale(0.97);
    }

    textarea:focus {
      outline: none !important;
      box-shadow: none !important;
    }

    /* Subtle minimalist scrollbar */
    ::-webkit-scrollbar {
      width: 5px;
    }
    ::-webkit-scrollbar-track {
      background: transparent;
    }
    ::-webkit-scrollbar-thumb {
      background: rgb(var(--ui-hairline));
      border-radius: 9999px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: rgb(var(--ui-muted));
    }
  
[data-purpose="chat-stream-container"]{overflow-wrap:anywhere}.grid>*{min-width:0}
.design-body{min-height:100vh}button:disabled{cursor:not-allowed;opacity:.55}button:focus-visible,a:focus-visible{outline:2px solid rgb(var(--ui-link));outline-offset:3px}
@media(max-width:480px){#clearChatBtn>span:last-child{display:none}#clearChatBtn{padding:8px;flex-shrink:0}}
</style>
