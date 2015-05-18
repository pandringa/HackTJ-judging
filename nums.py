from random import shuffle
nums = []
for i in range(1,55):
	nums.append(i);
	nums.append(i);
	nums.append(i);

shuffle(nums)
print(nums)