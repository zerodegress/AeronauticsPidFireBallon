#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

import matplotlib.pyplot as plt


def load_series(path: Path) -> list[float]:
    text = path.read_text(encoding="utf-8")

    # First try strict JSON.
    try:
        data = json.loads(text)
        if not isinstance(data, list):
            raise ValueError("data.json 顶层不是数组")
        return [float(x) for x in data]
    except Exception:
        # Fallback for relaxed formats such as trailing comma.
        nums = re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", text)
        if not nums:
            raise ValueError("未从 data.json 读取到任何数值")
        return [float(x) for x in nums]


def plot_response(values: list[float], out_path: Path, show: bool, sea_level: float) -> None:
    x = list(range(len(values)))

    plt.figure(figsize=(10, 4.8), dpi=120)
    plt.plot(x, values, linewidth=1.6, color="#1f77b4", label="Response")
    plt.axhline(y=sea_level, color="#2ca02c", linestyle=":", linewidth=1.2, label=f"Sea Level ({sea_level:g})")
    plt.title("Response Curve")
    plt.xlabel("Sample Index")
    plt.ylabel("Value")
    plt.ylim(bottom=sea_level)
    plt.grid(True, linestyle="--", alpha=0.35)
    plt.legend()
    plt.tight_layout()

    plt.savefig(out_path, bbox_inches="tight")
    print(f"图像已保存: {out_path}")

    if show:
        plt.show()
    else:
        plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="根据 data.json 绘制响应曲线")
    parser.add_argument("-i", "--input", default="data.json", help="输入数据文件路径")
    parser.add_argument("-o", "--output", default="response_curve.png", help="输出图像路径")
    parser.add_argument("--sea-level", type=float, default=63.0, help="MC 海平面高度（默认 63）")
    parser.add_argument("--show", action="store_true", help="绘图后弹窗显示")
    args = parser.parse_args()

    values = load_series(Path(args.input))
    if len(values) == 0:
        raise ValueError("数据为空，无法绘图")

    plot_response(values, Path(args.output), args.show, args.sea_level)


if __name__ == "__main__":
    main()
