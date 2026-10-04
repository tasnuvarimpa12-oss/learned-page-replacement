from collections import OrderedDict


def fifo_page_replacement(reference_string, frame_count):
    frames = []
    pointer = 0
    page_faults = 0
    page_hits = 0

    for page in reference_string:
        if page in frames:
            page_hits += 1
        else:
            page_faults += 1

            if len(frames) < frame_count:
                frames.append(page)
            else:
                frames[pointer] = page
                pointer = (pointer + 1) % frame_count

    total = page_hits + page_faults
    hit_ratio = page_hits / total if total > 0 else 0

    return {
        "page_faults": page_faults,
        "page_hits": page_hits,
        "hit_ratio": hit_ratio
    }


def lru_page_replacement(reference_string, frame_count):
    frames = OrderedDict()
    page_faults = 0
    page_hits = 0

    for page in reference_string:
        if page in frames:
            page_hits += 1
            frames.move_to_end(page)
        else:
            page_faults += 1

            if len(frames) >= frame_count:
                frames.popitem(last=False)

            frames[page] = True

    total = page_hits + page_faults
    hit_ratio = page_hits / total if total > 0 else 0

    return {
        "page_faults": page_faults,
        "page_hits": page_hits,
        "hit_ratio": hit_ratio
    }


def optimal_page_replacement(reference_string, frame_count):
    frames = []
    page_faults = 0
    page_hits = 0

    for i, page in enumerate(reference_string):

        if page in frames:
            page_hits += 1
            continue

        page_faults += 1

        if len(frames) < frame_count:
            frames.append(page)
            continue

        future_pages = reference_string[i + 1:]

        farthest_page = None
        farthest_distance = -1

        for frame_page in frames:

            if frame_page not in future_pages:
                farthest_page = frame_page
                break

            distance = future_pages.index(frame_page)

            if distance > farthest_distance:
                farthest_distance = distance
                farthest_page = frame_page

        frames[frames.index(farthest_page)] = page

    total = page_hits + page_faults
    hit_ratio = page_hits / total if total > 0 else 0

    return {
        "page_faults": page_faults,
        "page_hits": page_hits,
        "hit_ratio": hit_ratio
    }


if __name__ == "__main__":

    # Small test reference string
    reference_string = [
        1, 2, 3, 1, 4, 5, 2, 1,
        2, 3, 4, 5, 1, 2, 3, 4
    ]

    frame_count = 3

    fifo_result = fifo_page_replacement(
        reference_string,
        frame_count
    )

    lru_result = lru_page_replacement(
        reference_string,
        frame_count
    )

    optimal_result = optimal_page_replacement(
        reference_string,
        frame_count
    )

    print("Reference String:")
    print(reference_string)

    print("\nNumber of Frames:", frame_count)

    print("\nFIFO:")
    print(fifo_result)

    print("\nLRU:")
    print(lru_result)

    print("\nOptimal:")
    print(optimal_result)

