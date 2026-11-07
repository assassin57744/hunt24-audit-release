# Open Cluster Membership with Gaia DR3

Code for my research project **"Supplementing Catalogues of Open Clusters Using Gaia DR3 Data"** (manuscript in preparation, 2026).

**Author:** Chen Li, Gleneagle Secondary School, Coquitlam, BC, Canada

## Overview

This pipeline re-examines the membership of four open clusters and compares the results with the open cluster catalogue of Hunt & Reffert:

| Key | Cluster |
|-----|---------|
| M45 | Melotte 22 (Pleiades) |
| M44 | NGC 2632 (Praesepe) |
| M67 | NGC 2682 |
| M41 | NGC 2287 |

`config.py` also contains settings for M13 (NGC 6205, a globular cluster), which I used only for testing.

The pipeline has four main steps:

1. **Preprocessing** of Gaia DR3 data around each cluster.
2. **Seed selection** with HDBSCAN, to find a set of stars that clearly belong to the cluster.
3. **Membership probabilities** from a Gaussian Mixture Model (GMM), using the seed stars as a prior.
4. **Validation** of the candidate members with pyUPMASK.

The results are then cross-matched with the reference catalogue. Stars found by both are "Matched". Stars found only by this pipeline are "PG Only", and stars found only in the catalogue are "Ref Only".

## Repository structure

```
hunt24-audit/
    main.py              command-line entry point
    config.py            paths and per-cluster parameters
    modules/             pipeline stages (seeds, GMM, validation, audit, reports)
    modules/pyUPMASK/    modified copy of pyUPMASK (GPL-3.0)
    utils/               data download and helper scripts
    tests/               tests
    diffparam.py         one-off plot: M44 results for different seed parameters
    drawCSV.py           one-off plot: M45 wide field and background ring
    errormag.py          one-off plot: M67 parallax error vs. G magnitude
```

## Requirements

- Python 3.10 or later
- Install the dependencies:

```
pip install -r requirements.txt
```

## Data

Data files are not included in this repository (the `data/` folder is ignored by git). The ready-to-use input files are published once as attachments of the [`data-v1` release](https://github.com/assassin57744/hunt24-audit-release/releases/tag/data-v1), shared by all code releases. See `data/raw/gaia_archive/README.md` and `data/raw/vizier/README.md` for the file list and where to put each file.

The data come from:

- **Gaia DR3** (`gaiadr3.gaia_source`) through the Gaia Archive. Script: `research/hunt24-audit/utils/data_fetcher.py`.
- **Reference catalogues** through VizieR. Script: `research/hunt24-audit/utils/vizier_fetcher.py`.
- **Cluster parameters** (centre, distance, proper motion) from SIMBAD. Script: `research/hunt24-audit/utils/query_simbad.py`.

Example (run inside `research/hunt24-audit`):

```
python -c "from utils.data_fetcher import GaiaDataFetcher; GaiaDataFetcher().fetch_cluster('M45')"
python utils/vizier_fetcher.py
```

Each cluster has a background field: a ring 3° wide just outside the wide field. To test how the results depend on the background, `utils/split_background.py` cuts this ring into narrower rings (1° and 2° wide by default) and saves them as `gaiadr3_{cluster}_background_{1,2}deg.fits` next to the original file:

```
python utils/split_background.py                 # all clusters, 1° and 2°
python utils/split_background.py m45 --widths 1.5
```

Logging in to the Gaia Archive is optional. It gives a larger quota. To log in, set the environment variables `GAIA_USER` and `GAIA_PWD`. Never write credentials into the code.

## Usage

Run inside `research/hunt24-audit`:

```
python main.py M45              # one cluster
python main.py M44,M41          # several clusters
python main.py all              # all configured clusters
python main.py M67 --skip-viz   # skip the plotting stage
python main.py --help           # list all options
```

By default, the comparison uses the Hunt & Reffert catalogue (`--category hunt`) and HDBSCAN for the seed stars (`--algo hdbscan`). Results are written to `analysis/` and logs to `logs/`.

## Third-party code

`research/hunt24-audit/modules/pyUPMASK/` is a modified copy of [pyUPMASK](https://github.com/msolpera/pyUPMASK) (Pera et al. 2021), which is licensed under GPL-3.0. My changes:

- adapted the entry point (`pyUPMASK.py`) so the method can be called from this pipeline;
- replaced the deprecated `distutils.util.strtobool` in `modules/dataIO.py` so the code runs on newer Python versions.

## Use of AI tools

I used several AI tools while developing this code:

- **Gemini, DeepSeek, ChatGPT, Claude and Zhipu GLM**, mainly to restructure (refactor) the program and to adjust the logging output;
- **GitHub Copilot, Cline and Codeium**, mainly for code completion in the editor.

The research question, the choice of methods and parameters, and the interpretation of the results are my own. All cluster parameters used in the pipeline come from SIMBAD and the published literature.

## Acknowledgements

I thank Dr. Songmei Qin (Sun Yat-sen University) for her feedback on my methods and drafts.

This work has made use of data from the European Space Agency (ESA) mission Gaia (https://www.cosmos.esa.int/gaia), processed by the Gaia Data Processing and Analysis Consortium (DPAC). This research has made use of the SIMBAD database and the VizieR catalogue access tool, operated at CDS, Strasbourg, France.

## References

- Gaia Collaboration, Vallenari, A., et al. 2023, A&A, 674, A1 (Gaia DR3)
- Hunt, E. L., & Reffert, S. 2023, A&A, 673, A114
- Hunt, E. L., & Reffert, S. 2024, A&A, 686, A42
- Pera, M. S., et al. 2021, A&A, 650, A109 (pyUPMASK)

## License

This project is licensed under the GNU General Public License v3.0. See [LICENSE](LICENSE).
