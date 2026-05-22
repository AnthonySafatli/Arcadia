import type { Component } from "vue";

export interface SelectItem {
	id: string;
	name: string;
	icon: Component | null;
	tags: string[];
}
