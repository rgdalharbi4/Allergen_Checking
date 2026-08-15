<div align="center">

# 🥗 Allergen Detection from Product Ingredient Labels

### AI-powered food allergen detection from product ingredient labels

<br>

<div align="center">

<a href="https://allergenchecking-ajyk5cmt3w2obg6z9quhuk.streamlit.app">
  <img src="https://img.shields.io/badge/Live%20App-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white">
</a>

<img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white">

<a href="https://docs.ultralytics.com/models/yolov8/">
  <img src="https://img.shields.io/badge/YOLO-v8-00FFFF?style=for-the-badge">
</a>

<a href="https://universe.roboflow.com/raghad-alharbi/ingredient-label-detection-d4hgy/dataset/2">
  <img src="https://img.shields.io/badge/Roboflow-Dataset-6706CE?style=for-the-badge">
</a>

</div>
</div>

---

An AI-powered app that helps people with food allergies quickly check whether a supermarket product is safe for them — just by photographing it, instead of decoding a small, complex ingredient list.

---

## 🚨 Problem

Allergen information on food packaging is often written in dense scientific terms (e.g. "casein" instead of "milk") in small print, which is a major real-world cause of allergy incidents. The information exists — it's just hard to read and understand quickly, especially for parents of allergic children or elderly shoppers.

---

## ⚙️ How It Works (Pipeline)

<table>
<tr>
<td align="center"><b>📸 1. Capture</b></td>
<td align="center"><b>🎯 2. Locate</b></td>
<td align="center"><b>🔎 3. Read</b></td>
<td align="center"><b>🧠 4. Match</b></td>
<td align="center"><b>✅ 5. Result</b></td>
</tr>
</table>

1. **Capture** — user selects their allergy type(s) and photographs a product package
2. **Locate** — a custom-trained YOLOv8 object detection model finds the ingredient list region on the packaging (bilingual Arabic/English labels are detected as separate boxes when they appear in different areas)
3. **Read (OCR)** — the detected region is cropped from the original high-resolution image and passed to EasyOCR (Arabic + English) to extract the printed text
4. **Match** — the extracted text is checked against a bilingual allergen dictionary covering 13 major allergen categories, with fuzzy matching (via RapidFuzz) to tolerate minor OCR reading errors
5. **Result** — the user sees a direct answer: **Safe**, or **Warning** with the specific allergen(s) found

---

## 📦 Dataset

* **Classes (1):** `ingredient_label`
* **Source:** Combination of a public Roboflow dataset (385 images) and ~110 real product photos collected by the team, annotated in Roboflow
* **Why combine sources:** an initial model trained only on the public dataset scored very high on paper (~99.5% mAP) but performed poorly on real, self-photographed products — a classic overfitting/generalization gap. Adding real local product photos was necessary to make the model actually work in practice.
* **Hosted on Roboflow:** [ingredient-label-detection-d4hgy](https://universe.roboflow.com/raghad-alharbi/ingredient-label-detection-d4hgy/dataset/2)

Images are not stored in this repository (the dataset is large after augmentation). To download it:

```python
from roboflow import Roboflow
rf = Roboflow(api_key="YOUR_API_KEY")
project = rf.workspace("raghad-alharbi").project("ingredient-label-detection-d4hgy")
dataset = project.version(2).download("yolov8")
```

---

## 📊 Model & Results

**Architecture:** YOLOv8n (Ultralytics), standard object detection (not oriented/OBB, not segmentation)

Final model, evaluated on a held-out test set:

| Metric        |     Score |
| ------------- | --------: |
| **Precision** | **88.2%** |
| **Recall**    | **82.5%** |
| **mAP50**     | **85.8%** |
| **mAP50-95**  | **56.9%** |

We deliberately chose the higher-recall version of the model over an earlier, higher-precision version. For a safety-related allergy app, missing a real ingredient label (a false negative) is a more dangerous failure than an extra, imprecise detection — so recall was prioritized.

Validated on real product photos (e.g. a milk bottle with bilingual Arabic/English labeling), correctly detecting both the Arabic and English ingredient regions as separate boxes with high confidence (87% and 76% respectively).

---

## 🔎 OCR & Allergen Matching

After the ingredient label region is cropped, **EasyOCR** (configured for both Arabic and English) extracts the printed text. This text is then checked against a custom bilingual allergen dictionary.

**Allergen categories covered (13):** Milk, Egg, Peanut, Tree Nuts, Sesame, Gluten, Soy, Fish, Shellfish, Mustard, Celery, Sulphites, Corn — each mapped to its common scientific synonyms and derivative terms in both Arabic and English (e.g. milk → whey, casein, lactose, ghee, حليب, لبن, جبن...).

Matching uses **RapidFuzz** for fuzzy string comparison, so minor OCR misreads (a common issue with small print) don't cause a missed detection. Users can also type in a free-text allergen not covered by the 13 categories (e.g. strawberry), which is matched directly against the extracted text.

Example — end-to-end test on a real product photo:
```
Extracted text: "...Ingredients: Fresh Cow's Milk, Vitamin A, Vitamin D3..."
Allergy checked: milk
Result: {'safe': False, 'warnings': [{'allergy': 'milk', 'matched_term': 'milk'}]}
```

---

## 🛠️ Tech Stack

| Technology             | Usage                                                   |
| ---------------------- | ------------------------------------------------------- |
| **Roboflow**           | dataset annotation, versioning, augmentation            |
| **Ultralytics YOLOv8** | label region detection                                  |
| **Google Colab**       | model training (GPU)                                    |
| **EasyOCR**            | Arabic + English — text extraction                      |
| **RapidFuzz**          | fuzzy text matching for allergen detection               |
| **Python**             | allergen matching logic                                 |

---

## 🥜 Allergen Categories Covered

<div align="center">

`Milk`    `Egg`    `Peanut`    `Tree Nuts`    `Sesame`    `Gluten`    `Soy`

`Fish`    `Shellfish`    `Mustard`    `Celery`    `Sulphites`    `Corn`

</div>

---

## 👥 Team

**Data Science & AI Bootcamp**

---

<div align="center">

### 🌐 [Open the Streamlit App](https://allergenchecking-ajyk5cmt3w2obg6z9quhuk.streamlit.app)

</div>