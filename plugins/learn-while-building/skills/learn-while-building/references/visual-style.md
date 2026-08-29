# Visual style

The learning portal should feel like a calm notebook made for sustained reading.

## Palette

- warm paper: `#F6F1E8`
- light surface: `#FFFDF8`
- charcoal: `#26241F`
- muted olive: `#657054`
- terracotta: `#A45D3F`
- warm gray: `#746F66`
- soft rule: `#D8D0C3`

Do not use purple or blue gradients. Do not use neon glows, glass effects, glowing borders, or dark dashboard styling.

## Typography and layout

- Use a readable serif for titles and a restrained system sans serif for body text.
- Keep body text between 16 and 19 pixels with generous line height.
- Limit reading width to about 72 characters.
- Keep hierarchy visible through spacing and type, not a card around every section.
- Use one summary panel at most. Let detail sections sit directly on the page.
- Use buttons only for real actions.

## Copy

- Use natural section names such as `What changed`, `How to think about it`, and `Try it yourself`.
- Do not use emojis, decorative icon rows, synthetic praise, or motivational slogans.
- Do not use em dashes.
- Avoid phrases that imitate an AI dashboard, such as `AI insights`, `magic`, or `powered intelligence`.

## Motion

Motion must explain a sequence, relationship, or state change. Keep it slow enough to follow and provide pause or replay controls when repeated.

Honor `prefers-reduced-motion`. Every animation needs a static visual and text explanation. Three.js must load only after the user selects `Enable 3D view`. The lesson must remain complete if the library cannot load.

## Accessibility

- Meet WCAG AA contrast for text and controls.
- Keep keyboard focus clearly visible.
- Label figures, controls, quiz choices, and status messages.
- Do not encode meaning using color alone.
- Use responsive layouts that work at 360 pixels wide.
- Keep print output readable and remove interactive controls from print.
