# 😀 GitEmojis 😀

GitEmojis is a web app that showcases all GitHub emojis, organized by category and subcategory. It allows users to quickly browse, copy, and access emojis with ease. Whether you're a developer looking to add some fun to your commits or someone who wants to integrate GitHub emojis into your project, GitEmojis is here to help!

## Features:
- **Emoji Browser**: Browse GitHub emojis organized by category and subcategory.
- **Copy to Clipboard**: Click on an emoji to easily copy it to your clipboard.
- **REST API**: Access emojis via a simple REST endpoint: `https://gitemojis.com/{emoji_name}`. Retrieve emojis using `curl` or `wget` for integration into your own projects.
- **JSON Export**: Grab a copy of the JSON file containing all the emojis by calling [https://gitemojis.com/emojis.json](https://gitemojis.com/emojis.json).

  
## Upcoming Features:
- **Search Functionality**: Search the emoji list by name or category to find the perfect emoji quickly.
- **API Documentation**: Detailed API docs with examples to help you integrate GitEmojis into your projects.
- **Favorites**: Save your favorite emojis for quick access.

## Developing

Once you've installed dependencies with `npm install` (or `pnpm install` or `yarn`), start a development server:

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

## Building

To create a production version of your app:

```bash
npm run build
```

You can preview the production build with `npm run preview`.

> To deploy your app, you may need to install an [adapter](https://svelte.dev/docs/kit/adapters) for your target environment.
