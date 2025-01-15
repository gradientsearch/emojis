export async function getData(): Promise<[string, Error | undefined]> {
	const url = 'https://unicode.org/emoji/charts/full-emoji-list.txt';
	try {
		const response = await fetch(url);
		if (!response.ok) {
			return ['', Error(`Response status: ${response.status}`)];
		}

		const text = await response.text();
		return [text, undefined];
	} catch (error: any) {
		return ['', Error(`${error}`)];
	}
}
