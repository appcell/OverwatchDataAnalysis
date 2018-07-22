def hms_to_seconds(h, m, s):
    """
    Parse JSON file and return corresponding dict

    Author:
        Appcell

    Args:
        h: hours in int
        m: minutes in int
        s: seconds in float

    Returns:
        Time in seconds in float format

    """
    return float(h * 60 * 60 + m * 60 + s)