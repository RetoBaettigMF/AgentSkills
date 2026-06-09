# AI-Readable Publishing

When publishing content that should be consumable by AI tools (brand assets, style guides, API docs), always include machine-readable formats alongside the HTML.

## Pattern

For any published resource, provide three formats:

| File | Purpose |
|------|---------|
| `index.html` | Human-friendly page with visuals, dark/light toggle, download links |
| `brand.json` | Structured JSON data — full spec, linkable by AI tools |
| `brand.txt` | Plain text — copy-pasteable into prompts, minimum token overhead |

## JSON Structure

Include all relevant structured data (colors with hex/rgb/cmyk, typography with CSS snippets, asset URLs with base path). The JSON should be self-contained so an AI can reconstruct the brand without scraping HTML.

Example (`brand.json`):
```json
{
  "brand": "Example",
  "url": "https://example.com",
  "colors": {
    "primary": { "hex": "#0000FF", "rgb": "0,0,255", "usage": "Logo, highlights" }
  },
  "typography": {
    "corporate_font": "FontName",
    "css": "font-family: \"FontName\", sans-serif;",
    "weights": { "bold": { "weight": 700, "usage": "Headlines" } }
  },
  "logos": {
    "base_url": "https://baettig.org/morticia/example",
    "variants": [
      { "name": "Logo Dark", "png": "logo-dark.png", "svg": "logo-dark.svg" }
    ]
  }
}
```

## Plain Text Template

```text
BRAND NAME Guidelines
Source: <source-url>
Logo assets: <base-url>

COLORS
------
Primary: HEX #xxx, RGB x,x,x, CMYK x,x,x,x — Usage: ...

TYPOGRAPHY
----------
Corporate Font: FontName
  CSS: font-family: "FontName", sans-serif;
  Bold (weight 700): Headlines
  Regular (weight 400): Body text
```

## Prompt Tip

Include this hint on the HTML page so users know how to use it:

> Verwende die Brand Guidelines von https://baettig.org/morticia/example/brand.json und gestalte…
