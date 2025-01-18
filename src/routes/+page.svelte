<script lang="ts">
	import { onMount } from 'svelte';
	import { getData } from './services/emoji.service';
	import { SvelteMap } from 'svelte/reactivity';

	let emojis: string = '';
	let filteredEmojis: any = $state(undefined);
	let searchText: string = $state('');

	let toasts: any[] = $state([]);

	interface category {
		name: string
		subcategories: subcategory[]
	}

	interface subcategory {
		name: string
		emojis: emoji[]
	}

	interface emoji {
		name: string
		category: string
		subcategory: string
		emoji: string
		unicode: string
		description: string
	}

	onMount(async () => {
		let [resp, err] = await getData();
		if (err !== undefined) {
			console.log('TODO: popup a toast');
		} else {
			emojis = resp;
			let emojisObj = JSON.parse(emojis);
			let categories: any = [];
			
			Object.keys(emojisObj).forEach((category) => {
				
				let categoryList = [];
				Object.keys(emojisObj[category]).forEach((subcategory) => {
					let subcategoryList = [];
					Object.keys(emojisObj[category][subcategory]).forEach((emoji) => {
						let e = emojisObj[category][subcategory][emoji];
						if (!(e['name'] as string).includes(searchText)) {
							console.log('deleting ', e['name']);
							delete emojisObj[category][subcategory][emoji];
						}
					});
				});
			});

			filteredEmojis = JSON.parse(resp);
		}
	});

	$effect(() => {
		searchText;
		if (searchText.length <= 0 || emojis.length <= 0) {
			return;
		}

		console.log('search');
		let emojisObj = JSON.parse(emojis);
		Object.keys(emojisObj).forEach((category) => {
			Object.keys(emojisObj[category]).forEach((subcategory) => {
				Object.keys(emojisObj[category][subcategory]).forEach((emoji) => {
					let e = emojisObj[category][subcategory][emoji];
					if (!(e['name'] as string).includes(searchText)) {
						console.log('deleting ', e['name']);
						delete emojisObj[category][subcategory][emoji];
					}
				});
			});
		});

		filteredEmojis = filteredEmojis;
	});

	let idTimeouts: number[] = [];
	function copy(emoji: any) {
		navigator.clipboard.writeText(emoji['emoji']).then(
			() => {
				let id = crypto.randomUUID();
				toasts = [];
				idTimeouts.forEach((i) => {
					clearTimeout(i);
				});

				toasts.push(emoji);
				let idTimeout = setTimeout(() => {
					toasts = [];
				}, 2000);

				idTimeouts.push(idTimeout);
			},
			() => {
				// Failed to copy text
				console.error('Failed to copy text');
			}
		);
	}
</script>

<header class="sticky top-0 flex h-[48px] items-center justify-center bg-base-100 p-1">
	<div class="flex">
		<h1 class="text-center text-lg font-extrabold">
			😀 <span class="text-base-700">Git</span><span class="text-primary-600">Emojis</span> 😀
		</h1>
	</div>
</header>

<div class="flex h-full w-full justify-center">
	<div class="w-full max-w-2xl lg:max-w-5xl lg:text-2xl">
		<!--
  Heads up! 👋

  Plugins:
    - @tailwindcss/forms
-->

		<div class="relative pt-5">
			<label for="Search" class="sr-only"> Search </label>

			<input
				type="text"
				id="Search"
				placeholder="Search for..."
				class="w-full rounded-lg border-base-200 py-2.5 pe-10 pl-4 shadow-sm sm:text-sm"
				bind:value={searchText}
			/>

			<span class="absolute inset-y-0 end-0 grid w-10 place-content-center">
				<button type="button" class="text-base-700 hover:text-base-900">
					<span class="sr-only">Search</span>

					<svg
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="1.5"
						stroke="currentColor"
						class="size-4"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"
						/>
					</svg>
				</button>
			</span>
		</div>
		{#if filteredEmojis}
			{#each Object.keys(filteredEmojis) as category}
				<div class="mx-4 mt-10">
					<h1 class="font-bold capitalize">{category}</h1>
					{#each Object.keys(filteredEmojis[category]) as subcategory}
						<div class="py-4">
							<h2 class="capitalize">{subcategory.replaceAll('-', ' ')}</h2>
						</div>
						<div class="flex flex-wrap lg:text-3xl">
							{#each Object.keys(filteredEmojis[category][subcategory]) as emoji}
								<button
									onclick={() => {
										copy(filteredEmojis[category][subcategory][emoji]);
									}}
									ontouchstart={() => {
										copy(filteredEmojis[category][subcategory][emoji]);
									}}
									class="flex flex-wrap border p-4"
								>
									<span>
										{filteredEmojis[category][subcategory][emoji]['emoji']}
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

{#each toasts as t}
	<aside
		class=" fixed bottom-4 end-4 z-50 flex items-center justify-center gap-4 rounded-lg bg-base-900 px-5 py-3 text-base-200"
	>
		<p>
			Copied {t['name']}
			{t['emoji']}!
		</p>
	</aside>
{/each}
