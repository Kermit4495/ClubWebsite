# Context Document with an Annotated Iris Dataset Example

> This combined Markdown file includes two parts:
>
> - **Part I:**  How to write a `context document` file.
> - **Part II:** A complete annotated `Instruction.md` example using the classical Iris Flower Dataset.

---


---

## 0. What is a `Instruction.md` file?

A `Instruction.md` file is a documentation file.

It usually explains:

- Where the data comes from 
- What the project or dataset is
- What files are included
- How to run the code (with sample code)
- What outputs are generated
- Important notes

You can think of it as the **instruction manual** for a project folder.

---

## 1. File types: 

| File type | Meaning | Example |
|---|---|---|
| `.md` | Markdown documentation file | `Instruction.md` |
| `.py` | Python script file | `prepare_data.py` |
| `.csv` | Table/data file | `data.csv` |
| `.txt` | Plain text file | `notes.txt` |
| `.json` | Structured metadata/settings file | `summary.json` |
| `.edf` | Multichannel biomedical time-series file | `signal.edf` |

Important idea:

- A `.md` file usually explains the project.
- A `.py` file does the actual computation.
- A `.csv` file usually stores tabular data.
- A `.txt` file stores plain text.
- A `.json` file stores structured information.
- A `.edf`  file stores EEG signlas data

---

## 3. Basic Markdown syntax

### 3.1 Headings

Use `#` for headings.

```md
# Main title

## Section title

### Subsection title
```

Rendered result:

# Main title

## Section title

### Subsection title

---

### 3.2 Bullet points

```md
- item 1
- item 2
- item 3
```

Rendered result:

- item 1
- item 2
- item 3

---

### 3.3 Numbered lists

```md
1. Step one
2. Step two
3. Step three
```

Rendered result:

1. Step one
2. Step two
3. Step three

---

### 3.4 Inline code

Use backticks around short code words.

```md
The file is called `Instruction.md`.
```

Rendered result:

The file is called `Instruction.md`.

---

### 3.5 Code blocks

Use three backticks for commands or code.

````md
```bash
python prepare_data.py
```
````

Rendered result:

```bash
python prepare_data.py
```

---

### 3.6 Tables

Markdown tables use the vertical bar symbol `|`.

```md
| File | Description |
|---|---|
| `data.csv` | Raw data |
| `prepare_data.py` | Python script |
| `README.md` | Documentation |
```

Rendered result:

| File | Description |
|---|---|
| `data.csv` | Raw data |
| `prepare_data.py` | Python script |
| `Instruction.md` | Documentation |

---

## 4. Common symbols in Markdown and coding

| Symbol | Name | Meaning |
|---|---|---|
| `#` | hash / pound sign | Heading in Markdown |
| `/` | slash / forward slash | Used in file paths |
| `\` | backslash | Different from slash; often used in Windows paths or escape characters |
| `*` | asterisk | Wildcard in file patterns; also used for emphasis |
| `|` | vertical bar / pipe | Used in Markdown tables |
| ``` ` ``` | backtick | Used for inline code and code blocks |

Example:

```text
PNxx/*.edf
```

This means:

- `PNxx/` = a subject folder, such as `PN00/`
- `*` = any file name
- `.edf` = EDF file extension

So `PNxx/*.edf` means:

```text
any EDF file inside a subject folder
```

Examples:

```text
PN00/PN00-1.edf
PN01/PN01-2.edf
PN03/recording.edf
```

---

## 5. What should a dataset Instruction.md include?

A good dataset Instruction.md usually has these sections:

```md
# Dataset Name

## Description

## Source

## Files

## How to run

## Outputs

## Notes
```

For a more complete Instruction.md, you may also include:

```md
## Download

## Preprocessing
```

---

## 6. Minimal Instruction template

Copy this into a new file called `Instruction.md`.

````md
# My Dataset

This folder contains data and scripts for our project.

## Source

- Dataset page:
- DOI:
- Local folder:

## Files

| File | Description |
|---|---|
| `data.csv` | Raw data |
| `prepare_data.py` | Python script for data preparation |
| `Instruction.md` | Documentation file |

