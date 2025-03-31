"""
    ChatGPT write it,
    in the there was not section about making tests, so made it simple like that.
    in real application i would implement pytest or unittests
"""

import requests

# BASE_URL = "http://localhost:8080"  # localhost
BASE_URL = "https://fast-simon-app.ew.r.appspot.com"  # PROD

# Define test sequences
test_sequences = [
    {
        "name": "Sequence 1",
        "steps": [
            ("set?name=ex&value=10", "ex=10"),
            ("get?name=ex", "10"),
            ("unset?name=ex", "ex=None"),
            ("get?name=ex", "None"),
            ("end", "CLEANED"),
        ],
    },
    {
        "name": "Sequence 2",
        "steps": [
            ("set?name=a&value=10", "a=10"),
            ("set?name=b&value=10", "b=10"),
            ("numequalto?value=10", "2"),
            ("numequalto?value=20", "0"),
            ("set?name=b&value=30", "b=30"),
            ("numequalto?value=10", "1"),
            ("end", "CLEANED"),
        ],
    },
    {
        "name": "Sequence 3",
        "steps": [
            ("set?name=a&value=10", "a=10"),
            ("set?name=b&value=20", "b=20"),
            ("get?name=a", "10"),
            ("get?name=b", "20"),
            ("undo", "b=None"),
            ("get?name=a", "10"),
            ("get?name=b", "None"),
            ("set?name=a&value=40", "a=40"),
            ("get?name=a", "40"),
            ("undo", "a=10"),
            ("get?name=a", "10"),
            ("undo", "a=None"),
            ("get?name=a", "None"),
            ("undo", "NO COMMANDS"),
            ("redo", "a=10"),
            ("redo", "a=40"),
            ("end", "CLEANED"),
        ],
    },
]

# Function to run tests
def run_tests():
    for sequence in test_sequences:
        print(f"\n🟢 Running {sequence['name']}...")

        for endpoint, expected_output in sequence["steps"]:
            url = f"{BASE_URL}/{endpoint}"
            response = requests.get(url)
            actual_output = response.text.strip()  # Clean up response

            if actual_output == expected_output:
                print(f"✅ {endpoint} -> {actual_output}")
            else:
                print(f"❌ {endpoint} -> Expected: {expected_output}, Got: {actual_output}")

# Run the test script
if __name__ == "__main__":
    run_tests()
