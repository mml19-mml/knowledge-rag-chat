<script setup lang="ts">
import { ref, onBeforeUnmount } from 'vue';
import { listDocuments, uploadDocument, deleteDocument, reindexDocument, type DocumentRead } from '../api/client';
import AuthDesign from './AuthDesign.vue';
import DocumentsDesign from './DocumentsDesign.vue';
const key = ref(''); const token = ref(''); const documents = ref<DocumentRead[]>([]);
const file = ref<File | null>(null); const busy = ref(false); const error = ref(''); const notice = ref('');
const fileInput = ref<HTMLInputElement | null>(null);
onBeforeUnmount(() => { token.value = ''; key.value = ''; });
async function run(action: () => Promise<void>) {
  if (busy.value) return;
  busy.value=true; error.value=''; notice.value='';
  try { await action(); } catch(e) { error.value=e instanceof Error ? e.message : '操作失败'; }
  finally { busy.value=false; }
}
async function refresh() { documents.value=await listDocuments(token.value); }
function unlock() { return run(async()=>{const candidate=key.value.trim(); const result=await listDocuments(candidate); token.value=candidate; key.value=''; documents.value=result;}); }
function selectFile(candidate:File | null) { error.value=''; if(candidate && (!candidate.name.toLowerCase().endsWith('.pdf') || candidate.size>50*1024*1024)) { error.value='请选择不超过 50 MB 的 PDF 文件。'; file.value=null; if(fileInput.value)fileInput.value.value=''; return; } file.value=candidate; }
function drop(event:DragEvent) { if(!busy.value)selectFile(event.dataTransfer?.files[0] ?? null); }
function statusLabel(status:string) { return ({processed:'处理完成',processing:'处理中',pending:'等待处理',failed:'处理失败'} as Record<string,string>)[status] || status; }
function upload() { return run(async()=>{if(!file.value)return; await uploadDocument(token.value,file.value); file.value=null;if(fileInput.value)fileInput.value.value='';await refresh();notice.value='处理已结束，请检查下方状态与索引提示。';}); }
function remove(doc:DocumentRead) { if(window.confirm(`删除「${doc.filename}」及其知识片段？`))return run(async()=>{await deleteDocument(token.value,doc.id);await refresh();}); }
function reindex(id:string) { return run(async()=>{await reindexDocument(token.value,id);await refresh();notice.value='已尝试重建索引，请检查下方结果。';}); }
function lock() { token.value='';key.value='';documents.value=[];error.value='';notice.value='';file.value=null; }
</script>
<template><AuthDesign v-if="!token" v-model="key" :busy="busy" :error="error" @unlock="unlock"/><DocumentsDesign v-else :busy="busy" :error="error" :notice="notice" :file="file" :documents="documents" @refresh="run(refresh)" @lock="lock" @select="selectFile" @upload="upload" @reindex="reindex" @remove="remove"/></template>