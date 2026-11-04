# vizier — Literature reference catalogs (VizieR)

> ⚠️ **The data files in this directory are not included in the Git repository.**
>
> They total about 460 MB, and `vizier_hunt24_full.parquet` alone is about 410 MB, which exceeds GitHub's repository file size limit. They are distributed as release attachments instead.
> Before running the pipeline, **download the data attachments from the GitHub Releases page** and extract them into this directory, keeping the file names shown below:
>
> 👉 <https://github.com/assassin57744/hunt24-audit-release/releases>

>
> Download the attachments from the release that matches the code version you are using (the `public-hunt24-audit-vX.Y.Z` tag).

The pipeline reads this directory through `VIZIER_INPUT_DIR` in `config.py` (i.e. `data/raw/vizier/`). These catalogs are the external literature membership tables that the audit compares against.

## Directory layout

```text
vizier/
├── README.md                                # This file
├── vizier_hunt24_full.parquet               # Hunt & Reffert (2024)                    J/A+A/686/A42      ~410 MB   IDX_HUNT
├── vizier_zerj23.parquet                    # Zerjal et al. (2023)                                        ~3.8 MB   IDX_ZERJ
├── vizier_risb25.vot                        # Risbud et al. (2025), VOTable            J/A+A/694/A258     ~5.9 MB   IDX_RISB
├── vizier_cg2020_full.parquet               # Cantat-Gaudin et al. (2020)              J/A+A/633/A99      ~50 MB    IDX_CG20
├── vizier_heyl22_members.parquet            # Heyl et al. (2022), members              J/ApJ/926/132      ~105 KB   IDX_HEYL
└── vizier_heyl22_escapee_candidates.parquet # Heyl et al. (2022), escapee candidates   J/ApJ/926/132      ~33 KB    IDX_HEYL
```

## Notes

- **All 6 files are required.** Each is registered in `MANIFEST` in `config.py` under the matching `IDX_*` key.
- Heyl22 is loaded with the wildcard `vizier_heyl22_*.parquet`, so both files must be present.
- CG2020 uses Gaia DR2 source IDs. The pipeline converts them with the DR2 -> DR3 cross-match tables in `../gaia_archive/`, so the `gaia_archive` data is needed as well.
- File names must match the entries in `config.py`. Do not rename them.
