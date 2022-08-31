import { HistogramData } from "./types";
const BAR_GAP = 2;

export function clamp(num: number, min: number, max: number) {
  return Math.min(Math.max(num, min), max);
}

export function drawHistogram(
  histogramData: HistogramData,
  canvas: HTMLCanvasElement,
  labelsDiv: Element,
  dark = false
) {
  const context = canvas.getContext("2d");
  if (!context) return;
  if (dark) context.fillStyle = "white";
  const { width, height } = canvas;
  labelsDiv.innerHTML = "";

  const numBuckets = histogramData.counts.length;
  const barWidth = width / numBuckets;
  const maxBucketCount = Math.max(...histogramData.counts);

  histogramData.counts.forEach((count, index) => {
    const barHeight = height * (count / maxBucketCount);
    const startX = index * barWidth;
    const startY = height - barHeight;

    context.beginPath();
    context.rect(startX + BAR_GAP, startY, barWidth - BAR_GAP, barHeight);
    context.fill();
  });

  const labels = histogramData.range;
  labels.forEach((barLabel) => {
    const label = document.createElement("p");
    label.innerHTML = `${barLabel}`;
    label.style.textAlign = "center";
    labelsDiv.appendChild(label);
  });
}

export function drawGradient(
  colorNodes: Array<Array<number>>,
  canvas: HTMLCanvasElement,
  fullRange: Array<number>
) {
  const context = canvas.getContext("2d");
  if (!context) return;
  const { width, height } = canvas;

  const gradient = context.createLinearGradient(0, 0, width, 0);
  colorNodes.forEach((node) => {
    const scalarValue = clamp(node[0], fullRange[0], fullRange[1]);
    const proportion =
      (scalarValue - fullRange[0]) / (fullRange[1] - fullRange[0]);
    const rgb = node.slice(1).map((value) => value * 255);
    gradient.addColorStop(proportion, `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`);
  });
  gradient.addColorStop(1, "white");

  context.fillStyle = gradient;
  context.fillRect(0, 0, width, height);
}
