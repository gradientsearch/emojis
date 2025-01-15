<script lang="ts">
	import { onMount } from 'svelte';
	import { getData } from './services/emoji.service';

	let emojis: any = $state(undefined);
	onMount(async () => {
		let [resp, err] = await getData();
		if (err !== undefined) {
			console.log('TODO: popup a toast');
		} else {
			emojis = JSON.parse(resp);
		}
	});
</script>

<header class="bg-base-100 sticky top-0 flex h-[48px] items-center justify-center p-1">
	<div class="flex">
		<h1 class="text-center text-lg font-extrabold">
			😀 <span class="text-base-700">Git</span><span class="text-primary-600">Emojis</span> 😀
		</h1>
	</div>
</header>

<div class="flex h-full w-full justify-center">
	<div class="w-full max-w-2xl lg:max-w-5xl">
		{#if emojis}
        {#each Object.keys(emojis) as category}
            <div>
                <h1 class="font-bold">{category}</h1>
                {#each Object.keys(emojis[category]) as subcategory}
                <h2> {subcategory}</h2>
                {/each}
            </div>
            {/each}
			{JSON.stringify(emojis)}
		{/if}
	</div>
</div>
