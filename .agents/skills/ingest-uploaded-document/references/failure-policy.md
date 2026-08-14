# Failure policy

- Reject extension/signature mismatches before parsing.
- Reject encrypted PDFs and generic archives.
- Return a configuration error when Gemini is required but `GEMINI_API_KEY` is absent.
- Retry only HTTP 429 and transient 5xx responses. Do not retry authentication, validation, or unsupported-format errors.
- Require LibreOffice when an Office document needs visual fallback. Do not send raw Office bytes to the PDF/document input contract.
- Delete the saved upload when preparation fails.
- Keep a valid cached HTML artifact; regenerate it only when the source hash, model, or prompt version changes.
- Append embeddings and metadata atomically only after chunks are complete.
- Avoid logging document bodies, base64 payloads, model responses, or API keys.
