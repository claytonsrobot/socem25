import numpy as np

def generate_mock_data(duration=10, frequency=20):
    """
    Generate a synthetic 3-peak force curve for testing.
    
    Args:
        duration (int): Total time in seconds.
        frequency (int): Samples per second.

    Returns:
        Tuple[List[float], List[float], List[float]]: elapsed time, distance, force
    """
    t = np.linspace(0, duration, duration * frequency)
    # Simulate distance linearly increasing
    distance = 5 * t / duration

    # Create three Gaussian peaks on the curve
    peak1 = np.exp(-((t - duration * 0.25) ** 2) / 0.1)
    peak2 = np.exp(-((t - duration * 0.5) ** 2) / 0.1)
    peak3 = np.exp(-((t - duration * 0.75) ** 2) / 0.1)

    # Simulate some noise
    force = (peak1 + 1.5 * peak2 + peak3) * 5 + np.random.normal(0, 0.2, len(t))

    return t.tolist(), distance.tolist(), force.tolist()
