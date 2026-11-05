---
name: explain
description: Explain an FDE / LLM / agent / Claude Code concept, or a piece of lab code, in plain language with a pointer to the book and the pre-work level that teaches it. Use when the student types /explain <term or question>.
argument-hint: <term or question>
---

# /explain <term or question>

The student asked about: `$ARGUMENTS`

1. Look the term up in `glossary.md`. Use its definition, level and book section as your anchor, so your explanation matches the site and the book.

2. Answer in this shape, short:
   - **One-line definition** in plain English.
   - **An analogy or concrete example**, ideally from the labs (Parcelly's `lookup_order`, the OpenRouter call) or from FDE work with a client.
   - **Why it matters in the bootcamp**: one sentence.
   - **Read more:** the book section and the pre-work level, e.g. "Book §3.2 · L03".

3. If it's about **lab code** (e.g. "what does hello_llm.py send?"), walk through the relevant lines. For the L02/L03 TODOs, explain what the code around them does and what the TODO needs to achieve, but don't write the TODO code (see CLAUDE.md).

4. If the term isn't in the glossary, answer anyway in the same shape, and say it's outside the pre-work path if it is.

5. End with one quick question that checks understanding, e.g. "So if the model asks for `lookup_order`, who actually runs it?"
