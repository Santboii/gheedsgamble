# Font Setup Instructions

## Diablo-Style Fonts

This project uses **Exocet** and **Optimus Princeps** fonts for an authentic Diablo aesthetic.

### Required Font Files

To use the custom fonts, you need to add the following font files to the `public/fonts/` directory:

```
public/fonts/
├── exocet.woff2
├── exocet.woff
├── optimus-princeps.woff2
└── optimus-princeps.woff
```

### Where to Get the Fonts

These are commercial/licensed fonts. You can obtain them from:

1. **Exocet** - Classic Diablo title font
   - Available from font foundries or licensed font sites
   
2. **Optimus Princeps** - Diablo UI font
   - Available from font foundries or licensed font sites

### Fallback Fonts

If the custom fonts are not available, the site will fall back to:
1. Cinzel (Google Font - similar medieval style)
2. System serif fonts

### Current Font Usage

- **Headings (h1, h2):** Exocet → Optimus Princeps → Cinzel → serif
- **Body text:** Optimus Princeps → Exocet → Cinzel → serif

The site will work without the custom fonts, but for the best Diablo experience, add the font files to the `public/fonts/` directory.
