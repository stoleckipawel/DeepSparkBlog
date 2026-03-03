"""
Export the OG thumbnail from the promo R&D page.
Captures the #og-thumb element at 2× resolution (2400×1260) then
downscales to 1200×630 for crisp social sharing images.

Usage:
    python promotion/export_og_thumb.py [--url URL] [--out PATH]

Requires: pip install pyppeteer Pillow
"""
import asyncio, argparse, pathlib

async def export(url: str, out: pathlib.Path):
    from pyppeteer import launch
    edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    browser = await launch(
        headless=True,
        executablePath=edge,
        args=["--no-sandbox", "--disable-gpu", "--force-device-scale-factor=2"],
    )
    page = await browser.newPage()
    await page.setViewport({"width": 1400, "height": 900, "deviceScaleFactor": 2})
    await page.goto(url, {"waitUntil": "networkidle0", "timeout": 30_000})
    await asyncio.sleep(1)  # let fonts settle

    el = await page.querySelector("#og-thumb")
    if not el:
        print("ERROR: #og-thumb element not found on page")
        await browser.close()
        return

    out.parent.mkdir(parents=True, exist_ok=True)
    raw = out.with_suffix(".raw.png")
    await el.screenshot({"path": str(raw)})
    await browser.close()

    # Downscale from 2× to exact 1200×630
    from PIL import Image
    img = Image.open(raw)
    img = img.resize((1200, 630), Image.LANCZOS)
    img.save(str(out), optimize=True)
    raw.unlink()
    print(f"Saved {out}  ({img.size[0]}×{img.size[1]})")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://localhost:1313/promo-linkedin/")
    ap.add_argument("--out", default="assets/images/og-frame-graph-series.png")
    args = ap.parse_args()
    asyncio.run(export(args.url, pathlib.Path(args.out)))
