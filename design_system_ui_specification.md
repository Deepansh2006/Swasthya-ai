# Design System & Aesthetic Specification (`design.md`)

## 1. Core Philosophy & Aesthetic Direction
**Aesthetic Archetype:** Atmospheric Translucent & Fluid Tactility  
**Visual Benchmark:** Raycast, Linear, visionOS, Arc Browser  

This design system rejects both rigid, flat corporate templates ("classic web") and oversaturated, glowing cyberpunk clichés ("flashy neon"). Instead, visual hierarchy is built through **layered translucency, subtle light refraction, 1px specular hairlines, and choreographed fluid motion**. 

Surfaces behave like smoked, matte-finished optical glass resting over a deep, low-contrast ambient canvas. Elements do not simply appear or disappear; they interpolate smoothly in space, opacity, and optical blur.

---

## 2. Color & Atmospheric Tokens

Colors are engineered to work with `backdrop-filter`. Solid opaque boxes are avoided for elevated UI; instead, surfaces use low-opacity fills paired with background blur and subtle inner highlights.

### 2.1 Dark Mode (Primary Canvas)
```css
:root {
  /* Base Canvas (Opaque underlayers) */
  --bg-canvas: #090A0F;           /* Deep obsidian slate, never pure #000000 */
  --bg-subtle: #0F111A;           /* Secondary recessed wells */

  /* Translucent Glass Surfaces */
  --surface-glass-1: rgba(255, 255, 255, 0.035); /* Base cards, sidebar */
  --surface-glass-2: rgba(255, 255, 255, 0.065); /* Hover states, elevated panels */
  --surface-glass-3: rgba(255, 255, 255, 0.10);  /* Active elements, floating modals */
  --surface-glass-dark: rgba(9, 10, 15, 0.68);   /* Sticky navbars, command palettes */

  /* Ambient Mesh Accents (Used at 6% - 12% opacity behind glass) */
  --ambient-indigo: rgba(110, 123, 242, 0.09);
  --ambient-teal: rgba(68, 189, 174, 0.07);
  --ambient-rose: rgba(224, 114, 148, 0.06);

  /* Specular Borders & Hairlines */
  --border-subtle: rgba(255, 255, 255, 0.07);
  --border-highlight: rgba(255, 255, 255, 0.15);
  --border-focus: rgba(124, 138, 255, 0.45);
  --inner-glow: inset 0 1px 0 0 rgba(255, 255, 255, 0.11);

  /* Typography Hierarchy (Luminance-based, never flat gray) */
  --text-primary: rgba(245, 247, 255, 0.94);
  --text-secondary: rgba(220, 226, 245, 0.62);
  --text-muted: rgba(200, 208, 235, 0.38);

  /* Accents (Muted, desaturated, atmospheric — NO NEON) */
  --accent-primary: #7C8AFF;      /* Soft Periwinkle Indigo */
  --accent-primary-muted: rgba(124, 138, 255, 0.16);
  --accent-secondary: #52C4B0;    /* Seafoam Sage */
  --status-success: #4CC38A;      /* Muted Jade */
  --status-warning: #E5A93B;      /* Warm Ochre */
  --status-danger: #E56B6F;       /* Soft Coral Crimson */
}
```

### 2.2 Light Mode (Frosted Alabaster Canvas)
```css
[data-theme="light"] {
  --bg-canvas: #F4F5F8;
  --bg-subtle: #EAECEF;

  --surface-glass-1: rgba(255, 255, 255, 0.55);
  --surface-glass-2: rgba(255, 255, 255, 0.75);
  --surface-glass-3: rgba(255, 255, 255, 0.90);
  --surface-glass-dark: rgba(244, 245, 248, 0.72);

  --border-subtle: rgba(15, 18, 28, 0.07);
  --border-highlight: rgba(15, 18, 28, 0.14);
  --inner-glow: inset 0 1px 0 0 rgba(255, 255, 255, 0.80);

  --text-primary: rgba(15, 18, 28, 0.92);
  --text-secondary: rgba(15, 18, 28, 0.60);
  --text-muted: rgba(15, 18, 28, 0.38);

  --accent-primary: #5463E8;
  --accent-primary-muted: rgba(84, 99, 232, 0.12);
}
```

---

## 3. Translucency & Material Rules

To make translucent surfaces feel rich rather than muddy or washed out, every glass container must follow three rules:

