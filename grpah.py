import pandas as pd
import matplotlib.pyplot as plt

# Load YOLO training results
df = pd.read_csv("runs/detect/train2/results.csv")

# Get last epoch metrics
precision = df['metrics/precision(B)'].iloc[-1]
recall = df['metrics/recall(B)'].iloc[-1]
map50 = df['metrics/mAP50(B)'].iloc[-1]

metrics = ['Precision','Recall','mAP50']
values = [precision*100, recall*100, map50*100]

plt.figure(figsize=(8,5))
bars = plt.bar(metrics, values)

for bar in bars:
    y=bar.get_height()
    plt.text(
        bar.get_x()+bar.get_width()/2,
        y+1,
        f'{y:.2f}',
        ha='center'
    )

plt.title('Project Performance Metrics')
plt.ylabel('Percentage')
plt.ylim(0,100)

plt.tight_layout()
plt.savefig('project_metrics_graph.png',dpi=300)
plt.show()