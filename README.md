# CO2 Emissions Explorer

I put this together while studying environmental engineering to get a clearer 
picture of how CO2 emissions have actually changed since 1990 — not just for 
Germany but across some of the world's biggest emitters. The numbers are one 
thing, but seeing them visualized makes the differences a lot more striking.

Data comes from (https://github.com/owid/co2-data), which keeps a 
well-maintainedopen dataset on global emissions.

---

## What it shows

- How total emissions per country have changed from 1990 to 2022
- Who emits the most CO2 per person on average
- Whether higher GDP still correlates with higher emissions
- Which countries actually reduced emissions decade by decade — and which didn't

---

## How to run it

```bash
pip install pandas matplotlib numpy
python co2_explorer.py
```

Charts are saved automatically to an `output/` folder. The dataset is downloaded at runtime so no manual setup needed.

---

## Project structure

```
co2-emissions-explorer/
├── co2_explorer.py
├── README.md
└── output/
    ├── 01_trends.png
    ├── 02_per_capita.png
    ├── 03_co2_vs_gdp.png
    ├── 04_decade_heatmap.png
    └── summary.csv
```

---

Matin Bahadori
M.Sc. Umwelttechnik — BTU Cottbus-Senftenberg
