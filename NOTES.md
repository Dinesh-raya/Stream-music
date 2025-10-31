NOTES - Reversions, logical errors considered, and fixes applied
================================================================

What "Reverse each and every thing" means in this deliverable:
- I interpreted your request as wanting a clean, corrected, and stable project that undoes
  the earlier broken/incomplete attempts and returns the codebase to a consistent, working state.
- The produced project restores the intended features (search, inline audio playback, HLS support,
  playlist) while removing the prior syntax/formatting mistakes that caused errors during generation.

Logical errors that were encountered (and WHY they occurred):
1) Syntax errors when embedding multi-line HTML/JS inside Python triple-quoted strings
   - Cause: Unescaped braces or nested triple quotes and improper raw-string usage led to Python parsing errors.
   - Fix: Use safe string construction with % formatting and small concatenated strings to avoid accidental brace parsing.

2) Indentation/Unexpected indent errors
   - Cause: Mixing indentation levels and copy-pasting multi-line strings sometimes added stray indents.
   - Fix: The final app.py was written programmatically with a consistent dedented block (textwrap.dedent) to ensure proper Python indentation.

3) Using f-strings with JavaScript blocks containing braces {}
   - Cause: f-strings treat braces as expression delimiters. JS uses braces heavily, causing collisions.
   - Fix: Avoid f-strings for HTML/JS blocks; use % formatting or string concatenation instead.

4) HLS playback support incompatibility
   - Cause: Streamlit's st.audio doesn't support HLS. Browsers require hls.js or native HLS support.
   - Fix: Inject hls.js player HTML only when the URL ends with .m3u8. This is a robust, commonly used approach.

5) Edge cases for API responses (None, unexpected formats)
   - Cause: The Music API can sometimes return unexpected shapes or non-200 statuses.
   - Fix: Added defensive checks (type and key existence) and user-friendly error messages.

Testing and guarantees:
- This project was programmatically generated and packaged. It follows best-effort defensive coding.
- Runtime behavior depends on the external Music API availability and your browser's HLS support.
- I cannot execute the Streamlit app inside this environment for you, but the code is structured to run locally.

Files included:
- app.py (main Streamlit app)
- requirements.txt
- README.md (instructions)
- NOTES.md (this file)
