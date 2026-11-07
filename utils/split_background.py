"""将 3° 宽背景环 (gaiadr3_{c}_background.fits) 切分为外扩 1° / 2° 的子环。

背景环 = wide 视场外扩 3° 的圆环 [R_wide, R_wide + 3]。
本脚本输出 [R_wide, R_wide + w] (w = 1, 2) 的子集，格式、列定义、表头与原文件一致：
    gaiadr3_{c}_background_1deg.fits
    gaiadr3_{c}_background_2deg.fits

圆心与 R_wide 由实际数据反推得到（config.py 中的 CENTER/RADIUS 与查询时用的并不完全一致）：
wide 的最大角距 == 背景的最小角距 == R_wide，背景最大角距 == R_wide + 3。
运行时会再次校验这一点。

用法:  python scripts/split_background.py [m41 m44 ...] [--widths 1 2]
"""
import argparse
from pathlib import Path

import numpy as np
from astropy.io import fits

GAIA_DIR = Path(__file__).resolve().parents[1] / "data" / "raw" / "gaia_archive"

# cluster: (ra0, dec0, R_wide) —— 查询 Gaia Archive 时使用的圆心与 wide 半径 (deg)
RING_GEOMETRY = {
    "m41": (101.50, -20.75, 5.0),
    "m44": (130.10, 19.70, 11.9),
    "m45": (56.75, 24.12, 17.78),
    "m67": (132.85, 11.81, 5.0),
}
FULL_WIDTH = 3.0
TOL = 1e-3  # deg，校验容差


def ang_sep(ra, dec, ra0, dec0):
    """球面角距 (deg)，haversine 形式，数值稳定。"""
    ra, dec, ra0, dec0 = map(np.radians, (ra, dec, ra0, dec0))
    h = np.sin((dec - dec0) / 2) ** 2 + np.cos(dec) * np.cos(dec0) * np.sin((ra - ra0) / 2) ** 2
    return np.degrees(2 * np.arcsin(np.sqrt(np.clip(h, 0, 1))))


def radec_cols(names):
    ra = "RA_ICRS" if "RA_ICRS" in names else "ra"
    dec = "DE_ICRS" if "DE_ICRS" in names else "dec"
    return ra, dec


def split(cluster, widths, gaia_dir=GAIA_DIR):
    ra0, dec0, r_in = RING_GEOMETRY[cluster]
    src = Path(gaia_dir) / f"gaiadr3_{cluster}_background.fits"
    with fits.open(src, memmap=True) as hdul:
        tab = hdul[1]
        rc, dc = radec_cols(tab.columns.names)
        sep = ang_sep(np.asarray(tab.data[rc], float), np.asarray(tab.data[dc], float), ra0, dec0)

        lo, hi = sep.min(), sep.max()
        if abs(lo - r_in) > TOL or abs(hi - (r_in + FULL_WIDTH)) > TOL:
            raise RuntimeError(
                f"{cluster}: 背景环几何与预期不符: sep∈[{lo:.4f}, {hi:.4f}], "
                f"预期 [{r_in}, {r_in + FULL_WIDTH}]"
            )
        print(f"[{cluster}] 原背景 N={len(sep):,}, sep∈[{lo:.4f}, {hi:.4f}] deg")

        for w in widths:
            r_out = r_in + w
            mask = sep <= r_out
            hdr = tab.header.copy()
            hdr["RING_RA"] = (ra0, "[deg] ring center RA (ICRS)")
            hdr["RING_DEC"] = (dec0, "[deg] ring center Dec (ICRS)")
            hdr["RING_RIN"] = (r_in, "[deg] inner radius (= wide field radius)")
            hdr["RING_ROUT"] = (r_out, "[deg] outer radius")
            hdr["RING_W"] = (w, "[deg] ring width")
            hdr["RINGSRC"] = (src.name, "parent background file")
            out_hdu = fits.BinTableHDU(data=tab.data[mask], header=hdr, name=tab.name)
            dst = src.parent / f"gaiadr3_{cluster}_background_{w:g}deg.fits"
            fits.HDUList([hdul[0].copy(), out_hdu]).writeto(dst, overwrite=True)
            print(f"    -> {dst.name}: [{r_in}, {r_out}] deg, N={mask.sum():,} "
                  f"({mask.mean():.1%})")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("clusters", nargs="*", default=list(RING_GEOMETRY))
    ap.add_argument("--widths", nargs="+", type=float, default=[1, 2])
    ap.add_argument("--dir", default=str(GAIA_DIR), help="gaia_archive 目录 (默认: 本项目 data/raw/gaia_archive)")
    args = ap.parse_args()
    for c in args.clusters:
        split(c, args.widths, args.dir)


if __name__ == "__main__":
    main()
