import random


def generate_sequential_workload(length=1000, page_count=50):
    """
    Generates a locality-heavy sequential workload.
    Pages are accessed in a repeating sequential pattern.
    """
    workload = []

    for i in range(length):
        workload.append(i % page_count)

    return workload


def generate_random_workload(length=1000, page_count=50):
    """
    Generates a random workload.
    """
    return [random.randint(0, page_count - 1) for _ in range(length)]


def generate_bursty_workload(length=1000, page_count=50):
    """
    Generates a bursty workload.
    A small group of pages is accessed repeatedly,
    then another group becomes active.
    """
    workload = []

    while len(workload) < length:
        start = random.randint(0, page_count - 10)
        burst_pages = list(range(start, start + 10))

        burst_length = random.randint(30, 70)

        for _ in range(burst_length):
            workload.append(random.choice(burst_pages))

            if len(workload) >= length:
                break

    return workload[:length]


def generate_shifted_workload(
    phase_length=1000,
    page_count=50
):
    """
    Required workload-shift experiment.

    Phase 1:
        Locality-heavy/sequential

    Phase 2:
        Random/bursty
    """

    phase1 = generate_sequential_workload(
        phase_length,
        page_count
    )

    phase2 = generate_random_workload(
        phase_length,
        page_count
    )

    return phase1 + phase2


if __name__ == "__main__":

    random.seed(42)

    workload = generate_shifted_workload(
        phase_length=1000,
        page_count=50
    )

    print("Total references:", len(workload))
    print("Phase 1 references:", len(workload[:1000]))
    print("Phase 2 references:", len(workload[1000:]))

    print("\nFirst 30 references:")
    print(workload[:30])

    print("\nReferences around workload shift:")
    print(workload[990:1010])
