def removeDuplicates(nums: list[int]) -> int:
    seen = []
    count = 0
    for n in nums:
        if n in seen:
            count += 1
            seen.remove(n)
        seen.append(n)
    return seen, count

print(removeDuplicates([0,0,1,1,1,2,2,3,3,4]))