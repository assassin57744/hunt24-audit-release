# gaia_archive — Gaia DR3 raw data

> ⚠️ **The data files in this directory are not included in the Git repository.**
>
> They total about 6 GB, and the largest single file is about 1.6 GB, which exceeds GitHub's repository file size limit. They are distributed as release attachments instead.
> Before running the pipeline, **download the data attachments from the GitHub Releases page** and extract them into this directory, keeping the file names and layout shown below:
>
> 👉 <https://github.com/assassin57744/astro-research/releases>
>
> Download the attachments from the release that matches the code version you are using (the `public-hunt24-audit-vX.Y.Z` tag).

The pipeline reads this directory through `GAIA_INPUT_DIR` in `config.py` (i.e. `data/raw/gaia_archive/`).

## Directory layout

```text
gaia_archive/
├── README.md                                                  # This file
│
│   # --- Target cluster fields (Gaia DR3 wide-field source tables; IDX_FIELD_CLUSTER_* in MANIFEST) ---
├── gaiadr3_m41_wide.fits                                      # M41 (NGC 2287)          ~453 MB
├── gaiadr3_m44_wide.fits                                      # M44 (Praesepe)          ~427 MB
├── gaiadr3_m45_wide.fits                                      # M45 (Pleiades)          ~1.6 GB
├── gaiadr3_m67_wide.fits                                      # M67 (NGC 2682)          ~56 MB
│
│   # --- Background fields (IDX_FIELD_CLUSTER_*_BKG in MANIFEST) ---
├── gaiadr3_m41_background.fits                                #                         ~731 MB
├── gaiadr3_m44_background.fits                                #                         ~196 MB
├── gaiadr3_m45_background.fits                                #                         ~849 MB
├── gaiadr3_m67_background.fits                                #                         ~91 MB
│
│   # --- Gaia DR2 -> DR3 cross-match tables (IDX_DR2IDX; matched by gaia_gaiadr3_dr2_neighbourhood_Melotte_22_r*) ---
├── gaia_gaiadr3_dr2_neighbourhood_Melotte_22_r2_0.fits        #                         ~2.6 MB
├── gaia_gaiadr3_dr2_neighbourhood_Melotte_22_r2_0_4_0.fits    #                         ~7.8 MB
├── gaia_gaiadr3_dr2_neighbourhood_Melotte_22_r4_0_5_0.fits    #                         ~5.9 MB
│
│   # --- External pyUPMASK membership results (read by modules/auditor.py as {cluster}_pyUPMASK.csv) ---
├── m41_pyUPMASK.csv
├── m44_pyUPMASK.csv
├── m45_pyUPMASK.csv
├── m67_pyUPMASK.csv
│
│   # --- Parquet copies / earlier versions; not read by the current pipeline (optional) ---
├── gaiadr3_m41_wide.parquet
├── gaiadr3_m44_wide.parquet
├── gaiadr3_m45_wide.parquet
└── gaiadr3_m67_wide.parquet

```

## Notes

- **Required files**: `*_wide.fits`, `*_background.fits`, `gaia_gaiadr3_dr2_neighbourhood_Melotte_22_r*.fits` and `*_pyUPMASK.csv`. Without them, the analysis for the corresponding cluster cannot run.
- **Optional files**: `*_wide.parquet` and the `no_errors/` directory, kept for reference or for reproducing earlier results.
- `MANIFEST` in `config.py` also registers `.fits` files for Mel 25, Mel 111 and M13. These are not part of the current data package; you only need to prepare them yourself if you analyze those clusters.
- File names must match the entries in `config.py`. Do not rename them.
