<template>
  <div class="h-[calc(100vh-180px)] flex flex-col items-center p-6 bg-neutral-900">

    <!-- === Header avec bouton New Chat === -->
<!-- === Header avec logo, titre et bouton New Chat === -->
<div class="w-full max-w-3xl flex justify-between items-center mb-4">



  <!-- Bouton New Chat -->
  <button
    @click="newChat"
    class="px-4 py-1.5 rounded-full font-semibold transition-all duration-200 flex items-center gap-2"
    style="background-color:#538CE6; color:white;"
  >
    💬 New Chat
  </button>
</div>
    <!-- === Header initial (avant tout message) === -->
    <div
      v-if="messages.length === 0"
      class="flex flex-col items-center space-y-6 w-full"
    >
    <div class="w-full max-w-3xl flex justify-between items-center mb-4"></div>
     <img src="/src/assets/img/logoo.png" alt="Logo" class="h-50 w-auto" />
      <h1 class="text-2xl font-bold text-white flex items-center gap-2 text-center">
        Hi MRE Team, what can I help with?
      </h1>

      <div
        class="w-full max-w-3xl flex items-center space-x-2 bg-neutral-800 rounded-full px-4 py-2 shadow-lg"
      >
        <!-- Upload fichier -->
        <label class="cursor-pointer text-white hover:text-blue-400 transition-colors">
          📎
          <input type="file" class="hidden" @change="handleFileUpload" />
        </label>

        <!-- Input -->
        <input
          v-model="message"
          @keyup.enter.exact.prevent="sendMessage"
          type="text"
          class="flex-1 bg-transparent text-white placeholder-neutral-400 focus:outline-none"
          placeholder="Ask your question..."
        />

        <!-- Bouton Send -->
        <button
          @click="sendMessage"
          :disabled="loading"
          class="bg-blue-500 text-white px-4 py-1.5 rounded-full font-semibold disabled:opacity-50"
        >
          {{ loading ? '...' : 'Send' }}
        </button>
      </div>
    </div>

    <!-- === Chat affichage messages === -->
    <div v-else class="w-full max-w-3xl flex flex-col flex-1">
      
      <!-- Zone scrollable des messages -->
      <div
        ref="chatScroll"
        class="flex-1 overflow-y-auto mb-4 space-y-4 pr-2 max-h-[calc(100vh-280px)] scroll-smooth"
      >
        <div
          v-for="(msg, index) in messages"
          :key="index"
          :class="[ 'flex', msg.sender === 'user' ? 'justify-end' : 'justify-start' ]"
        >
          <div
            :class="[
              'rounded-2xl px-4 py-3 text-sm shadow-md max-w-[75%] whitespace-pre-line',
              msg.sender === 'user'
                ? 'bg-blue-600 text-white'
                : 'bg-neutral-700 text-white'
            ]"
            v-html="msg.sender === 'bot' ? renderMarkdown(msg.text) : msg.text"
          ></div>
        </div>
      </div>

      <!-- Input en bas -->
      <div
        class="w-full flex items-center space-x-2 bg-neutral-800 rounded-full px-4 py-2 shadow-lg"
      >
        <input
          v-model="message"
          @keyup.enter.exact.prevent="sendMessage"
          type="text"
          class="flex-1 bg-transparent text-white placeholder-neutral-400 focus:outline-none"
          placeholder="Ask your question..."
        />
        <button
          @click="sendMessage"
          :disabled="loading"
          class="bg-blue-500 text-white px-4 py-1.5 rounded-full font-semibold disabled:opacity-50"
        >
          {{ loading ? '...' : 'Send' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { marked } from 'marked'

export default {
  data() {
    return {
      message: '',
      messages: JSON.parse(sessionStorage.getItem('chatHistory') || '[]'),
      loading: false,
    }
  },

  watch: {
    messages: {
      handler(newVal) {
        sessionStorage.setItem('chatHistory', JSON.stringify(newVal))
      },
      deep: true,
    }
  },

  methods: {
    /** Transforme texte en HTML Markdown */
    renderMarkdown(text) {
      return marked(text || '', { breaks: true })
    },

    /** Envoi message utilisateur */
    async sendMessage() {
      if (!this.message.trim()) return

      const userMessage = this.message
      this.messages.push({ text: userMessage, sender: 'user' })
      this.message = ''
      this.loading = true

      this.scrollToBottom()

      try {
        const res = await fetch('http://localhost:8000/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: userMessage }),
        })

        const data = await res.json().catch(() => null)

        if (data && data.reply) {
          this.messages.push({ text: data.reply, sender: 'bot' })
        } else {
          this.messages.push({ text: '❌ Réponse API vide ou invalide.', sender: 'bot' })
        }
      } catch (err) {
        console.error('Erreur fetch:', err)
        this.messages.push({ text: '❌ Erreur de communication avec MRE IA.', sender: 'bot' })
      } finally {
        this.loading = false
        this.scrollToBottom()
      }
    },

    /** Scroll automatique */
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.chatScroll
        if (container) container.scrollTop = container.scrollHeight
      })
    },

    /** Gestion des fichiers */
    handleFileUpload(event) {
      const file = event.target.files[0]
      if (file) {
        console.log('📎 Fichier sélectionné :', file.name)
      }
    },

    /** Démarre une nouvelle conversation */
    newChat() {
      this.messages = []
      sessionStorage.removeItem('chatHistory')
    },
  },
}
</script>

<style scoped>
.scroll-smooth {
  scroll-behavior: smooth;
}
</style>
