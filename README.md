# 🎨 Cartoon-Image-Converter

## 1. Project Overview

This project converts a given image into a **cartoon-style rendering** using classical image processing techniques implemented with OpenCV.

Unlike simple edge-overlay approaches, this pipeline focuses on:

* Color simplification (quantization)
* Robust edge extraction (internal gradient)
* Noise suppression via baseline filtering
* Direct edge-to-line mapping without contour reconstruction

The goal is to produce **clean, bold, and visually consistent cartoon-style images** while minimizing artifacts such as double edges and noisy contours.

---

## 2. Key Features

* Edge-preserving smoothing (Bilateral Filter)
* Color quantization using K-means clustering
* Internal gradient-based edge detection (reduces double edges)
* Baseline subtraction to remove weak edges
* Contrast enhancement for strong edge emphasis
* Direct line mask generation (no contour re-drawing)
* Final compositing via edge masking

---

## 3. Image Processing Pipeline

---

### Step 1. Grayscale Conversion & Preprocessing

* Convert image to grayscale
* Apply Gaussian blur to reduce noise

**Purpose**

* Stabilize edge detection
* Remove high-frequency noise

**Output**

![edge\_source](assets/edge_source.jpg)

---

### Step 2. Internal Gradient Computation

```python
grad = edge_src - erode(edge_src)
```

**Purpose**

* Extract edge intensity using internal gradient
* Reduce double-edge artifacts

**Output**

![internal\_gradient](assets/internal_gradient.jpg)

---

### Step 3. Weak Edge Removal (Baseline Subtraction)

```python
grad_cut = max(grad - baseline, 0)
```

**Purpose**

* Remove weak edges
* Preserve only strong structural edges

**Output**

![gradient\_cut](assets/gradient_cut.jpg)

---

### Step 4. Gradient Contrast Enhancement

```python
normalize → scale (alpha)
```

**Purpose**

* Amplify strong edges
* Improve edge-background separation

**Output**

![gradient\_emphasized](assets/gradient_emphasized.jpg)

---

### Step 5. Line Image Generation

```python
line_img = 255 - grad_emph
```

**Purpose**

* Convert gradient into black line mask
* Avoid contour reconstruction artifacts

**Output**

![line\_image](assets/line_image.jpg)

---

### Step 6. Color Quantization

* Apply K-means clustering to reduce colors

**Purpose**

* Create flat color regions
* Enhance cartoon-like appearance

---

### Step 7. Final Composition

```python
cartoon = color * line_mask
```

**Purpose**

* Overlay edges onto simplified color image
* Produce final cartoon rendering

**Output**

![cartoon](assets/cartoon.jpg)

---

## 4. Limitations

### ❌ 1. Low Contrast Images

* Weak gradients are not detected properly
* Results in missing edges

**Example**

![bad\_case](assets/bad_case.jpg)

---

### ❌ 2. High Texture / Noise Images

* Fine textures interpreted as edges
* Produces noisy and cluttered output

**Example**

![bad\_case2](assets/bad_case2.jpg)

---

### ❌ 3. Lighting Sensitivity

* Shadows and illumination changes affect gradient magnitude
* Leads to inconsistent edge extraction

---

### ❌ 4. Parameter Sensitivity

Key parameters significantly affect output quality:

* `baseline` → edge suppression strength
* `alpha` → contrast intensity
* `kernel size` → edge thickness
* `K` → level of color simplification

---

## 5. Discussion

This implementation improves upon naive cartoon rendering methods by:

* Eliminating contour reconstruction errors
* Reducing double-edge artifacts
* Explicitly filtering weak edges before enhancement

However, since it relies on heuristic image processing techniques, performance varies depending on image characteristics.

---

## 6. How to Run

```bash
python main.py
```

### Requirements

* Python 3.x
* OpenCV
* NumPy

---

## 7. Example Result

| Stage        | Image                        |
| ------------ | ---------------------------- |
| Edge Source  | assets/edge_source.jpg       |
| Gradient     | assets/internal_gradient.jpg |
| Final Output | assets/cartoon.jpg           |

---