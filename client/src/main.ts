import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import { VueQueryPlugin } from "@tanstack/vue-query";
import App from "./App.vue";

import Home from "./pages/Home/Home.vue";
import HostLobby from "./pages/HostLobby/HostLobby.vue";
import JoinRoom from "./pages/JoinRoom/JoinRoom.vue";
import GameRoom from "./pages/GameRoom/GameRoom.vue";
import Stats from "./pages/Stats/Stats.vue";
import NotFound from "./pages/NotFound/NotFound.vue";

import "vue3-toastify/dist/index.css";
import "./assets/global.css";

const router = createRouter({
	history: createWebHistory(),
	routes: [
		{ path: "/", name: "home", component: Home },
		{ path: "/host", name: "host", component: HostLobby },
		{ path: "/join", name: "join", component: JoinRoom },
		{ path: "/room/:id", name: "room", component: GameRoom },
		{ path: "/stats", name: "stats", component: Stats },
		{ path: "/:pathMatch(.*)*", name: "not-found", component: NotFound },
	],
});

createApp(App).use(router).use(VueQueryPlugin).mount("#app");
