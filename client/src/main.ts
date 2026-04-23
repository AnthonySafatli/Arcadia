import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

import Home from './pages/Home/Home.vue'
import HostLobby from './pages/HostLobby/HostLobby.vue'
import JoinRoom from './pages/JoinRoom/JoinRoom.vue'
import GameRoom from './pages/GameRoom/GameRoom.vue'

import './assets/global.css'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: Home },
    { path: '/host', name: 'host', component: HostLobby },
    { path: '/join', name: 'join', component: JoinRoom },
    { path: '/room/:id', name: 'room', component: GameRoom },
  ],
})

createApp(App).use(router).mount('#app')
