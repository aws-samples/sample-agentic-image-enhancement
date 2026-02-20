"""Visualization utilities for image display and comparison."""

from typing import Tuple
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
import numpy as np
from tools.enhancement_tools import analyze_image


class VisualizationUtilities:

    @staticmethod
    def show_image(
        image: np.ndarray, title: str = "", figsize: Tuple = (10, 8)
    ) -> None:
        """Display a single image with optional title."""
        fig, ax = plt.subplots(1, 1, figsize=figsize)
        ax.imshow(image)
        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.axis("off")
        plt.tight_layout()
        plt.show()

    @staticmethod
    def show_comparison(
        original: np.ndarray,
        enhanced: np.ndarray,
        title: str = "Original vs Enhanced",
        metrics: bool = True,
    ) -> None:
        """
        Side-by-side comparison with optional quality metrics.

        Shows both images at equal size with metric annotations
        beneath each for quick quantitative comparison.
        """
        fig = plt.figure(figsize=(18, 10))
        gs = GridSpec(2, 2, height_ratios=[5, 1], hspace=0.3)

        # ── Images ──
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.imshow(original)
        ax1.set_title("Original", fontsize=14, fontweight="bold")
        ax1.axis("off")

        ax2 = fig.add_subplot(gs[0, 1])
        ax2.imshow(enhanced)
        ax2.set_title("Enhanced", fontsize=14, fontweight="bold")
        ax2.axis("off")

        # ── Metrics (if requested) ──
        if metrics:
            orig_metrics = analyze_image(original)
            enh_metrics = analyze_image(enhanced)

            def format_metrics(m: dict) -> str:
                return (
                    f"Contrast: {m['contrast_std']:.1f}  |  "
                    f"Sharpness: {m['sharpness_laplacian']:.0f}  |  "
                    f"Brightness: {m['mean_brightness']:.0f}  |  "
                    f"Yellowing: {m['yellowing_index']:.3f}"
                )

            ax3 = fig.add_subplot(gs[1, 0])
            ax3.text(
                0.5,
                0.5,
                format_metrics(orig_metrics),
                ha="center",
                va="center",
                fontsize=11,
                family="monospace",
                bbox=dict(boxstyle="round,pad=0.5", facecolor="#f0f0f0"),
            )
            ax3.axis("off")

            ax4 = fig.add_subplot(gs[1, 1])
            ax4.text(
                0.5,
                0.5,
                format_metrics(enh_metrics),
                ha="center",
                va="center",
                fontsize=11,
                family="monospace",
                bbox=dict(boxstyle="round,pad=0.5", facecolor="#e8f5e9"),
            )
            ax4.axis("off")

        fig.suptitle(title, fontsize=16, fontweight="bold", y=0.98)
        plt.show()

    @staticmethod
    def show_operations_log(operations: list) -> None:
        """Pretty-print the operations that were applied."""
        print("\n┌─ Operations Applied ─────────────────────────┐")
        for i, op in enumerate(operations, 1):
            region_str = ""
            if op.region and not op.region.is_full_image():
                r = op.region
                region_str = (
                    f" [region: ({r.x1:.1f},{r.y1:.1f})-({r.x2:.1f},{r.y2:.1f})]"
                )
            print(
                f"│ {i}. {op.operation:20s} intensity={op.parameters['intensity']:.2f}{region_str}"
            )
        print("└──────────────────────────────────────────────┘")
