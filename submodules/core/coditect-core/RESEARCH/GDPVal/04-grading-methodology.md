# GDPval: Grading Methodology

## 1. Human Expert Grading

### Approach: Blinded Pairwise Comparisons

Experts in the relevant occupation are presented with:
1. **Request** (task prompt)
2. **Reference files** (if any)
3. **Two or more unlabeled deliverables** (human vs. model outputs)

Experts rank deliverables without knowing which is human or AI-generated.

### Grading Output

- **Win**: Model deliverable preferred over human
- **Tie**: Deliverables judged equivalent
- **Loss**: Human deliverable preferred

### Evaluation Criteria

Experts consider both objective and subjective factors:

| Objective | Subjective |
|-----------|------------|
| Correctness | Structure |
| Accuracy | Style |
| Completeness | Format |
| Instruction following | Aesthetics |
| Calculation accuracy | Relevance |

### Grading Statistics

| Metric | Value |
|--------|-------|
| Average grading time per comparison | >1 hour |
| Samples per task per model | 3 |
| Graders per sample | 3 |
| Total comparisons per task per model | 9 |

### Blinding Limitations

Despite scrubbing filenames, stylistic tells may have revealed model origins:
- **OpenAI**: Often used em dashes
- **Claude**: Frequently adopted first-person phrasing
- **Grok**: Occasionally referred to itself as "Grok"

> Content/style not altered to preserve sample integrity.

---

## 2. Human Inter-Rater Agreement

### Measurement

For sample *s* with two human ratings H₁, H₂ ∈ {0, 0.5, 1}:

```
Agreement_HH = E[1 - |H₁ - H₂|]
```

Where:
- 1 = preference for model
- 0.5 = tie
- 0 = preference for human

### Results

| Metric | Agreement Rate |
|--------|----------------|
| **Human inter-rater agreement** | **70.8%** |
| Per-model range | 60-84% |

> Traditional reliability statistics (Cohen's κ, Fleiss' κ, Krippendorff's α) less applicable due to ordinal {0, 0.5, 1} output structure.

---

## 3. Automated Grader

### Design

GPT-5-high trained to perform pairwise comparisons mimicking industry professional experts.

### Performance

| Metric | Value |
|--------|-------|
| **Automated-Human Agreement** | **65.7%** |
| Human Inter-Rater Agreement | 70.8% |
| Gap | 5.1% |

### Agreement by Model (Automated vs Human)

| Model Evaluated | Automated-Human | Human-Human |
|-----------------|-----------------|-------------|
| GPT-4o | 84.5% | 84.2% |
| Gemini 2.5 Pro | 73.5% | 72.6% |
| Grok 4 | 69.2% | 71.4% |
| o4-mini high | 62.4% | 71.4% |
| Claude Opus 4.1 | 59.6% | 60.3% |
| o3 high | 56.0% | 69.0% |
| GPT-5 high | 55.3% | 66.2% |

### Known Bias

> Automated grader (GPT-5 based) shows **lower correlation with humans when assessing capable OpenAI models**—consistent with research showing models favor their own outputs (Panickssery et al., 2024).

Agreement highest for less capable models whose outputs are easier to distinguish from human deliverables.

---

## 4. Automated Grader Limitations

### Tasks Marked as Ungradable (12 of 220)

| Limitation | Description |
|------------|-------------|
| **Internet Access** | Tasks requiring online resources (e.g., finding/downloading music) |
| **Python-Only Container** | 3 Software Developer tasks requiring other languages + dependencies |
| **Font Packages** | Some human deliverables render differently without specific fonts |
| **Speech-to-Text** | Limited transcription for non-voice sounds |

### Technical Environment

Container runs **Python only** with limited external access.

---

## 5. Grader Container Packages

The automated grader has pre-installed packages for processing diverse file types:

### Core Data/ML
```
numpy, pandas, scipy, scikit-learn, torch, tensorflow, keras
xgboost, lightgbm, catboost, statsmodels, sympy
```

### Visualization
```
matplotlib, seaborn, plotly, bokeh, plotnine, graphviz
```

### Document Processing
```
python-docx, python-pptx, openpyxl, PyMuPDF, pdf2image
pdfplumber, reportlab, fpdf2, weasyprint, camelot-py
```

### Media Processing
```
Pillow, opencv-python, moviepy, ffmpeg-python
pydub, librosa, soundfile, mutagen
```

### Specialized
```
pytesseract (OCR), qrcode, cadquery (CAD)
rdkit (chemistry), biopython, spacy (NLP)
```

### Additional Packages

```
libreoffice          # Document rendering (critical for PDF generation)
aspose-words         # Word document processing
av                   # Audio/video container format handling
cadquery / cadquery-ocp  # CAD/3D modeling
pedalboard           # Audio effects
pyloudnorm           # Audio loudness normalization
```

---

## 6. Prompt for Agent Sampling

Key instructions given to models during evaluation:

### Character Handling
- Avoid U+2011 (use U+002D hyphen instead)
- Minimize emojis, nonstandard bullet points, special characters

### Document Creation
- Graphics must be legible (≥ half page width)
- Use LibreOffice for PDF creation (required for consistent rendering)
- Use cross-platform fonts (Noto Sans/Noto Serif recommended)
- Embed fonts if using non-standard options

### Mandatory Formatting Checks

```
STEP 1: Convert visual deliverables to PNGs using LibreOffice
STEP 2: Display PNGs and check for:
        - Text/graphics cut off or overlapping
        - Blank sections
        - Readability issues (dark on dark, light on light)
STEP 3: Programmatic checks for blank pages, overflow, page limits
STEP 4: Match deliverable sections to prompt instructions
STEP 5: Verify final files are exactly as intended
```

### Scaffolding Improvements

- Enabled GET requests in container
- Best-of-N sampling (N=4) with GPT-5 judge selection
