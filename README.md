# 📊 DataFut | Impact Analysis of Neymar on Brazil National Team Performance (2010+)

## 🎯 Objective

This project investigates the statistical impact of Neymar on the Brazil National Team performance in official matches since 2010.

The goal is to compare team performance in games **with** and **without** Neymar, using structured data analysis instead of opinion-based debate.

---

## 🔎 Methodology

- Historical dataset of international matches
- Filtering for official matches only (excluding friendlies)
- Data cleaning and normalization
- Cross-source date reconciliation (±1 day tolerance)
- Creation of performance metrics (win rate, goals, etc.)
- Balanced sample comparison

All preprocessing and transformations were performed using Python and Pandas.

---

## 📈 Key Findings

- **70.69% win rate with Neymar** (58 official matches)
- **47.06% win rate without Neymar** (51 official matches)
- **+23 percentage point difference**

The sample sizes are balanced, strengthening the comparison reliability.

---

## 📌 Insights

The data suggests a significant performance gap in official competitions when Neymar is on the field.

While correlation does not necessarily imply causation, the statistical difference (+23 p.p.) indicates measurable impact on team results.

This project demonstrates how data analysis can elevate sports discussions beyond subjective opinions.

---

## 🛠️ Tech Stack

- Python
- Pandas
- Streamlit
- Plotly

---

## 🚀 How to Run Locally

Install dependencies:

```bash
pip install -r requirements.txt

Run the interactive dashboard:
streamlit run app.py

📊 Dashboard Preview
[Dashboard Preview](dashboard.png)

📌 Author

Fernando Ferreira Alves
DataFut Project