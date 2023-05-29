import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# plt.rcParams["font.family"] = "Times New Roman"
font = {'family' : 'Arial',
        'size'   : 10}
plt.rc('font', **font)

scenarios = (
    "Central CA\n (Central CA)",
    "Central CA\n (Southern CA)",
    "Central CA\n (Northern CA)",
    "Northern CA\n (Northern CA)",
    "Northern CA\n (Central CA)",
    "Southern OR\n (OR coast)",
    "Central OR\n (OR coast)",
    "Southern WA\n (WA coast)",
)
capex = {
    "Installation CapEx": np.divide(np.array([432, 461, 507, 501, 577, 561, 453, 467]), 1),
    "System CapEx": np.divide(np.array([1613, 1613, 1613, 1475, 1475, 1502, 1434, 1562]), 1),
    "Turbine CapEx": np.divide(np.array([1306, 1306, 1306, 1306, 1306, 1306, 1306, 1306]), 1),
    "Soft CapEx": np.divide(np.array([645, 645, 645, 645, 645, 645, 645, 645]), 1),
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

    labels = [f'{val:.0f}' for val in labels]
    
    # remove the labels parameter if it's not needed for customized labels
    ax.bar_label(c, labels=labels, label_type='center')

ax.set_ylim([0, 6000])
ax.set_ylabel("$/kW")
ax.legend(loc="upper right")

plt.show()