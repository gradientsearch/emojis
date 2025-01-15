<script lang="ts">
	import { onMount } from 'svelte';
	import { getData } from './services/emoji.service';
	import { SvelteMap } from 'svelte/reactivity';

	let emojis: any = $state(undefined);
	let toasts: Map<string, any> = $state(new SvelteMap<string, any>());
	onMount(async () => {
		let [resp, err] = await getData();
		if (err !== undefined) {
			console.log('TODO: popup a toast');
		} else {
			emojis = JSON.parse(resp);
		}
	});

	function copy(emoji: any) {
		navigator.clipboard.writeText(emoji['emoji']).then(
			() => {
				let id = crypto.randomUUID();

				toasts.set(id, emoji);
				setTimeout(() => {
					toasts.delete(id);
				}, 2000);
			},
			() => {
				// Failed to copy text
				console.error('Failed to copy text');
			}
		);
	}
</script>

<header class="bg-base-100 sticky top-0 flex h-[48px] items-center justify-center p-1">
	<div class="flex">
		<h1 class="text-center text-lg font-extrabold">
			😀 <span class="text-base-700">Git</span><span class="text-primary-600">Emojis</span> 😀
		</h1>
	</div>
</header>

<div class="flex h-full w-full justify-center">
	<div class="w-full max-w-2xl lg:max-w-5xl lg:text-2xl">
		{#if emojis}
			{#each Object.keys(emojis) as category}
				<div class="mx-4 mt-10">
					<h1 class="font-bold capitalize">{category}</h1>
					{#each Object.keys(emojis[category]) as subcategory}
						<div class="py-4">
							<h2 class="capitalize">{subcategory.replaceAll('-', ' ')}</h2>
						</div>
						<div class="flex flex-wrap lg:text-3xl">
							{#each Object.keys(emojis[category][subcategory]) as emoji}
								<button
									onclick={() => {
										copy(emojis[category][subcategory][emoji]);
									}}
									class="flex flex-wrap border p-4"
								>
									<span>
										{emojis[category][subcategory][emoji]['emoji']}
									</span>
								</button>
							{/each}
						</div>
					{/each}
				</div>
			{/each}
		{/if}
	</div>
</div>

{#each toasts.keys() as t}
	<aside
		class=" bg-base-900 text-base-200 fixed bottom-4 end-4 z-50 flex items-center justify-center gap-4 rounded-lg px-5 py-3"
	>
		<p>
			Copied {toasts.get(t)['name']}
			{toasts.get(t)['emoji']}!
		</p>
	</aside>
{/each}
