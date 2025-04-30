# ollama

This app wraps the excellent work of [Ollama](https://github.com/ollama/ollama), providing a simple and consistent LLM server interface for use within Make87 systems.

It exposes a local Ollama instance to other apps as a shared LLM provider, with optional extensions for text message exchange and image input. Ideal for chat-based agents, vision + language pipelines, or any tool requiring LLM access.

## What it provides

- 🔁 A wrapper around [Ollama](https://ollama.com) to serve models like `llama3`, `mistral`, `gemma`, and others over HTTP. You can define to model to use in the config.
- 💬 A lightweight provider for sending and receiving text prompts.
- 🖼️ Optional provider for image to text.

This app is part of the **Make87** ecosystem and is intended to be deployed and managed by the platform. No manual configuration is necessary.

## Attribution

This project builds on the amazing work done by the [Ollama team](https://github.com/ollama/ollama). We do not modify their binaries or re-implement model serving—this is simply a wrapper for integration.
