from astropy.io import fits
from astropy.coordinates import SkyCoord
import astropy.units as u
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# 1. FITS 文件路径
# ============================================================

fits_file_1 = r".\research\hunt24-audit\data\raw\gaia_archive\gaiadr3_m45_wide.fits"
fits_file_2 = r".\research\hunt24-audit\data\raw\gaia_archive\gaiadr3_m45_background.fits"

# ============================================================
# 2. 读取 FITS
# ============================================================

coord_aliases = {
    "ra": [
        "ra",
        "RA",
        "Ra",
        "RA_ICRS",
        "ra_icrs",
        "RAJ2000",
        "raj2000",
        "_RAJ2000",
        "alpha",
        "Alpha",
        "ALPHA"
    ],

    "dec": [
        "dec",
        "DEC",
        "Dec",
        "DE_ICRS",
        "dec_icrs",
        "DEJ2000",
        "dej2000",
        "_DEJ2000",
        "delta",
        "Delta",
        "DELTA"
    ]
}

def find_coord_column(columns, aliases):
    """
    从 columns 中寻找与 aliases 匹配的列名。
    忽略大小写。
    """
    column_map = {
        col.lower(): col
        for col in columns
    }

    for alias in aliases:
        if alias.lower() in column_map:
            return column_map[alias.lower()]

    return None

def read_fits_radec(filename):
    """
    从 FITS 文件读取 RA 和 Dec。
    默认列名为 ra 和 dec。
    """

    with fits.open(filename) as hdul:
        # 一般 Gaia / VizieR 表格数据在 HDU 1
        data = hdul[1].data

        print(f"\nFile: {filename}")
        print("Columns:")
        print(data.columns.names)

        columns = data.columns.names

        ra_col = find_coord_column(
            columns,
            coord_aliases["ra"]
        )

        dec_col = find_coord_column(
            columns,
            coord_aliases["dec"]
        )

    print("RA column:", ra_col)
    print("Dec column:", dec_col)

    if ra_col is None or dec_col is None:
        raise ValueError(
            f"Cannot find RA/Dec columns.\n"
            f"Available columns: {columns}"
        )

    ra = np.asarray(data[ra_col], dtype=float)
    dec = np.asarray(data[dec_col], dtype=float)

    return ra, dec


ra1, dec1 = read_fits_radec(fits_file_1)
ra2, dec2 = read_fits_radec(fits_file_2)

print(f"\nFile 1 stars: {len(ra1)}")
print(f"File 2 stars: {len(ra2)}")


plt.figure(figsize=(10, 8))

plt.scatter(
    ra1,
    dec1,
    s=10,
    alpha=0.6,
    label="Field Stars"
)

plt.scatter(
    ra2,
    dec2,
    s=10,
    alpha=0.6,
    label="Background Stars"
)

plt.xlabel("RA [deg]")
plt.ylabel("Dec [deg]")

plt.title("Distribution of Field Stars and Background Stars of Mel 22")

plt.grid(alpha=0.3)

plt.legend()


# ============================================================
# 5. 天文学惯例：RA 从左向右减小
# ============================================================

plt.gca().invert_xaxis()


# ============================================================
# 6. 保存 PNG
# ============================================================

plt.tight_layout()

plt.savefig(
    r".\research\hunt24-audit\analysis\fieldbg.png",
    dpi=300,
    bbox_inches="tight"
)
