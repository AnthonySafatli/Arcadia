<template>
	<router-view v-slot="{ Component }">
		<transition name="fade-slide" mode="out-in">
			<component :is="Component" :key="$route.path" />
		</transition>
	</router-view>
</template>

<style>
#app {
	height: 100%;
}
</style>
