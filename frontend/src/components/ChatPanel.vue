<script setup lang="ts">
import { ref, nextTick } from 'vue';
import { askRag, type RagSource } from '../api/client';
import WelcomeDesign from './WelcomeDesign.vue';
import ConversationDesign from './ConversationDesign.vue';
type Message = { time:string; role: string; text: string; sources?: RagSource[] };
const messages = ref<Message[]>([]);
const question = ref('');
const busy = ref(false);
const error = ref('');
const model = ref('');
const latestSourceCount = ref(0);
function clearChat() { messages.value=[]; error.value=''; model.value=''; latestSourceCount.value=0; }
function keyboard(event:KeyboardEvent) { if(event.key==='Enter' && !event.shiftKey && !event.isComposing) { event.preventDefault(); void send(); } }

async function send() {
  const text = question.value.trim();
  if (!text || busy.value) return;
  busy.value = true; error.value = ''; question.value = '';
  messages.value.push({role:'你', text,time:new Date().toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'})});
  try {
    const response = await askRag('', text, '');
    model.value=response.model || ''; latestSourceCount.value=new Set(response.sources.map(s=>s.document_id)).size;
    messages.value.push({role:'知识助手',time:new Date().toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'}),text:response.answer,sources:response.sources});
  } catch { error.value = '暂时无法回答，请稍后重试。'; question.value = text; }
  finally { busy.value = false; await nextTick(); document.querySelector('[data-purpose="chat-stream-container"]')?.lastElementChild?.scrollIntoView({behavior:'smooth',block:'nearest'}); }
}
</script>
<template><WelcomeDesign v-if="!messages.length" v-model="question" :busy="busy" :error="error" @send="send"/><ConversationDesign v-else v-model="question" :busy="busy" :error="error" :messages="messages" :model="model" :source-count="latestSourceCount" @send="send" @clear="clearChat"/></template>