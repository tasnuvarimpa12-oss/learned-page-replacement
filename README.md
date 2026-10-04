# Learned Page Replacement

## CSE-307 Operating Systems Term Paper

### Project Overview

This project studies classical page replacement algorithms under a changing memory-access workload.

The implemented classical algorithms are:

- FIFO
- LRU
- Optimal (Belady's Algorithm)

A lightweight Decision Tree based adaptive component is also implemented. It uses features such as page access frequency and recency to predict an eviction candidate.

The main experiment contains a deliberate workload shift:

1. Phase 1 - sequential/locality-based access pattern
2. Phase 2 - random access pattern

The performance of the classical algorithms and the learned approach is compared before and after the workload shift.

---

## Project Structure

```text
learned-page-replacement/
│
├── src/
│   ├── page_replacement.py
│   ├── workload_generator.py
│   ├── adaptive_model.py
│   └── experiment.py
│
├── results/
│   ├── page_replacement_results.csv
│   └── hit_ratio_comparison.png
│
├── README.md
└── requirements.txt
