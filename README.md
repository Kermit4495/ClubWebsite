# ClubWebsite

## Notebook Issue: `pd.read_csv()` Failures

Several notebooks in this repository call `pandas.read_csv()`. Not all of them
will run successfully out of the box — some depend on paths or environments
that only exist on the original author's machine (or on Kaggle), and one was
apparently moved without updating its data path. This section documents each
`read_csv` call found across the `.ipynb` files, whether it currently works,
and how to fix the ones that don't.

### Background: what is a "file path"?

If you're new to programming, most of the problems below boil down to one
idea: **a path is just an address that tells the computer where to find a
file.** The rest of this section explains that idea before diving into the
specific bugs.

Think of your computer's storage like a set of nested folders (also called
"directories"), similar to folders inside folders on your Desktop:

```
/Users/alice/
├── Documents/
│   └── data/
│       └── Sales.csv
└── Downloads/
```

A **path** is just written directions for walking through those folders to
reach a specific file — the same way a street address tells a delivery
driver which house to go to. There are two kinds of paths:

- **Absolute path** — directions starting from the very top of the computer's
  file system, like a full mailing address. Example:
  `/Users/alice/Documents/data/Sales.csv`. This always points to the exact
  same file, no matter where you're "standing" (i.e., no matter what your
  program's current working directory is) — but it only works on the machine
  it was written for, since `/Users/alice/...` won't exist on someone else's
  computer.
- **Relative path** — directions starting from wherever you currently are,
  like telling someone "go up one floor, then it's the second door on the
  left." Example: `data/Sales.csv` means "look for a folder called `data`
  *right next to where I am now*, then find `Sales.csv` inside it." The
  special shorthand `..` means "go up one folder level" — so `../../data`
  means "go up two folders, then look for `data`."

The key thing that trips people up: **"where I am now" (the current working
directory) depends on where you launched the program from — not on where the
notebook file happens to be saved.** So a relative path like `../../data`
might work perfectly when you run the notebook from one folder, and fail
with a `FileNotFoundError` when you (or someone else, or a different
computer) run the exact same notebook from a different folder. That's
exactly what happens in several of the bugs described below — a path assumed
one folder layout, and the file got moved (or opened from somewhere else),
breaking the directions.

### Summary

| Notebook | Status | Root cause |
|---|---|---|
| `bike-store-sales-in-europe.ipynb` | ❌ Fails | Hardcoded Kaggle-only path |
| `W1-3-EDA-Univariate-Multi.ipynb` | ❌ Fails | Broken relative path after notebook was moved |
| `Movie_Analysis_Revised.ipynb` | ✅ Works (conditionally) | Relative path — only works if run from repo root |
| `Data_Loading_CSV.ipynb` | ✅ Works (conditionally) | Self-downloading helper — needs network access |
| `I94_Traffic_BigDataViz_Demo.ipynb` | ✅ Works (conditionally) | Reads directly from a remote URL — needs network access |
| `pandas.ipynb` | N/A | `read_csv` only appears in a comment, not executed |

---

### 1. `bike-store-sales-in-europe.ipynb` — ❌ Fails

**Code (cell 4):**
```python
Sales = pd.read_csv('/kaggle/input/bike-sales-in-europe/Sales.csv')
```

**Recorded error output:**
```
FileNotFoundError: [Errno 2] No such file or directory:
'/kaggle/input/bike-sales-in-europe/Sales.csv'
```

