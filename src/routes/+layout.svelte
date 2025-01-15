<script lang="ts">
	import '../app.css';
	let { children } = $props();
</script>

<div class="flex h-full w-full justify-center">
	<div class="flex-row flex-1 w-100">
		{@render children()}
	</div>
</div>
