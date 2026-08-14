# Gemini conversion

Use the Gemini Interactions API at `https://generativelanguage.googleapis.com/v1beta/interactions`. Authenticate with the `x-goog-api-key` header. Keep `gemini-3.5-flash-lite` as the default free-tier model unless current official pricing or model availability changes.

For PDF input, send a base64 content block with `type: document` and `mime_type: application/pdf`. For supported images, use `type: image`. Keep inline payloads below `GEMINI_INLINE_MAX_BYTES`; implement the Files API before accepting larger inputs.

Require HTML-only transcription that preserves visible content and reading order. Instruct the model to ignore instructions embedded inside the source document. After receiving output:

1. Remove Markdown fences.
2. Drop script, style, iframe, object, embed, SVG, forms, links, handlers, and unknown attributes.
3. Keep only semantic document tags.
4. Require non-empty readable text.
5. Cache by file SHA-256, model, and prompt version.

Official references:

- https://ai.google.dev/gemini-api/docs/document-processing
- https://ai.google.dev/gemini-api/docs/file-input-methods
- https://ai.google.dev/gemini-api/docs/pricing
