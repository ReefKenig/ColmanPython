def allSumsDP(arr):
    sums = set([0])
    for num in arr:
        new_sums = {s + num for s in sums}
        sums.update(new_sums)
    return set(sums)