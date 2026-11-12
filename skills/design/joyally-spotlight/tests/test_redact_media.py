import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from PIL import Image


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "redact_media.py"
spec = importlib.util.spec_from_file_location("redact_media", SCRIPT)
redact = importlib.util.module_from_spec(spec)
spec.loader.exec_module(redact)


class RedactMediaTest(unittest.TestCase):
    def test_image_cover_replaces_secret_pixels_and_strips_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, output, other_source, other_output, manifest = (
                root / name for name in ("source.png", "out.png", "other.png", "other-out.png", "masks.json")
            )
            for path, secret_color in ((source, (5, 10, 20, 255)), (other_source, (200, 100, 50, 255))):
                image = Image.new("RGBA", (80, 40), (255, 255, 255, 255))
                for x in range(10, 30):
                    for y in range(5, 17):
                        image.putpixel((x, y), secret_color)
                image.save(path)
            manifest.write_text(json.dumps({"width": 80, "height": 40, "regions": [
                {"x": 10, "y": 5, "width": 20, "height": 12, "mode": "solid", "color": "#E9EDF1"}
            ]}))
            regions = redact.load_regions(manifest, 80, 40, None, False)
            redact.redact_image(source, output, regions)
            redact.redact_image(other_source, other_output, regions)
            with Image.open(output) as result:
                self.assertEqual(result.mode, "RGB")
                self.assertEqual(result.info, {})
                self.assertEqual(result.getpixel((10, 5)), (233, 237, 241))
                self.assertEqual(result.getpixel((29, 16)), (233, 237, 241))
                self.assertEqual(result.getpixel((30, 16)), (255, 255, 255))
            self.assertEqual(output.read_bytes(), other_output.read_bytes())
            with self.assertRaisesRegex(ValueError, "dimensions"):
                redact.load_regions(manifest, 81, 40, None, False)

    def test_rejects_reconstructable_or_transparent_cover(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "masks.json"
            for region in (
                {"x": 1, "y": 1, "width": 10, "height": 10, "mode": "mosaic"},
                {"x": 1, "y": 1, "width": 10, "height": 10, "color": "#E9EDF180"},
            ):
                manifest.write_text(json.dumps({"regions": [region]}))
                with self.assertRaisesRegex(ValueError, "opaque"):
                    redact.load_regions(manifest, 80, 40, None, False)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg unavailable")
    def test_video_masks_full_clip_and_removes_audio(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, output, frame = (root / name for name in ("source.mp4", "out.mp4", "frame.png"))
            subprocess.run([
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "lavfi",
                "-i", "color=c=white:s=80x40:d=1:r=4", "-f", "lavfi",
                "-i", "sine=frequency=440:duration=1", "-shortest",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(source)
            ], check=True)
            width, height, duration = redact.dimensions(source, True)
            manifest = root / "masks.json"
            manifest.write_text(json.dumps({"regions": [
                {"x": 10, "y": 4, "width": 20, "height": 12, "mode": "solid", "color": "#E9EDF1"}
            ]}))
            regions = redact.load_regions(manifest, width, height, duration, True)
            redact.redact_video(source, output, regions)
            subprocess.run([
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(output),
                "-frames:v", "1", str(frame)
            ], check=True)
            with Image.open(frame) as result:
                masked = result.getpixel((15, 8))
                visible = result.getpixel((35, 8))
                self.assertGreater(min(masked), 220)
                self.assertLess(max(masked) - min(masked), 12)
                self.assertGreater(min(visible), 240)
            probe = subprocess.run([
                "ffprobe", "-v", "error", "-select_streams", "a",
                "-show_entries", "stream=index", "-of", "csv=p=0", str(output)
            ], check=True, capture_output=True, text=True)
            self.assertEqual(probe.stdout.strip(), "")


if __name__ == "__main__":
    unittest.main()
