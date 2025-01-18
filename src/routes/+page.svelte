<script lang="ts">
	import { onMount } from 'svelte';
	import { getData } from './services/emoji.service';
	import { SvelteMap } from 'svelte/reactivity';

	let emojis: string = '';
	let filteredEmojis: category[] = $state([]);
	let searchText: string = $state('');

	let toasts: any[] = $state([]);
	interface category {
		name: string;
		subcategories: subcategory[];
	}

	interface subcategory {
		name: string;
		emojis: emoji[];
	}

	interface emoji {
		name: string;
		category: string;
		subcategory: string;
		emoji: string;
		unicode: string;
		description: string;
	}

	onMount(async () => {
		let [resp, err] = await getData();
		if (err !== undefined) {
			console.log('TODO: popup a toast');
		} else {
			emojis = resp;
			filterEmojis();
		}
	});

	$effect(() => {
		searchText;
		filterEmojis();
	});

	function filterEmojis() {
		if (emojis.length <= 0) {
			return;
		}

		let emojisObj = JSON.parse(emojis);
		let categories: category[] = [];
		Object.keys(emojisObj).forEach((c) => {
			let category: category = {
				name: c,
				subcategories: []
			};
			Object.keys(emojisObj[c]).forEach((s) => {
				let subcategory: subcategory = {
					name: s,
					emojis: []
				};

				Object.keys(emojisObj[c][s]).forEach((e) => {
					let emoji = emojisObj[c][s][e] as emoji;
					if (emoji.name.includes(searchText)) {
						subcategory.emojis.push(emoji);
					}
				});
				if (subcategory.emojis.length > 0) {
					category.subcategories.push(subcategory);
				}
			});
			if (category.subcategories.length > 0) {
				categories.push(category);
			}
		});

		filteredEmojis = categories;
	}

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

<header class="sticky top-0 flex h-[90px] items-center justify-center bg-base-100 p-1">
	<div class="flex flex-col">
		<h1 class="text-center text-lg font-extrabold pt-10">
			😀 <span class="text-base-700">Git</span><span class="text-primary-600">Emojis</span> 😀
		</h1>

		<div class="relative m-2 pt-5 ">
			<label for="Search" class="sr-only"> Search </label>

			<input
				type="text"
				id="Search"
				placeholder="Search for..."
				class="w-full rounded-lg shadow-lg py-2.5 pe-10 ps-4 focus:scale-110 sm:text-sm border-primary-500 focus:outline-primary-500 border"
				bind:value={searchText}
			/>

			<span class="absolute inset-y-0 end-0 grid w-10 place-content-center pt-4">
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
	</div>
</header>

<div class="flex h-full w-full justify-center">
	<div class="w-full max-w-2xl lg:max-w-xl lg:text-2xl">
		{#if filteredEmojis}
			{#each filteredEmojis as category}
				{#if category.subcategories.length > 0}
					<div class="mx-4 mt-10">
						<h1 class="font-bold capitalize">{category.name}</h1>
						{#each category.subcategories as subcategory}
							{#if subcategory.emojis.length > 0}
								<div class="py-4">
									<h2 class="capitalize">{subcategory.name.replaceAll('-', ' ')}</h2>
								</div>
								<div class="flex flex-wrap lg:text-3xl">
									{#each subcategory.emojis as emoji}
										<button
											onclick={() => {
												copy(emoji);
											}}
											ontouchstart={() => {
												copy(emoji);
											}}
											class="flex flex-wrap border p-4"
										>
											<span class="lg:2xl text-3xl">
												{emoji.emoji}
											</span>
										</button>
									{/each}
								</div>
							{/if}
						{/each}
					</div>
				{/if}
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