**Root cause:**
This notebook was authored and executed on [Kaggle](https://www.kaggle.com/),
where every attached dataset is automatically mounted read-only at
`/kaggle/input/<dataset-slug>/...`. That mount point is a Kaggle-runtime
artifact — it does not exist on a local machine, in CI, or in any environment
outside a Kaggle kernel. The path was left hardcoded when the notebook was
exported/copied into this repo, so any local run fails immediately at this
cell.

**Fix:**
1. Download the source dataset from Kaggle — search for **"Bike Sales in
   Europe"** (or the specific dataset the notebook was built against) and
   download `Sales.csv`.
2. Place the file somewhere inside (or relative to) this repo, e.g. `data/Sales.csv`.
3. Update the cell to use a portable path instead of the Kaggle-specific one:
   ```python
   from pathlib import Path
   Sales = pd.read_csv(Path(__file__).resolve().parent / 'data' / 'Sales.csv')
   # or, in a notebook, simply:
   Sales = pd.read_csv('data/Sales.csv')
   ```
4. (Optional, more robust) Mirror the pattern used in `Data_Loading_CSV.ipynb`
   (see below): write a small `ensure_data_file()` helper that checks for the
   file locally and downloads it if missing, so the notebook runs on any
   machine without manual setup.

---

### 2. `W1-3-EDA-Univariate-Multi.ipynb` — ❌ Fails

**Code (cell 3):**
```python
from pathlib import Path
DATA_DIR = Path("../../") / "data"
tracks = pd.read_csv(DATA_DIR / 'spotify_track_ratings.csv')
```

**Root cause:**
`Path("../../")` is resolved relative to the **current working directory of
the Python process** (i.e., wherever the notebook kernel was launched from),
not relative to the notebook file's location on disk. The double `../../`
implies this notebook was originally two directory levels deep (e.g. something
like `weeks/week1/W1-3-EDA-Univariate-Multi.ipynb`) with a shared `data/`
folder two levels up. In this repository, however, the notebook lives at the
top level (`ClubWebsite/W1-3-EDA-Univariate-Multi.ipynb`), so `../../data`
resolves outside the repo entirely — a location that doesn't exist:

```
$ ls ../../data
NOT FOUND
```

This is a classic "moved the file, forgot to update the relative path" bug.

**Fix (pick one):**
- **Preferred — fix the path in place:** Since `spotify_track_ratings.csv` is
  not checked into this repo, either:
  - Reuse the download helper from `Data_Loading_CSV.ipynb` (`ensure_data_file`)
    to fetch it automatically, or
  - Point `DATA_DIR` at wherever the file actually lives, e.g.:
    ```python
    DATA_DIR = Path.cwd()          # if the CSV sits next to the notebook
    # or an absolute/explicit path:
    DATA_DIR = Path("data")
    ```
- **Alternative — restore original structure:** If this notebook is meant to
  be part of a nested course/week structure with a shared `data/` directory,
  move it back into that structure (e.g. `weeks/week1/`) and restore the
  sibling `data/` folder two levels up.

In general, avoid `../../`-style relative paths for data files — they only
work when the working directory matches the author's original layout exactly.
Prefer paths anchored to the notebook itself or a small resolver helper.

---

### 3. `Movie_Analysis_Revised.ipynb` — ✅ Works, but only from the repo root

**Code (cell 1):**
```python
df = pd.read_csv("movie_cluster_data.csv")
```

**Status:** `movie_cluster_data.csv` exists directly in the repo root, so this
works today — but only because the notebook happens to sit next to the CSV
and is (presumably) launched with the repo root as the working directory.

**Risk / fix:** If this notebook is ever moved into a subfolder, or is run
with a different working directory (e.g. from CI, or opened via `jupyter
notebook` started from a different folder), this call will fail with
`FileNotFoundError` for the same reason as issue #2 above. To make it robust
regardless of working directory, anchor the path to the notebook's own
location:
```python
from pathlib import Path
NOTEBOOK_DIR = Path.cwd()  # or use a fixed known path
df = pd.read_csv(NOTEBOOK_DIR / "movie_cluster_data.csv")
```

---

### 4. `Data_Loading_CSV.ipynb` — ✅ Works, but needs network access

**Code (cell 1, helper + cells 3/10):**
```python
DATA_DIR = Path.home() / 'Downloads' / 'data_loading_csv_data'

DATA_SOURCES = {
    'yelp.csv': 'https://raw.githubusercontent.com/justmarkham/DAT8/master/data/yelp.csv',
    'spotify_track_ratings.csv': 'https://huggingface.co/datasets/maharshipandya/spotify-tracks-dataset/resolve/main/dataset.csv',
    'citibike_station_information.json': 'https://gbfs.citibikenyc.com/gbfs/en/station_information.json',
}

def ensure_data_file(filename):
    # checks DATA_DIR, cwd, and ~/Downloads first;
    # falls back to urlretrieve(DATA_SOURCES[filename]) if not found locally
    ...

csv_path = ensure_data_file('yelp.csv')
yelp = pd.read_csv(csv_path)
```

**Status:** This notebook is self-healing by design. `ensure_data_file()`
searches a few local candidate folders first and only reaches out to the
network if the file truly isn't present anywhere. This is a good pattern —
notably better than the hardcoded paths in issues #1 and #2.

**When it can still fail:**
- No internet access (offline environment, sandboxed CI, corporate firewall).
- One of the source URLs goes stale, moves, or the remote host rate-limits/blocks
  the request.
- The download succeeds but returns an empty/error page instead of real CSV
  content (the helper does check for a non-empty file, but not that its
  *contents* are valid CSV).

**Fix / hardening suggestions:**
- Cache a copy of these datasets inside the repo (e.g. under `data/`) so the
  notebook doesn't depend on external hosts at all.
- Add a content sanity check (e.g. verify the first line looks like a CSV
  header) after download, not just non-empty size.
- Wrap `urlretrieve` in a `try/except` with a clear message pointing at the
  manual-download fallback if the network call fails.

---

### 5. `I94_Traffic_BigDataViz_Demo.ipynb` — ✅ Works, but needs network access

**Code (cell 2):**
```python
url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00492/Metro_Interstate_Traffic_Volume.csv.gz'
df = pd.read_csv(url)
```

**Status:** `pandas.read_csv` can read directly from an HTTP(S) URL (and
transparently decompresses the `.gz`), so this works as long as the UCI
archive is reachable.

**When it can still fail:**
- No internet access.
- The UCI Machine Learning Repository reorganizes/removes the dataset path
  (this has happened before with UCI's older `.../machine-learning-databases/`
  URLs).

**Fix / hardening suggestion:** Download the file once and commit a local
copy (or use the same `ensure_data_file`-style caching helper as in
`Data_Loading_CSV.ipynb`) so the notebook is reproducible without depending on
an external server's continued availability.

---

### 6. `pandas.ipynb` — Not an actual failure

The only `read_csv` occurrence here is inside a comment:
```python
# sales.to_csv("sales_data.csv", index=False) # saving the DataFrame to a CSV file
## When reading a CSV file back into a DataFrame by `pd.read_csv()`, pandas will "infer" ...
```
No code is executed, so there is nothing to fix.

---

### General recommendation

The two real bugs (`bike-store-sales-in-europe.ipynb` and
`W1-3-EDA-Univariate-Multi.ipynb`) share the same underlying mistake: a path
was hardcoded to a specific environment or directory depth (a Kaggle mount,
or `../../` relative to an assumed folder structure) and never revalidated
after the notebook was copied into this repository. The `ensure_data_file()`
pattern in `Data_Loading_CSV.ipynb` is the most portable approach used in this
repo — future notebooks that load external CSVs should follow it: check a few
local candidate locations first, fall back to a documented download URL, and
fail with a clear, actionable error message if neither is available.
