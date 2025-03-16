import argparse
from zxcvbn import zxcvbn

def format_time(seconds):
    """
    Converts seconds to a human-readable string with years, days, hours, minutes, and seconds.
    """
    intervals = (
        ('years', 31536000),
        ('days', 86400),
        ('hours', 3600),
        ('minutes', 60),
        ('seconds', 1)
    )
    result = []
    for name, count in intervals:
        value = int(seconds // count)
        if value:
            result.append(f"{value} {name}")
            seconds -= value * count
    return ', '.join(result) if result else "0 seconds"

def main():
    parser = argparse.ArgumentParser(
        description="Test password strength using zxcvbn and display human-readable crack times."
    )
    parser.add_argument(
        "password", 
        help="The password to evaluate. If your password contains spaces, enclose it in quotes."
    )
    args = parser.parse_args()

    # Evaluate the password using zxcvbn
    result = zxcvbn(args.password)

    # Display basic results
    print("Password:", args.password)
    print("Score (0 to 4):", result['score'])
    print("Estimated guesses:", result['guesses'])
    print("Estimated entropy (bits):", result.get('entropy', 'N/A'))

    # Display estimated crack times in human-readable format
    print("\nEstimated crack times:")
    for method, seconds in result['crack_times_seconds'].items():
        human_readable = format_time(seconds)
        print(f"  {method}: {human_readable}")

    # Display user feedback if any
    print("\nFeedback:")
    feedback = result.get('feedback', {})
    warning = feedback.get('warning')
    suggestions = feedback.get('suggestions', [])
    if warning:
        print("  Warning:", warning)
    if suggestions:
        for suggestion in suggestions:
            print("  Suggestion:", suggestion)
    if not warning and not suggestions:
        print("  No suggestions, good job!")

if __name__ == '__main__':
    main()
