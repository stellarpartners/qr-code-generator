# QR Code Generator

A single-page, browser-only QR code designer. Style the dots, the corner
squares and the background, drop a logo in the middle, then export PNG, SVG
or PDF.

**Live app:** <https://qrcode.stellarpartners.gr/>

The whole thing is one `index.html`. There is no build step, no backend, and
no account. Nothing you type leaves your browser.

---

## Features

- **Nine collapsible sections** — content, templates, dot style, corner
  squares, corner dots, background, logo, border and margin, error correction.
- **Solid or gradient** colours for the dots, both corner types and the
  background. Gradients support linear and radial types, two colour stops, and
  a rotation slider for the dot gradient.
- **9 ready-made templates** across three groups: social, business and event.
- **12 built-in icons** (Facebook, Instagram, LinkedIn, X, YouTube, TikTok,
  WhatsApp, Snapchat, a globe, email, phone, location) plus upload of your own
  image.
- **Export to PNG (1024 / 2048 / 4096 px), SVG (vector) or PDF (A4).**
- **Background can be transparent** — useful for PNG and SVG overlays.
- **Undo and redo** with `Ctrl+Z` / `Ctrl+Y`, 50 steps deep.
- **Your work is remembered** in `localStorage`, so a reload does not lose it.
- **Clear all** resets everything back to defaults, behind a confirmation.

## Quick start

### Use the hosted version

Open <https://qrcode.stellarpartners.gr/>. Done.

### Run it locally

There is no build step. You do need a web server, because the app loads the
`icons/` and `shapes/` SVGs over HTTP:

```bash
git clone https://github.com/stellarpartners/qr-code-generator.git
cd qr-code-generator
python3 -m http.server 8000
# then open http://127.0.0.1:8000/
```

Any static server works — `npx serve`, `php -S`, nginx, whatever you have.

## How to use it

1. **Content** — type a URL or any text. The QR code updates as you type.
2. **Templates** — click one to get a finished look in a single click.
   Clicking a template keeps your text, logo, size and margin.
3. **Dot style / Corner squares / Corner dots** — pick a shape, then choose
   `Solid` or `Gradient` and set the colours.
4. **Background** — `Transparent`, `Solid` or `Gradient`.
5. **Logo / Image** — click a built-in icon, or upload your own file. Adjust
   the size and padding, and decide whether the dots behind the logo are
   hidden.
6. **Border & Margin** — the quiet zone around the code, in pixels.
7. **Error correction** — `L`, `M`, `Q` or `H`. Raise it when you add a logo.
8. **Export** — pick a size, then click `PNG`, `SVG` or `PDF`.

Press `Ctrl+Z` to undo and `Ctrl+Y` to redo. `Clear all` wipes the design and
the saved profile.

## Examples

### Example payloads

Anything you can type works. These are the common cases:

| What you want | Type this |
|---|---|
| Open a website | `https://stellarpartners.gr/` |
| Call a number | `tel:+302107000000` |
| Send an email | `mailto:hello@example.com` |
| Send a text message | `sms:+302107000000?body=Hello` |
| Open a map location | `geo:38.3686,21.4318` |
| Join a Wi-Fi network | `WIFI:T:WPA;S:MyNetwork;P:my-password;;` |
| Show a vCard | Paste a `BEGIN:VCARD` … `END:VCARD` block |
| Plain text | `Hello from Stellar Partners` |

Two rules of thumb:

- Shorter text makes a lower-density code, and a lower-density code scans from
  further away. Use a short link when you can.
- QR codes are read by cameras, so they need contrast. Dark dots on a light
  background is the safe choice. Light-on-dark works on modern phones, but not
  everywhere — test it before you print it.

### Styling example — a branded code for a business card

1. Type `https://example.com/your-name`.
2. Click the **Corporate** template.
3. In **Dot style**, switch to `Gradient`, then set colour 1 to `#1a2b4a` and
   colour 2 to `#0A66C2`, and drag rotation to `45`.
4. In **Background**, pick `Solid` and set `#f0f2f5`.
5. In **Logo / Image**, click the `Website` icon, set size to `30`, and leave
   *Hide dots behind the logo* ticked.
6. In **Error correction**, click `H`.
7. In **Border & Margin**, set the quiet zone to `20` for print.
8. Click `SVG` for printing, or `PNG` at 2048 px for the web.

### Example configuration

