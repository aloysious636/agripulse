"""Generate app icon (PNG + ICO) with the standard library only."""
import struct, zlib
from pathlib import Path

N = 256
BG, FG, LEAF = (15, 61, 42), (52, 211, 153), (243, 244, 239)

def inside_round(x, y, r=48):
    cx = min(max(x, r), N - 1 - r); cy = min(max(y, r), N - 1 - r)
    return (x - cx) ** 2 + (y - cy) ** 2 <= r * r

def dist_seg(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return ((px - ax - t * dx) ** 2 + (py - ay - t * dy) ** 2) ** 0.5

pts = [(36, 150), (92, 150), (112, 100), (140, 190), (164, 120), (178, 150), (222, 150)]
rows = []
for y in range(N):
    row = bytearray([0])
    for x in range(N):
        if not inside_round(x, y):
            row += bytes((0, 0, 0, 0)); continue
        col = BG
        if any(dist_seg(x, y, *pts[i], *pts[i + 1]) <= 9 for i in range(len(pts) - 1)):
            col = FG
        if ((x - 128) / 34) ** 2 + ((y - 64) / 24) ** 2 <= 1:
            col = LEAF
        row += bytes((*col, 255))
    rows.append(bytes(row))
raw = b"".join(rows)

def chunk(t, d):
    c = struct.pack(">I", len(d)) + t + d
    return c + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)

png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", N, N, 8, 6, 0, 0, 0)) + \
      chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
out = Path(__file__).resolve().parent.parent / "app" / "static" / "images"
(out / "agripulse.png").write_bytes(png)
ico = struct.pack("<HHH", 0, 1, 1) + struct.pack("<BBBBHHII", 0, 0, 0, 0, 1, 32, len(png), 22) + png
(out / "agripulse.ico").write_bytes(ico)
print("icon written", len(png), "bytes")
