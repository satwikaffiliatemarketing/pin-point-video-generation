
from game_player import play_pinpoint
import os

# Mock data based on observed clue 'Canned beverages'
data = {
    "answer": "SODA",
    "clues": ["Canned beverages"],
    "plausible_guesses": ["POP", "COLA", "BEER", "SELTZER"]
}

output_video = "demo_gameplay.webm"

print(f"Running demo gameplay with expected answer: {data['answer']}")
play_pinpoint(data, output_video)

if os.path.exists(output_video):
    print(f"SUCCESS: Video generated at {output_video}")
else:
    print("FAILURE: No video generated.")
