# Eye Gaze and Direct-Eye-Contact Edits

Read this reference when the user asks to move an iris or pupil, correct an upward or sideways gaze, make a mascot look at the viewer, or refine eye contact while preserving an existing character.

## Anatomy contract

Name the requested part before editing:

| Visual region | Term | Edit consequence |
|---|---|---|
| White eye area | sclera / 眼白 / 巩膜 | Defines the visible eye opening; do not move it for a gaze-only edit. |
| Colored ring or colored eye interior | iris / 虹膜 | Sets eye color and part of the gaze construction; moving the whole iris changes more than the black center. |
| Black central area | pupil / 瞳孔 | Primary dark gaze indicator. “黑色区域往下” means move the pupil, not the iris. |
| White dots on the pupil | catchlights / 高光 / 反光 | Reflections, not gaze indicators. They normally travel with the pupil while preserving their size and relative position. |

If the user says `黑色区域`, resolve it as the pupil unless the supplied image proves otherwise. If terminology remains ambiguous and the edit would materially differ, identify the regions in plain language before spending an API call.

## Gaze geometry

Judge gaze from the dark pupil body inside each colored iris. A front-facing head, symmetrical eye outlines, or matching white catchlights do not prove direct eye contact.

For a camera-facing gaze:

1. Keep the head facing the camera independently from the eye instruction.
2. Keep each iris fixed unless the user explicitly asks to move the iris.
3. Place each dark pupil body near the horizontal and vertical center of its iris.
4. Require balanced visible iris clearance above and below each pupil.
5. Require matching normalized pupil positions in both eyes and visual axes that converge on the camera.
6. Reject pupils visibly in the upper, lower, left, or right third of the iris, mismatched eye directions, looking past the viewer, or a result inferred only from catchlights.

When measurable, record normalized centers relative to the visible iris bounds:

```text
u = (pupil_center_x - iris_left) / iris_width
v = (pupil_center_y - iris_top) / iris_height
```

Direct gaze should visually approach `(0.5, 0.5)` in both eyes. Do not turn this into a rigid numeric threshold when stylized eyelids occlude the iris; 4× visual inspection remains the release gate.

## Pupil-only edit workflow

Treat the supplied image as both the edit target and the identity reference.

1. Preserve the approved asset. Generate an uninstalled candidate first.
2. Use the image-edit endpoint with a single allowed change: move both black pupil bodies by the same small amount. Keep iris boundaries, sclera, eyelids, eye outlines, face, pose, palette, material, lighting, framing, alpha, and composition fixed.
3. Move existing catchlights together with their pupils. Preserve catchlight size, shape, brightness, and relative location within each pupil.
4. Inspect the whole candidate for identity drift, then inspect both eyes at 4× or greater. Also inspect intended icon sizes such as 64 px, 32 px, and 16 px when the asset is a logo or avatar.
5. Reject whole-image replacement if the model changes body proportions, silhouette, eye construction, iris size, facial features, crop, transparency, or styling—even if its gaze is correct.
6. Do not overwrite the approved asset until identity, gaze, transparency, and intended-size gates pass.

Use this prompt core and append the asset-specific invariants:

```text
Change only the two black pupil bodies inside the existing colored irises. Move each
complete black pupil body, together with its existing white catchlights, slightly
downward by the same small amount. Keep both irises completely fixed and unchanged.
Keep pupil size, shape, color, and horizontal position unchanged. Place each dark
pupil mass at the horizontal and vertical center of its iris, with balanced colored
iris clearance above and below. Both visual axes converge on the camera lens. White
catchlights are reflections and do not define gaze. No upward gaze, downward gaze,
side glance, eye roll, looking past the viewer, or off-camera focus.
```

Avoid fixed pixel amounts in the API prompt unless the input and output resolution are guaranteed. Prefer a small percentage of visible iris height and inspect the actual result.

## Locked-raster recovery when the model drifts

The current edit endpoint can return correct pupils while redrawing the rest of the character. Do not install that full result.

A locked-raster composite is acceptable only when all of the following are true:

1. The candidate pupil geometry came from an actual image-edit result, not from locally translating a generic ellipse or copied pupil patch.
2. The approved source remains the immutable base.
3. The allowed regions are tight masks around the old and new pupil bodies, their catchlights, and only the narrow iris area required to fill pixels vacated by the pupil.
4. Iris boundaries, sclera, eyelids, eye outlines, face, and every pixel outside those regions stay on the approved base.
5. The composite records zero changed pixels outside the allowed regions before installation.
6. The final PNG retains the source alpha behavior and, for compact indexed logos, preferably the original palette outside changed pixels.

Moving a pupil necessarily reveals iris where the pupil used to be. That narrow iris reconstruction is part of a pupil-only edit; moving the entire iris is not. Never describe a whole-iris replacement as a pupil-only change.

Do not locally translate a flattened circular or elliptical pupil patch. It duplicates or erases antialiased eyelids, sclera, iris texture, muzzle, fur, or feathers and can create halos and seams. Do not move catchlights alone; that changes reflected light, not gaze.

## QA and metadata

Before accepting:

1. Compare approved source and final result at full resolution.
2. Crop both eyes and inspect at 4× or greater, judging the dark pupil bodies separately from catchlights.
3. Verify both pupils have matching normalized positions and the intended camera-facing gaze.
4. Verify no seam, double pupil, damaged iris boundary, overwritten eyelid, or asymmetric eye construction.
5. Verify transparency and target file-size budgets.
6. Verify changed pixels outside the declared pupil regions equal zero for a locked-raster composite.

Metadata should record the edit target, identity reference or source hash, model, requested and actual resolution, generation time, prompt, allowed pupil regions, changed-pixel count, changed pixels outside allowed regions, identity QA, gaze QA, transparency QA, and whether the installed result is a full model output or a locked-raster composite.

If no candidate passes both identity and gaze gates, preserve the approved source, report the failed geometry or drift, and stop. A successful API response is not an accepted eye edit.
