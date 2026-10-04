import random
import os
import pandas as pd
import matplotlib.pyplot as plt

from page_replacement import (
    fifo_page_replacement,
    lru_page_replacement,
    optimal_page_replacement
)

from workload_generator import (
    generate_sequential_workload,
    generate_random_workload,
    generate_bursty_workload,
    generate_shifted_workload
)

from adaptive_model import (
    AdaptivePageReplacement,
    learned_page_replacement
)


FRAME_COUNT = 10
PAGE_COUNT = 50
PHASE_LENGTH = 1000


def run_policy(policy_name, workload):

    if policy_name == "FIFO":
        return fifo_page_replacement(
            workload,
            FRAME_COUNT
        )

    if policy_name == "LRU":
        return lru_page_replacement(
            workload,
            FRAME_COUNT
        )

    if policy_name == "Optimal":
        return optimal_page_replacement(
            workload,
            FRAME_COUNT
        )


def main():

    random.seed(42)

    os.makedirs("results", exist_ok=True)

    # --------------------------------------------------
    # 1. Generate training data
    # --------------------------------------------------

    training_traces = []

    for _ in range(20):

        trace = generate_bursty_workload(
            length=500,
            page_count=PAGE_COUNT
        )

        training_traces.append(trace)

    # --------------------------------------------------
    # 2. Train adaptive model
    # --------------------------------------------------

    print("Training adaptive model...")

    model = AdaptivePageReplacement()

    model.train(
        training_traces,
        FRAME_COUNT
    )

    print("Adaptive model trained successfully.")

    # --------------------------------------------------
    # 3. Generate experimental workload
    # --------------------------------------------------

    phase1 = generate_sequential_workload(
        PHASE_LENGTH,
        PAGE_COUNT
    )

    phase2 = generate_random_workload(
        PHASE_LENGTH,
        PAGE_COUNT
    )

    complete_workload = phase1 + phase2

    # --------------------------------------------------
    # 4. Run classical algorithms
    # --------------------------------------------------

    policies = [
        "FIFO",
        "LRU",
        "Optimal"
    ]

    results = []

    for policy in policies:

        result_phase1 = run_policy(
            policy,
            phase1
        )

        result_phase2 = run_policy(
            policy,
            phase2
        )

        result_total = run_policy(
            policy,
            complete_workload
        )

        results.append({
            "Policy": policy,
            "Phase": "Before Shift",
            "Page Faults": result_phase1["page_faults"],
            "Page Hits": result_phase1["page_hits"],
            "Hit Ratio": result_phase1["hit_ratio"]
        })

        results.append({
            "Policy": policy,
            "Phase": "After Shift",
            "Page Faults": result_phase2["page_faults"],
            "Page Hits": result_phase2["page_hits"],
            "Hit Ratio": result_phase2["hit_ratio"]
        })

        results.append({
            "Policy": policy,
            "Phase": "Overall",
            "Page Faults": result_total["page_faults"],
            "Page Hits": result_total["page_hits"],
            "Hit Ratio": result_total["hit_ratio"]
        })

    # --------------------------------------------------
    # 5. Run learned approach
    # --------------------------------------------------

    learned_phase1 = learned_page_replacement(
        phase1,
        FRAME_COUNT,
        model
    )

    learned_phase2 = learned_page_replacement(
        phase2,
        FRAME_COUNT,
        model
    )

    learned_total = learned_page_replacement(
        complete_workload,
        FRAME_COUNT,
        model
    )

    results.append({
        "Policy": "Learned",
        "Phase": "Before Shift",
        "Page Faults": learned_phase1["page_faults"],
        "Page Hits": learned_phase1["page_hits"],
        "Hit Ratio": learned_phase1["hit_ratio"]
    })

    results.append({
        "Policy": "Learned",
        "Phase": "After Shift",
        "Page Faults": learned_phase2["page_faults"],
        "Page Hits": learned_phase2["page_hits"],
        "Hit Ratio": learned_phase2["hit_ratio"]
    })

    results.append({
        "Policy": "Learned",
        "Phase": "Overall",
        "Page Faults": learned_total["page_faults"],
        "Page Hits": learned_total["page_hits"],
        "Hit Ratio": learned_total["hit_ratio"]
    })

    # --------------------------------------------------
    # 6. Save results
    # --------------------------------------------------

    df = pd.DataFrame(results)

    df.to_csv(
        "results/page_replacement_results.csv",
        index=False
    )

    print("\n========== RESULTS ==========\n")

    print(df.to_string(index=False))

    # --------------------------------------------------
    # 7. Create graph
    # --------------------------------------------------

    plot_data = df[
        df["Phase"].isin(
            ["Before Shift", "After Shift"]
        )
    ]

    pivot = plot_data.pivot(
        index="Policy",
        columns="Phase",
        values="Hit Ratio"
    )

    pivot.plot(
        kind="bar",
        figsize=(9, 6)
    )

    plt.title(
        "Page Replacement Hit Ratio Before and After Workload Shift"
    )

    plt.ylabel("Hit Ratio")

    plt.xlabel("Policy")

    plt.xticks(rotation=0)

    plt.tight_layout()

    plt.savefig(
        "results/hit_ratio_comparison.png",
        dpi=300
    )

    plt.close()

    print("\nResults saved to:")
    print("results/page_replacement_results.csv")
    print("results/hit_ratio_comparison.png")


if __name__ == "__main__":
    main()

