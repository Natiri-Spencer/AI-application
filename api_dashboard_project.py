import json
raw_members = [
          {"name":"John Maikuva","steps":9009,"protocols":"OMAD","sleep":7.5,"cold shower":False},
          {"name":"Caren Natili","steps":10000,"protocols":"2MAD","sleep":7.5,"cold shower":True},
          {"name":"John Wawire","steps":10900,"protocols":"OMAD","sleep":8,"cold shower":True},
          {"name":"Benson Maikuva","steps":9000,"protocols":"2MAD","sleep":7.5,"cold shower":True},
          {"name":"Grace Omolo","steps":8900,"protocols":"OMAD","sleep":8,"cold shower":False},
          {"name":"Marcy Ochieng","steps":12000,"protocols":"OMAD","sleep":7.5,"cold shower":True},
          {"name":"Marion Otieno","steps":11500,"protocols":"2MAD","sleep":6,"cold shower":True},
          {"name":"Mercy Achieng","steps":12200,"protocols":"OMAD","sleep":6.5,"cold shower":False},
     ]
daily_steps = [50200, 64000, 58400, 84000, 54600, 78000, 65400]
daily_names= ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
skills_lists = [
     
            {"name": "Programming",  "instructor": "Eliud Jumba", "enrolled": 7},
            {"name": "Auditing",   "instructor": "Marcy Omondi",  "enrolled": 13},
            {"name": "copywriting", "instructor": "Forchieve Maikuva", "enrolled":20},
            {"name": "Goat breeding", "instructor": "Kelvin Wawire",  "enrolled": 10},
            {"name": "Poultry hutching",  "instructor": "Queenter Naliaka", "enrolled": 8}
               
]
#----process---
STEP_GOAL = 10000
goal_met = [m for m in raw_members if m["steps"] >= STEP_GOAL]
avg_steps = round(sum(m["steps"] for m in raw_members)/len(raw_members))
showers = sum([1 for m in raw_members if m['cold shower']])
best_day = daily_names[daily_steps.index(max(daily_steps))] #Returns day and highest step
top_skill = max(skills_lists, key=lambda m:m["enrolled"])

#Output
w=50
print("="*w) 
print("SMP COMMAND CENTER DASHBOARD | WEEK 5")
print("="*w)

print("\n SECTION 1:MEMBERS PERFOMANCE")
print(f" Total Members:{len(raw_members)}")
print(f"Hit {STEP_GOAL:,} step_goal:  {len(goal_met)}/{len(raw_members)}")
print(f"  {'Average steps:':<28} {avg_steps:,}")
print(f"{'Cold shower today:':<28} {showers}/{len(raw_members)}")
print(f"Goal hitters: {', '.join(m['name'] for m in goal_met)}")
#Section 2
print(f"\n SECTION 2: WEEKLY STEPS")
for day, total in zip(daily_names,daily_steps):
     bar = '#'*(total//5000)
     print(f" {day:4}{total:>7,} {bar}")
print(f"Best day:{best_day} ({max(daily_steps):,} total steps)")
print(f"Week average:{round(sum(daily_steps)/len(daily_steps)):,}  steps/day")

#Section 3
print(f"\n SECTION 3: SMP ACTIVE SKILLS")
for s in sorted(skills_lists, key=lambda x: -x["enrolled"]):
     print(f" | Instructor: {s['instructor']:15}  | {s['name']:15} | {s['enrolled']} enrolled")
print(f"Most popular: {top_skill['name']} {top_skill['enrolled']} enrolled")
print("="*w)

#export to json
export = {
     "week":5,
     "members":{"total":len(raw_members), "goal_met":len(goal_met),"Average steps":avg_steps},
     "weekly":{"best day": best_day, "total steps":sum(daily_steps)},
     "skills":{"active":len(skills_lists),"most popular":top_skill['name']}
}
print(f"\nJson Export:")
print(json.dumps(export, indent=2))