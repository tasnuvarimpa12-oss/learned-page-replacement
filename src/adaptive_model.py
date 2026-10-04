from collections import Counter
from sklearn.tree import DecisionTreeClassifier


class AdaptivePageReplacement:
    """
    Learned page replacement policy.

    The model learns to identify which page should be
    evicted using:
        - recency
        - access frequency
        - normalized age
    """

    def __init__(self):
        self.model = DecisionTreeClassifier(
            max_depth=5,
            random_state=42
        )
        self.is_trained = False

    def _features(self, page, cache, history, current_index):
        frequency = history[:current_index].count(page)

        positions = [
            i for i, p in enumerate(history[:current_index])
            if p == page
        ]

        if positions:
            last_used = positions[-1]
            recency = current_index - last_used
        else:
            recency = current_index + 1

        age = recency / max(current_index + 1, 1)

        return [
            frequency,
            recency,
            age
        ]

    def train(self, training_traces, frame_count):
        X = []
        y = []

        for trace in training_traces:

            cache = []

            for i, page in enumerate(trace):

                if page in cache:
                    continue

                if len(cache) < frame_count:
                    cache.append(page)
                    continue

                # Find the optimal victim using future knowledge.
                future = trace[i + 1:]

                victim = None
                farthest = -1

                for candidate in cache:

                    if candidate not in future:
                        victim = candidate
                        break

                    distance = future.index(candidate)

                    if distance > farthest:
                        farthest = distance
                        victim = candidate

                # Generate training samples.
                for candidate in cache:

                    features = self._features(
                        candidate,
                        cache,
                        trace,
                        i
                    )

                    X.append(features)

                    if candidate == victim:
                        y.append(1)
                    else:
                        y.append(0)

                cache[cache.index(victim)] = page

        self.model.fit(X, y)
        self.is_trained = True

    def choose_victim(self, cache, history, current_index):
        if not cache:
            return None

        if not self.is_trained:
            raise RuntimeError("Model has not been trained.")

        candidates = []

        for page in cache:

            features = self._features(
                page,
                cache,
                history,
                current_index
            )

            probability = self.model.predict_proba(
                [features]
            )[0]

            if len(probability) == 2:
                victim_probability = probability[1]
            else:
                victim_probability = 0

            candidates.append(
                (victim_probability, page)
            )

        # Highest probability = predicted eviction candidate
        candidates.sort(
            key=lambda x: x[0],
            reverse=True
        )

        return candidates[0][1]


def learned_page_replacement(
    reference_string,
    frame_count,
    model
):
    cache = []

    page_faults = 0
    page_hits = 0

    for i, page in enumerate(reference_string):

        if page in cache:
            page_hits += 1
            continue

        page_faults += 1

        if len(cache) < frame_count:
            cache.append(page)
        else:
            victim = model.choose_victim(
                cache,
                reference_string,
                i
            )

            cache[cache.index(victim)] = page

    total = page_hits + page_faults

    hit_ratio = (
        page_hits / total
        if total > 0
        else 0
    )

    return {
        "page_faults": page_faults,
        "page_hits": page_hits,
        "hit_ratio": hit_ratio
    }
