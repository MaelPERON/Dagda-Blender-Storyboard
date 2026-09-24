def fit(value, old_min, old_max, new_min, new_max):
    t = (value - old_min) / (old_max - old_min)
    t = max(0.0, min(1.0, t))
    return new_min + t * (new_max - new_min)
