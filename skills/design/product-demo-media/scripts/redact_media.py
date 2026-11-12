#!/usr/bin/env python3
"""Apply reviewed, deterministic masks to a screenshot or silent demo recording."""

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys


IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
VIDEO_SUFFIXES = {".mp4", ".mov", ".m4v"}


def dimensions(path: Path, video: bool) -> tuple[int, int, float | None]:
    if not video:
        try:
            from PIL import Image
        except ImportError as error:
            raise ValueError("Pillow is required for screenshots: python3 -m pip install Pillow") from error
        with Image.open(path) as image:
            return image.width, image.height, None
    if not shutil.which("ffprobe") or not shutil.which("ffmpeg"):
        raise ValueError("FFmpeg and FFprobe are required for recordings")
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "stream=width,height:format=duration",
         "-of", "json", str(path)],
        check=True, capture_output=True, text=True,
    )
    probe = json.loads(result.stdout)
    stream = next((row for row in probe.get("streams", []) if row.get("width") and row.get("height")), None)
    if not stream:
        raise ValueError("Recording has no video stream")
    duration = float(probe.get("format", {}).get("duration", 0))
    return int(stream["width"]), int(stream["height"]), duration or None


def load_regions(path: Path, width: int, height: int, duration: float | None, video: bool) -> list[dict]:
    data = json.loads(path.read_text())
    if "width" in data and data["width"] != width or "height" in data and data["height"] != height:
        raise ValueError("Mask manifest dimensions do not match the source")
    regions = data.get("regions")
    if not isinstance(regions, list) or not regions:
        raise ValueError("Mask manifest must contain at least one region")
    validated = []
    for index, region in enumerate(regions):
        if not isinstance(region, dict):
            raise ValueError(f"Region {index} must be an object")
        try:
            x, y, w, h = (region[key] for key in ("x", "y", "width", "height"))
        except KeyError as error:
            raise ValueError(f"Region {index} is missing {error}") from error
        if any(type(value) is not int for value in (x, y, w, h)) or x < 0 or y < 0 or w < 1 or h < 1:
            raise ValueError(f"Region {index} has invalid pixel coordinates")
        if x + w > width or y + h > height:
            raise ValueError(f"Region {index} exceeds {width}x{height} bounds")
        mode = region.get("mode", "solid")
        if mode not in {"solid", "mosaic"}:
            raise ValueError(f"Region {index} has invalid mode")
        start, end = region.get("start", 0), region.get("end", duration)
        if video:
            if not isinstance(start, (int, float)) or start < 0:
                raise ValueError(f"Region {index} has invalid start time")
            if end is not None and (not isinstance(end, (int, float)) or end <= start or duration and end > duration + 0.1):
                raise ValueError(f"Region {index} has invalid end time")
        elif "start" in region or "end" in region:
            raise ValueError(f"Region {index} has times on a still image")
        validated.append({"x": x, "y": y, "width": w, "height": h, "mode": mode,
                          "start": float(start), "end": float(end) if end is not None else None})
    return validated


def redact_image(source: Path, output: Path, regions: list[dict]) -> None:
    from PIL import Image, ImageDraw

    with Image.open(source) as opened:
        image = opened.convert("RGB")
    for region in regions:
        x, y, w, h = (region[key] for key in ("x", "y", "width", "height"))
        if region["mode"] == "solid":
            ImageDraw.Draw(image).rectangle((x, y, x + w - 1, y + h - 1), fill=(0, 0, 0))
        else:
            crop = image.crop((x, y, x + w, y + h))
            small = crop.resize((max(1, w // 16), max(1, h // 16)), Image.Resampling.BOX)
            image.paste(small.resize((w, h), Image.Resampling.NEAREST), (x, y))
    image.save(output)


def redact_video(source: Path, output: Path, regions: list[dict]) -> None:
    filters = []
    current = "0:v"
    for index, region in enumerate(regions):
        x, y, w, h = (region[key] for key in ("x", "y", "width", "height"))
        end = region["end"]
        condition = f"between(t,{region['start']},{end})" if end is not None else f"gte(t,{region['start']})"
        next_label = f"v{index}"
        if region["mode"] == "solid":
            filters.append(
                f"[{current}]drawbox=x={x}:y={y}:w={w}:h={h}:color=black:t=fill:"
                f"enable='{condition}'[{next_label}]"
            )
        else:
            base, sample, pixel = f"b{index}", f"s{index}", f"p{index}"
            filters.append(f"[{current}]split=2[{base}][{sample}]")
            filters.append(
                f"[{sample}]crop={w}:{h}:{x}:{y},scale={max(1, w // 16)}:{max(1, h // 16)},"
                f"scale={w}:{h}:flags=neighbor[{pixel}]"
            )
            filters.append(
                f"[{base}][{pixel}]overlay=x={x}:y={y}:enable='{condition}'[{next_label}]"
            )
        current = next_label
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin", "-i", str(source),
         "-filter_complex", ";".join(filters), "-map", f"[{current}]", "-an",
         "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
         "-movflags", "+faststart", "-map_metadata", "-1", "-map_chapters", "-1",
         str(output)],
        check=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--masks", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.expanduser().resolve()
    created = False
    try:
        source, manifest = (path.expanduser().resolve() for path in
                            (args.input, args.masks))
        if not source.is_file() or not manifest.is_file():
            raise ValueError("Input and mask manifest must be readable files")
        if source == output or output.exists():
            raise ValueError("Output must be a new path distinct from the input")
        video = source.suffix.lower() in VIDEO_SUFFIXES
        if not video and source.suffix.lower() not in IMAGE_SUFFIXES:
            raise ValueError("Supported input: PNG, JPEG, WebP, MP4, MOV, M4V")
        if video and output.suffix.lower() != ".mp4":
            raise ValueError("Video output must be MP4")
        if not video and output.suffix.lower() not in IMAGE_SUFFIXES:
            raise ValueError("Image output must be PNG, JPEG, or WebP")
        width, height, duration = dimensions(source, video)
        regions = load_regions(manifest, width, height, duration, video)
        output.parent.mkdir(parents=True, exist_ok=True)
        created = True
        if video:
            redact_video(source, output, regions)
        else:
            redact_image(source, output, regions)
        print(json.dumps({"output": str(output), "width": width, "height": height,
                          "regions": len(regions), "audio": "removed" if video else None,
                          "reviewed": False}))
        return 0
    except (ValueError, OSError, subprocess.CalledProcessError, json.JSONDecodeError) as error:
        if created and output.exists():
            output.unlink()
        print(f"redaction failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
