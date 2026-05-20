"""PPTX → PDF via LibreOffice (headless).

Strategy:
  1. Try the fast path: plain `soffice --headless --convert-to pdf`.
     This uses the user's default LibreOffice profile and is the fastest path.
  2. If that fails (typically because a LibreOffice UI session holds a lock on
     the user profile), retry with an isolated `-env:UserInstallation=` profile.
     The isolated profile's first call exits 81 while LO bootstraps the
     profile, so we run it twice.

Pre-requisite: `libreoffice-impress` must be installed.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

# Candidate paths for the LibreOffice headless binary (cross-platform).
SOFFICE_CANDIDATES = [
    "/usr/lib/libreoffice/program/soffice.bin",                   # Linux (apt)
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",       # macOS (brew cask)
    "/opt/homebrew/bin/soffice",                                  # macOS (Apple Silicon brew)
    "/usr/local/bin/soffice",                                     # macOS (Intel brew)
    "C:\\Program Files\\LibreOffice\\program\\soffice.exe",       # Windows
]


def soffice_path() -> str | None:
    """Return path to LibreOffice if present, else None. Never raises."""
    for p in SOFFICE_CANDIDATES:
        if os.path.exists(p):
            return p
    return shutil.which("soffice") or shutil.which("libreoffice")


def _resolve_soffice() -> str:
    found = soffice_path()
    if not found:
        raise RuntimeError(
            "LibreOffice not found. Install it to enable PPTX → PDF conversion:\n"
            "  · Linux : apt install libreoffice-impress libreoffice-writer\n"
            "  · macOS : brew install --cask libreoffice\n"
            "  · Windows : https://www.libreoffice.org/download/"
        )
    return found


def _run_convert(soffice: str, pptx_path: Path, work_dir: Path,
                 *, profile_url: str | None = None,
                 timeout: int = 120) -> tuple[int, str, str]:
    """Run a single soffice conversion. Returns (returncode, stdout, stderr)."""
    cmd = [soffice]
    if profile_url:
        cmd.append(f"-env:UserInstallation={profile_url}")
    cmd += ["--headless", "--convert-to", "pdf",
            "--outdir", str(work_dir), str(pptx_path)]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return proc.returncode, proc.stdout, proc.stderr


def pptx_to_pdf(pptx_path: str | os.PathLike,
                pdf_path: str | os.PathLike | None = None) -> str:
    """Convert a single .pptx to .pdf. Returns the resulting PDF path.

    If `pdf_path` is None, writes next to the PPTX with the same stem.
    """
    pptx_path = Path(pptx_path).resolve()
    if not pptx_path.exists():
        raise FileNotFoundError(pptx_path)

    if pdf_path is None:
        outdir = pptx_path.parent
        target = outdir / (pptx_path.stem + ".pdf")
    else:
        target = Path(pdf_path).resolve()
        outdir = target.parent
    outdir.mkdir(parents=True, exist_ok=True)

    soffice = _resolve_soffice()

    # Convert into a fresh tmp dir, NOT the final outdir. Otherwise a stale
    # PDF from a previous build would mask a silent LO failure (returns 0
    # even when nothing was produced).
    work_dir = Path(tempfile.mkdtemp(prefix="lo-slider-out-"))
    profile_dir: Path | None = None
    try:
        produced = work_dir / (pptx_path.stem + ".pdf")
        rc1, out1, err1 = _run_convert(soffice, pptx_path, work_dir)

        if not produced.exists():
            # Fast path failed — likely a LibreOffice UI session holds the
            # default profile lock. Retry with an isolated profile.
            profile_dir = Path(tempfile.mkdtemp(prefix="lo-slider-prof-"))
            profile_url = profile_dir.as_uri()

            # Bootstrap the fresh profile: the first call exits 81 but
            # initializes the profile dir. Discard its output.
            _run_convert(soffice, pptx_path, work_dir, profile_url=profile_url,
                         timeout=30)

            rc2, out2, err2 = _run_convert(soffice, pptx_path, work_dir,
                                           profile_url=profile_url)
            if not produced.exists():
                raise RuntimeError(
                    f"LibreOffice conversion failed for {pptx_path}.\n"
                    f"  fast path : rc={rc1} stderr={err1.strip()!r}\n"
                    f"  isolated  : rc={rc2} stderr={err2.strip()!r}\n"
                    "If LibreOffice's UI is open elsewhere, try closing it.\n"
                    "Or verify that libreoffice-impress is installed:\n"
                    "  apt list --installed 2>/dev/null | grep impress"
                )

        # Move into place — overwrite any previous output.
        if target.exists():
            target.unlink()
        shutil.move(str(produced), str(target))
        return str(target)
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)
        if profile_dir is not None:
            shutil.rmtree(profile_dir, ignore_errors=True)
