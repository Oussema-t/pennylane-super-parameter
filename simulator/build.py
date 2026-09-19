"""Wrap circuit_simulator.html (a head-less fragment used for the claude.ai artifact)
into a complete standalone page, simulator/index.html, that opens from disk or any static host."""
from pathlib import Path

HERE = Path(__file__).parent
src = (HERE / "circuit_simulator.html").read_text(encoding="utf-8")
cut = src.index("</style>") + len("</style>")
head, body = src[:cut], src[cut:]

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="light dark">
<meta name="description" content="Step-by-step 3-qubit simulator for the PennyLane Super Parameter challenge: circuit canvas, statevector, probabilities and Bloch spheres.">
{head}
</head>
<body>{body}
</body>
</html>
"""
(HERE / "index.html").write_text(page, encoding="utf-8")
print(f"wrote {HERE / 'index.html'} ({len(page)} bytes)")
