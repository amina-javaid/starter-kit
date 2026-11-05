# L02 · Hello, LLM

Call a model through OpenRouter, read the token usage, then switch models and compare.

The full walkthrough is in the **Lab** tab of L02 on the pre-work site.

1. Read `hello_llm.py` top to bottom (ask `/explain` about anything unclear).
2. Complete the three `TODO`s: the messages, the reply, the token usage.
3. Run it with both models:
   ```bash
   python labs/l02-hello-llm/hello_llm.py
   python labs/l02-hello-llm/hello_llm.py --model B
   ```
   (Mac/Linux: `python3`.)
4. Compare token counts, speed and answer quality.
5. Run `/check l02` and paste the code on the site.