1. **Blur + Saturation Pairing:** Never use `backdrop-filter: blur()` alone. Combine it with `saturate()` so underlying ambient colors gently bloom through the frosted layer.
2. **Top-Edge Specular Catchlight:** Real glass catches light on its upper rim. Use `--inner-glow` (`inset 0 1px 0 0 rgba(255, 255, 255, 0.11)`) on cards, buttons, and modals.
3. **Ambient Underlay:** Place 1–2 large, slow-drifting radial gradients (`400px`–`700px` radius, `filter: blur(90px)`, opacity `< 0.10`) fixed to the background canvas so scrolling content subtly shifts in tint as it passes over them.

```css
/* Standard Translucent Material Recipe */
.glass-panel {
  background: var(--surface-glass-1);
  backdrop-filter: blur(16px) saturate(140%);
  -webkit-backdrop-filter: blur(16px) saturate(140%);
  border: 1px solid var(--border-subtle);
  box-shadow: 
    var(--inner-glow),
    0 12px 32px -8px rgba(0, 0, 0, 0.28);
}
```

---

## 4. Motion Architecture & Smooth Transitions

**Core Rule:** Never use `transition: all 0.3s ease`. Linear or default CSS easing feels mechanical. All motion must use expressive exponential ease-out curves or spring physics, animating only compositor-friendly properties (`transform`, `opacity`, `filter`, and explicit color tokens).

### 4.1 Easing & Timing Tokens
```css
:root {
  /* Easing Curves */
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);        /* Primary UI entrance & hover */
  --ease-out-quart: cubic-bezier(0.25, 1, 0.5, 1);       /* Smooth state interpolation */
  --ease-in-out-Quint: cubic-bezier(0.83, 0, 0.17, 1);   /* Layout & drawer shifts */
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);      /* Tactile micro-bounces (toggles, icons) */

  /* Duration Tiers */
  --duration-micro: 150ms;   /* Button hover, border brightening, text color shift */
  --duration-meso: 280ms;    /* Dropdowns, tooltips, tab pills, card elevation */
  --duration-macro: 480ms;   /* Modals, sidebars, page view transitions */
}
```

### 4.2 Signature Transition Patterns

* **The Blur-Dissolve Entrance (Modals, Popovers, Route Views):**
  Instead of sliding abruptly from off-screen or simply fading opacity, elements materialize by resolving their optical blur while rising slightly:
  * **Initial State:** `opacity: 0; transform: translateY(8px) scale(0.985); filter: blur(6px);`
  * **Active State:** `opacity: 1; transform: translateY(0) scale(1); filter: blur(0px);`
  * **Transition:** `all var(--duration-meso) var(--ease-out-expo)`
* **Shared-Layout Pill Indicators (Tabs & Navigation):**
  Active navigation states should not blink off and on. Use a single floating translucent pill (`background: var(--surface-glass-2); border: 1px solid var(--border-highlight)`) that glides horizontally/vertically between active items using `var(--ease-out-expo)` over `260ms`.
* **Tactile Press Compression:**
  Interactive buttons and cards compress subtly on `:active` (`transform: scale(0.98)`) over `100ms` and release back with `--ease-spring`.
* **Staggered Cascade:**
  When rendering lists or grid cards, stagger item entrances by `35ms` per item, capped at a maximum total delay of `280ms` so the interface never feels sluggish.

---

## 5. Typography & Scannability

Typography is clean, high-contrast in weight, and tightly tracked on display sizes to balance the airy, translucent containers.

* **UI Sans Stack:** `'Inter', 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif`
* **Monospace / Data Stack:** `'JetBrains Mono', 'Geist Mono', monospace` (always enable `font-variant-numeric: tabular-nums` for counters, prices, and timestamps).

| Role | Size | Line Height | Weight | Letter Spacing | Color Token |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Display / Hero** | `clamp(2rem, 3.5vw, 3rem)` | `1.12` | `600` | `-0.032em` | `--text-primary` |
| **Section Heading (H1/H2)** | `1.375rem` (`22px`) | `1.25` | `600` | `-0.022em` | `--text-primary` |
| **Card Title (H3)** | `1rem` (`16px`) | `1.4` | `500` | `-0.011em` | `--text-primary` |
| **Body Default** | `0.9375rem` (`15px`) | `1.6` | `400` | `-0.005em` | `--text-secondary` |
| **Metadata / Micro** | `0.75rem` (`12px`) | `1.4` | `500` | `+0.02em` | `--text-muted` |

