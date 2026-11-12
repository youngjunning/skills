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
    def test_image_masks_exact_pixels_and_rejects_wrong_dimensions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, output, manifest = (root / name for name in ("source.png", "out.png", "masks.json"))
            image = Image.new("RGB", (80, 40), (255, 255, 255))
            for x in range(40, 60):
                for y in range(5, 17):
                    image.putpixel((x, y), (x * 3, y * 12, 0))
            image.save(source)
            manifest.write_text(json.dumps({"width": 80, "height": 40, "regions": [
                {"x": 10, "y": 5, "width": 20, "height": 12, "mode": "solid"},
                {"x": 40, "y": 5, "width": 20, "height": 12, "mode": "mosaic"}
            ]}))
            regions = redact.load_regions(manifest, 80, 40, None, False)
            redact.redact_image(source, output, regions)
            with Image.open(output) as result:
                self.assertEqual(result.getpixel((10, 5)), (0, 0, 0))
                self.assertEqual(result.getpixel((29, 16)), (0, 0, 0))
                self.assertEqual(result.getpixel((30, 16)), (255, 255, 255))
                self.assertEqual(result.getpixel((40, 5)), result.getpixel((59, 16)))
            with self.assertRaisesRegex(ValueError, "dimensions"):
                redact.load_regions(manifest, 81, 40, None, False)

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
                {"x": 10, "y": 4, "width": 20, "height": 12, "mode": "solid"},
                {"x": 40, "y": 4, "width": 20, "height": 12, "mode": "mosaic"}
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
                self.assertLess(max(masked), 15)
                self.assertGreater(min(visible), 240)
            probe = subprocess.run([
                "ffprobe", "-v", "error", "-select_streams", "a",
                "-show_entries", "stream=index", "-of", "csv=p=0", str(output)
            ], check=True, capture_output=True, text=True)
            self.assertEqual(probe.stdout.strip(), "")


if __name__ == "__main__":
    unittest.main()