## How to run

```bash
python prepare_data.py
```

## Outputs

| Output file | Description |
|---|---|
| `processed_data.csv` | Cleaned data |

## Notes

- This Instruction explains the dataset.
- The Python script does the actual work.
- Check the instructions before running the script.
````
---

## 7. Real example: Iris_Example Dataset

Now let us look at a simple public dataset example.

The dataset is called:

```md
# Iris_Example
```

It is based on the classical Iris Flower Dataset.

Each row is one iris flower, and the dataset contains four flower measurements plus one species label.

In this project folder, the `Instruction.md` explains:

- The dataset source
- How to download or reuse the data
- What raw files exist
- What processed files are generated
- What the Python script does
- How to load the data and start a simple classification task

---

## 8. Source section

A source section explains where the data comes from.

Example:

```md
## Source

- Repository: UCI Machine Learning Repository
- Dataset page: https://archive.ics.uci.edu/dataset/53/iris
- DOI: https://doi.org/10.24432/C56C76
- Local folder: `Iris_Example/`
```

### What is DOI?

DOI means **Digital Object Identifier**.

It is a permanent academic identifier for a paper, dataset, or other research object.

A DOI is useful when you need to cite a dataset in a report or research paper.

---

## 9. Download section

The `Instruction.md` may include commands like:

```bash
python prepare_iris.py --download --save-csv
python prepare_iris.py --no-download --save-csv
```

These are terminal commands.

They are not Python code that you type inside a Python file.

---

## 10. What does this command mean?

Example:

```bash
python prepare_iris.py --download --save-csv
```

Breakdown:

| Part | Meaning |
|---|---|
| `python` | Use Python to run a script |
| `prepare_iris.py` | The Python script file |
| `--download` | Fetch the Iris dataset from the online source |
| `--save-csv` | Save processed data as CSV files |

Important:

```text
--download means the script may access the internet to fetch the dataset.
```

If the data already exists locally, you can use:

```bash
python prepare_iris.py --no-download --save-csv
```

---

## 11. Download vs no download

### This may download data:

```bash
python prepare_iris.py --download --save-csv
```

Why?

Because it includes:

```bash
--download
```

### This does not download data:

```bash
python prepare_iris.py --no-download --save-csv
```

Why?

Because `--no-download` means:

```text
Use local files only.
Do not download new files.
```

---

## 12. What is a Python script?

A Python script is a `.py` file that performs actions.

In this example:

```text
prepare_iris.py
```

is the script.

The `Instruction.md` is the instruction manual.

The Python script does the work.

| File | Role |
|---|---|
| `Instruction.md` | Explains the project |
| `prepare_iris.py` | Runs the data preparation |
| `raw/` | Stores raw downloaded or local data |
| `processed/` | Stores processed output files |

---

## 13. Raw files

The `Instruction.md` may show raw files like:

```text
iris.data
iris.names
```

These are raw dataset files.

### `iris.data`

This is the main data file.

It contains rows of iris flower measurements and species labels.

### `iris.names`

This is the dataset description file.

It explains the variables, class labels, and background information.

Examples of raw files:

```text
raw/iris.data
raw/iris.names
```

---

## 14. Processed files

The `Instruction.md` may list processed files like this:

```md
| File | Rows represent |
|---|---|
| `iris_clean.csv` | One row per iris flower |
| `features.csv` | Four numeric flower measurements |
| `labels.csv` | Species label for each flower |
| `train.csv` | Training split for modeling practice |
| `test.csv` | Test split for model evaluation |
| `summary.json` | Dataset counts and preprocessing settings |
```

Rendered table:

| File | Rows represent |
|---|---|
| `iris_clean.csv` | One row per iris flower |
| `features.csv` | Four numeric flower measurements |
| `labels.csv` | Species label for each flower |
| `train.csv` | Training split for modeling practice |
| `test.csv` | Test split for model evaluation |
| `summary.json` | Dataset counts and preprocessing settings |



---

## Notes

- This activity uses a simple public dataset.
- Each row is one flower.
- The four numeric measurements are features.
- The species column is the label.
- Use `--no-download` if the data already exists locally.