---

## 6. Spatial Grid & Radii Scale

Nested rounded corners must be concentric. If an outer card has a padding of `12px` and an inner button has a radius of `10px`, the outer card radius should be $R_{\text{outer}} = R_{\text{inner}} + \text{Padding} = 22\text{px}$ (or snapped to the nearest token).

* `--radius-xs: 6px` (Badges, keyboard shortcuts, inline tags)
* `--radius-sm: 10px` (Buttons, text inputs, menu items)
* `--radius-md: 16px` (Standard glass cards, dropdown menus)
* `--radius-lg: 24px` (Modals, command palettes, primary layout containers)
* `--radius-full: 9999px` (Floating status pills, avatar rings)

**Layout Spacing:** Use generous breathing room. Minimum `20px`–`24px` internal padding on cards, and `16px`–`24px` gaps in bento/grid layouts so the background canvas remains visible between translucent panels.

---

## 7. Component-Level Specifications

### 7.1 Interactive Glass Cards
* **Default:** `background: var(--surface-glass-1)`, `border: 1px solid var(--border-subtle)`, `box-shadow: var(--inner-glow)`.
* **Hover:** Background shifts to `var(--surface-glass-2)`, border brightens to `var(--border-highlight)`, and card elevates `transform: translateY(-2px)` over `240ms var(--ease-out-expo)`.
* **Optional Cursor Spotlight:** On desktop, track mouse coordinates `(x, y)` relative to the card to render a subtle radial gradient (`radial-gradient(350px circle at var(--mouse-x) var(--mouse-y), rgba(255,255,255,0.06), transparent 60%)`) across the card surface and border.

### 7.2 Buttons
* **Primary Action:**
  * Soft atmospheric fill (`background: linear-gradient(180deg, rgba(124, 138, 255, 0.9) 0%, rgba(98, 112, 235, 0.9) 100%)`), `border: 1px solid rgba(255, 255, 255, 0.22)`, `box-shadow: inset 0 1px 0 rgba(255,255,255,0.25), 0 4px 14px rgba(124, 138, 255, 0.22)`.
  * Never use harsh neon outer glows.
* **Secondary / Ghost Glass:**
  * `background: var(--surface-glass-1)`, `border: 1px solid var(--border-subtle)`, `color: var(--text-primary)`.
  * Hover brightens background to `var(--surface-glass-2)` and border to `var(--border-highlight)`.

### 7.3 Inputs & Search Fields
* **Recessed Well:** Unlike cards (which sit above the canvas), inputs sit *slightly inside* the surface (`background: rgba(0, 0, 0, 0.22)` in dark mode, `border: 1px solid var(--border-subtle)`).
* **Focus Transition:** On `:focus-visible`, suppress default browser outlines. Transition `border-color` to `var(--border-focus)` and expand a soft halo: `box-shadow: 0 0 0 3px var(--accent-primary-muted)` over `180ms var(--ease-out-expo)`.

### 7.4 Floating Navigation / Command Bar
* Position detached from viewport edges (`top: 16px` or `bottom: 24px`) with `--radius-lg` or `--radius-full`.
* Use `--surface-glass-dark` with `backdrop-filter: blur(20px) saturate(160%)` so content scrolling underneath blurs cleanly into an atmospheric smudge without hurting legibility.

---

## 8. Strict Anti-Patterns (What to Avoid)

1. **No Neon / Cyberpunk Glows:** Never use `box-shadow: 0 0 20px #00ffff` or saturated `#FF00FF` / `#00FF00` accents. All color accents must have controlled saturation (`< 75%` HSL saturation) and blend into the glass.
2. **No Opaque Gray Boxes on Dark Mode:** Avoid solid `#1E1E1E` or `#2A2A2A` cards. Even subtle `4%` white translucency with a `1px` `8%` white border feels infinitely more refined.
3. **No Jarring Unmounts:** Dropdowns, modals, toasts, and tab panels must animate *out* (fade + slight scale down `0.98` + `blur(4px)` over `160ms`) before being removed from the DOM.
4. **No Heavy Drop Shadows:** Never use dark, muddy shadows on light mode or thick black shadows on dark mode. Rely on `1px` border contrast and surface luminance to separate layers.
5. **No Accessibility Neglect:** Always include a `@media (prefers-reduced-motion: reduce)` fallback that disables spatial `translate`/`scale` and instant-swaps opacity over `100ms`.