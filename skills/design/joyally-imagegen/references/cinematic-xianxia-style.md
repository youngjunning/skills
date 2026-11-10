# Cinematic xianxia style

Use this preset when the user asks for a cinematic Chinese cultivation-fantasy look or uses `凡人修仙传风格` as the routing phrase. Treat the phrase as a visual shorthand, then write outbound prompts only with the original traits below.

## Visual grammar

- Premium cinematic 3D Chinese fantasy animation, realistic adult proportions, refined cloth, metal, stone, cloud and energy materials.
- Monumental mountain silhouettes, cloud seas, moonlit ancient cities or suspended terraces, deep atmospheric perspective and volumetric shafts of light.
- Deep indigo and blue-black base, moon silver, mist cyan, jade green energy and restrained antique-gold accents.
- Quiet, disciplined power: sparse lightning filaments, floating particles and luminous formations support the subject instead of filling the frame.
- Wide, layered compositions with a strong foreground, readable middle ground and immense distant world. Keep negative space where article copy or deterministic diagrams need it.
- No baked text, logos, signatures or interface chrome in model-generated layers.

## Franchise-free translation

Do not send franchise titles, creator names, existing character names, story-specific terms, logos or copied title treatments to an image model. Do not reproduce a supplied still's exact composition. Convert the request into the visual grammar above and create an original setting.

## Identity lock

When the user asks to preserve the supplied male protagonist, use `../assets/identity-references/kbase-xianxia-male-protagonist.png` as the locked identity asset. Preserve its face, hairstyle, blue-and-gold layered robe, jade-green sword, body proportions and pose.

For covers and structured diagrams, reserve a perimeter zone and composite this transparent PNG as an immutable raster layer. Generate only the environment behind it. Do not ask the model to redraw the character when exact continuity matters.

For a genuine pose, costume or expression edit, route through `image-edit.md`, attach the identity reference, describe only the requested change and inspect the face, hair, costume and sword before acceptance.

## Structured diagrams

Use the model only for a subdued, text-free atmospheric background. Render all titles, nodes, labels, arrows, badges and legends deterministically with HTML/CSS/SVG. Keep the locked protagonist outside the semantic graph's protected content area.

The final diagram must still pass the architecture validator and full-resolution raster review. Reject low-contrast copy, text over the face or sword, clipped energy effects, ambiguous edge direction and decorative marks that resemble connectors.

## Cover composition

Prefer a 16:9 frame. Place the locked protagonist on the right third with the jade sword directing the eye toward the left or center. Reserve the left half for atmosphere or optional deterministic typography. Use one distant moon or celestial light source, one architectural silhouette and restrained jade energy echoes to connect the character with the environment.
