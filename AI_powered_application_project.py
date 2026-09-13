#Train the classifier
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
# 28-day SMP training data
# Features: [sleep_hr, water_glasses, bench_kg]
x = np.array([
    [6.5, 6, 80], [7.2, 8, 85], [5.8, 5, 75], [8.0, 10, 90],
    [7.5, 9, 88], [6.0, 6, 78], [7.8, 8, 86], [8.2, 10, 92],
    [5.5, 4, 70], [7.0, 7, 82], [6.8, 8, 84], [8.5, 11, 95],
    [7.3, 9, 89], [6.2, 6, 76], [7.9, 10, 91], [5.9, 5, 73],
    [8.1, 11, 93], [7.4, 8, 87], [6.7, 7, 83], [8.3, 10, 94],
    [5.6, 4, 71], [7.1, 8, 85], [8.0, 9, 90], [6.4, 6, 77],
    [7.6, 9, 88], [8.4, 11, 96], [6.3, 7, 79], [7.7, 10, 91]
])
# Labels: 1 = hit 10,000 steps, 0 = did not
y = np.array([0,1,0,1,1,0,1,1,0,1,1,1,1,0,1,0,1,1,0,1,0,1,1,0,1,1,0,1])
#split size 80/20
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2, random_state=42)
#train
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(x_train, y_train)


COACHING_TEMPLATES = {
    # key: (hit_goal, sleep_ok, water_ok)
    (True, True, True):  ("Strong inputs, strong output. Sleep and hydration are locked in.",
                          "Keep this baseline consistent and the steps will follow."),
    (True, True, False): ("You hit the goal despite low water. Sleep is your biggest lever.",
                          "Push hydration tomorrow and the margin grows."),
    (True, False, True): ("Water carried today's performance despite low sleep.",
                          "Shore up sleep tonight. Hitting goals on low sleep has hidden costs."),
    (True, False, False): ("Goal hit through willpower, not system. Willpower runs out.",
                           "Fix sleep and water before the next session."),
    (False, True, True): ("Inputs were solid but the goal was missed.",
                          "Audit what absorbed the energy. Do not cut sleep or water."),
    (False, True, False): ("Sleep is solid, hydration is low, goal was missed.",
                           "Add two glasses of water tomorrow. Hydration shifts step counts more than expected."),
    (False, False, True): ("Low sleep is the lead variable. Water is fine.",
                           "Get to bed 45 minutes earlier. The effect shows within 72 hours."),
    (False, False, False): ("Both inputs are below threshold and the goal was missed.",
                            "Reset tonight: 8 hours sleep minimum, 10 glasses water tomorrow."),
}

def get_coaching_message(sleep, water, hit_goal):
     """Simulate coaching. Real version calls OpenAI chat API"""
     key = (bool(hit_goal), sleep >= 7.0, water >= 8)
     line1, line2 = COACHING_TEMPLATES[key]
     return f"{line1} {line2}"
def analyze_day(sleep_hr,water_glasses, bench_kg, day_label=None):
     """Run the full pipeline: predict, score, coach."""
     features = np.array([[sleep_hr, water_glasses,bench_kg]])
     prediction = clf.predict(features)[0]
     proba = clf.predict_proba(features)[0]
     confidence = proba[prediction]
     coaching = get_coaching_message(sleep_hr, water_glasses, prediction)
     return {
        "label":         day_label or "Day",
        "sleep_hr":      sleep_hr,
        "water_glasses": water_glasses,
        "bench_kg":      bench_kg,
        "hit_goal":      bool(prediction),
        "confidence":    confidence,
        "coaching":      coaching,
    }
     
     

# Test the coaching layer directly

# --- Batch of incoming days ---
incoming_days = [
    ("Day 29", 8.0, 10, 92),
    ("Day 30", 5.5,  4, 70),
    ("Day 31", 7.2,  7, 84),
    ("Day 32", 8.5, 11, 95),
    ("Day 33", 6.1,  5, 76),
    ("Day 34", 7.8,  9, 88),
    ("Day 35", 5.9,  6, 73),
    ("Day 36",9.0, 9, 100)
]

#Process all days collect before printing
results = [analyze_day(sleep, water, bench, label)
           for label, sleep, water, bench, in incoming_days]

# --- Individual reports ---
SEP = "=" * 62
print(SEP)
print("    SMP PERFORMANCE COACH  |  DAILY REPORTS")
print(SEP)
for r in results:
     outcome = "HIT GOAL" if r['hit_goal'] else "MISS GOAL"
     print(f"\n{r['label']}")
     print(f"Outcome: {outcome} ({r['confidence']:.0%}) confidence")
     print(f"Inputs: sleep={r['sleep_hr']}h , water={r['water_glasses']}gl, bench={r['bench_kg']}kg")
     print(f"  Coach:    {r['coaching']}")


# --- Summary ---
print()
print(SEP)
print("    SUMMARY")
print(SEP)

total  = len(results)
hits   = sum(1 for r in results if r["hit_goal"])
misses = total - hits
avg_conf = np.mean([r["confidence"] for r in results])
hit_days = [r for r in results if r['hit_goal']]
missed_days = [r for r in results if not r['hit_goal']]

avg_sleep_hit = np.mean([r['sleep_hr'] for r in hit_days] if hit_days else 0)
avg_water_hit = np.mean([r['water_glasses'] for r in hit_days] if hit_days else 0)
avg_sleep_miss = np.mean([r['sleep_hr'] for r in missed_days] if missed_days else 0)
avg_water_miss = np.mean([r['water_glasses'] for r in missed_days] if missed_days else 0)

print()
print(f" Days Analyzed: {total}")
print(f"Goal hit: {hits}/{total}({hits/total:.0%})")
print(f"Goals missed: {misses}/{total}({misses/total:.0%})")
print(f"  Avg confidence:   {avg_conf:.0%}")
print()
print("  On HIT days:")
print(f"    avg sleep:  {avg_sleep_hit:.1f}h  |  avg water: {avg_water_hit:.1f} glasses")
print()
print("  On MISS days:")
print(f"    avg sleep:  {avg_sleep_miss:.1f}h  |  avg water: {avg_water_miss:.1f} glasses")
print()
sleep_diff = avg_sleep_hit - avg_sleep_miss
water_diff = avg_water_hit - avg_water_miss
print(f"  HIT days averaged {sleep_diff:+.1f}h more sleep and {water_diff:+.1f} more glasses of water")
print()
print(SEP)
print("    End of report")
print(SEP)