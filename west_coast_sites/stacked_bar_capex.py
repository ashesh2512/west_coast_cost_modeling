import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
plt.rcParams["font.family"] = "Times New Roman"

scenarios = (
    "Central CA\n (San Luis)",
    "Central CA\n (Long Beach)",
    "Central CA\n (Humboldt)",
    "Northern CA\n (Humboldt)",
    "Northern CA\n (San Luis)",
    "Southern OR\n (Coos Bay)",
    "Central OR\n (Coos Bay)",
    "Southern WA\n (Grays Harbor)",
)
capex = {
    "System CapEx": np.array([1659, 1659, 1659, 1524, 1524, 1524, 1466, 1605]),
    "Turbine CapEx": np.array([1306, 1306, 1306, 1306, 1306, 1306, 1306, 1306]),
    "Installation CapEx": np.array([393, 413, 429, 419, 538, 485, 386, 390]),
    "Soft CapEx": np.array([645, 645, 645, 645, 645, 645, 645, 645]),
}
width = 0.5

fig, ax = plt.subplots()
bottom = np.zeros(len(scenarios))

for capex_type, cost in capex.items():
    p = ax.bar(scenarios, cost, width, label=capex_type, bottom=bottom)
    bottom += cost

for c in ax.containers:

    # Optional: if the segment is small or 0, customize the labels
    labels = [v.get_height() if v.get_height() > 0 else '' for v in c]
    
    # remove the labels parameter if it's not needed for customized labels
    ax.bar_label(c, labels=labels, label_type='center')

ax.set_ylim([0, 6000])
ax.set_ylabel("$M")
ax.legend(loc="upper right")

plt.show()