The app keeps its state in `localStorage` under the key `qrgen_config_v1`.
The `options` object is the option object of
[`qr-code-styling`](https://github.com/qr-code-styling/qr-code-styling), so you
can drive the library directly if you want to generate codes in bulk:

```html
<script src="https://unpkg.com/qr-code-styling@1.9.2/lib/qr-code-styling.js"></script>
<script>
  const qr = new QRCodeStyling({
    width: 1000,
    height: 1000,
    type: 'svg',
    data: 'https://stellarpartners.gr/',
    margin: 20,
    qrOptions: { errorCorrectionLevel: 'H' },
    image: 'icons/globe.svg',
    imageOptions: { hideBackgroundDots: true, imageSize: 0.4, margin: 4 },
    dotsOptions: {
      type: 'rounded',
      gradient: {
        type: 'linear',
        rotation: Math.PI / 4,
        colorStops: [
          { offset: 0, color: '#1a2b4a' },
          { offset: 1, color: '#0A66C2' }
        ]
      }
    },
    cornersSquareOptions: { type: 'extra-rounded', color: '#1a2b4a' },
    cornersDotOptions: { type: 'dot', color: '#0A66C2' },
    backgroundOptions: { color: '#f0f2f5' }
  });
  qr.append(document.getElementById('qr'));
  qr.download({ name: 'business-card', extension: 'svg' });
</script>
```

### Templates

| Group | Names |
|---|---|
| Social | Instagram, LinkedIn, WhatsApp |
| Business | Corporate, Minimal, Bold |
| Event | Neon, Soft, Gradient |

Templates set the dot, corner and background styles. They keep your text,
logo, dimensions and margin.

## Export formats

| Format | Size | Notes |
|---|---|---|
| PNG | 1024, 2048 (default) or 4096 px square | Raster. Choose it for images and social posts. |
| SVG | 1000 × 1000 viewBox, vector | Scales to any size. Choose it for print and for designers. |
| PDF | A4 portrait, code centred at 120 mm | Built from a raster render, then compressed. Choose it for a quick printable sheet. |

For the sharpest printed result, use **SVG** and place it in your own layout.
The PDF is the fast option, not the highest-quality one.

## Scanning tips

- Keep a margin (quiet zone) of at least 4 modules — the default of 10 px is
  fine for screen use, raise it for print.
- Keep the logo small. The app measures the logo it actually draws and shows
  the real width as a percentage of the code, because the library rounds the
  logo to whole QR modules.
- Use error correction `H` (30% recovery) whenever you add a logo or print
  small.
- Check the contrast. Light-on-dark codes work on modern phones but fail on
  older scanners.
- Always test the finished code with a real phone before you print 5,000 of
  them.

## Privacy

Everything runs in the browser. The app makes no network request except for
the two JavaScript libraries it loads from unpkg (pinned by version and
Subresource Integrity hash). Your text, links and uploaded logos never leave
your device. The saved profile lives in your browser's `localStorage` and
`Clear all` deletes it.

## Browser support

Verified in Chromium-based browsers (Chrome, Edge) on desktop and at a mobile
viewport (390 × 844). Firefox and Safari are **not** covered by the test matrix
yet.

The app uses `localStorage`, `canvas`, `FileReader` and CSS custom properties.
All four are long-standing standards, so current Firefox and Safari should work —
but treat that as an expectation, not a test result.

## Project structure

```
index.html      the entire application: markup, CSS and JavaScript
404.html        not-found page for the static host
favicon.svg     site icon
icons/          12 social and contact icons, used as QR centre logos
shapes/         11 shape preview icons for the style pickers
tools/          build-free helper scripts (see below)
```

### Helper scripts

| Script | What it does |
|---|---|
| `tools/measure-logo-size.html` | Opens a page that renders a logo at every slider value and prints the size the library actually draws. Run it after a library upgrade. |
| `tools/check-integrity.sh` | Recomputes the Subresource Integrity hashes for the two CDN libraries. Run it when you bump a library version. |

## Deployment

The site is a Cloudflare Pages project called `qrcodegenerator`, served at
<https://qrcode.stellarpartners.gr/>.

- **Build command:** none. The repository root *is* the published site.
- **Production branch:** `master`.
- Pages is connected to this GitHub repository, so **a push to `master` is the
  deploy**. Pushing any other branch creates a preview deployment.

Because the repository root is published, every file in it is reachable on the
live site — including this README and the LICENSE.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). In short: keep it a single file with no
build step, and test in a real browser before you open a pull request.

## Credits

Built by [Stellar Partners](https://stellarpartners.gr/).

The app stands on two open-source libraries:

| Library | Version | Licence | Used for |
|---|---|---|---|
| [qr-code-styling](https://github.com/qr-code-styling/qr-code-styling) | 1.9.2 | MIT | Rendering the styled QR code |
| [jsPDF](https://github.com/parallax/jsPDF) | 2.5.1 | MIT | Building the PDF export |

### Trademarks

The built-in icons in `icons/` are derived from
[Simple Icons](https://simpleicons.org/), which releases its icon set under
CC0-1.0. The marks themselves — Facebook, Instagram, LinkedIn, X, YouTube,
TikTok, WhatsApp, Snapchat — are trademarks of their respective owners. They
are used here to label the networks they represent. Their presence does not
imply any affiliation with, or endorsement by, those companies. If you reuse
one of these icons, you are responsible for complying with the owner's brand
guidelines.

## Licence

[MIT](LICENSE) © Stellar Partners
