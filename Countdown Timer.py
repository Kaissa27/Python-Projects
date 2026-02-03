# Countdown Timer

for variable in range(start, stop, step):
  # Code to repeat

for i in range(5, 0, -1):
  print(i)

while condition:
  # Code to repeat

count = 0
while count < 5:
  print(count)

import time

for i in range(10, 0, -2):
  print(i)
  time.sleep(2)
print("Happy New Year!")

# Countdown Timer

import time

# Step 1: Get user input for countdown start
start = int(input("Enter the number to start the countdown from: "))

# Step 2: Countdown using a while loop
print("\n--- Countdown Begins ---")
while start > 0:
  print(start)
  time.sleep(1)
  start -= 1

# Step 3: Print final message
print("Countdown Complete!")