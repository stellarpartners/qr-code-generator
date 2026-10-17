# Contributing

Thanks for looking. This is a small tool and it should stay small.

## Ground rules

- **Keep it one file.** All markup, CSS and JavaScript live in `index.html`.
  Do not add a build step, a bundler, a framework or a dependency manager.
- **No backend.** No server code, no API keys, no database. Everything runs in
  the browser.
- **No new runtime dependencies** without a good reason. Say why in the pull
  request. If you add one, pin the version and add its Subresource Integrity
  hash (run `python3 tools/check-integrity.py --verify`).
- **Keep it in English.** The interface and the documentation are English.

## Before you open a pull request

Run the two checks CI runs first — they catch a stale integrity hash and a
broken inline script before the deploy does:

```bash
python3 tools/check-html.py
python3 tools/check-integrity.py --verify
```

Then:

1. Serve the folder and open it in a real browser:

   ```bash
   python3 -m http.server 8000
   ```

2. Check that the code still renders and that the browser console is clean.
3. Scan the result with a real phone. A styled QR code that no scanner can read
   is not a working feature.
4. Test at a narrow width (about 390 px) as well as on desktop.
5. If you changed the logo sizing, run `tools/measure-logo-size.html` and say
   what changed.

## Style

- Match the existing code: two-space indentation, `const` and `let`, plain
  functions, comments that explain *why* rather than *what*.
- Write commit messages in the imperative mood: `Fix gradient reset on clear`.
- Keep the diff focused. One concern per pull request.

## Reporting a problem

Open an issue and include:

- what you did,
- what you expected,
- what happened,
- your browser and version,
- the text you encoded, if the problem is with the output.

## Licence

By contributing you agree that your work is released under the
[MIT licence](LICENSE).
