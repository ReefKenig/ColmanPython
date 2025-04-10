

def dnc(baseFunc, combineFunc):
    def helper(arr):
        if len(arr) == 1:
            return baseFunc(arr[0])
        mid = len(arr) // 2
        left = helper(arr[:mid])
        right = helper(arr[mid:])
        return combineFunc(left, right)
    return helper


def maxAreaHist(hist):
    def helper(left, right):
        if left == right:
            return hist[left]
        mid = (left + right) // 2
        left_area = helper(left, mid)
        right_area = helper(mid + 1, right)
        cross_area = maxCrossArea(left, mid, right)
        return max(left_area, right_area, cross_area)
    def maxCrossArea(left, mid, right):
        l = mid
        r = mid + 1
        min_height = min(hist[l], hist[r])
        max_area = min_height * 2
        while l > left or r < right:
            if l > left and (r == right or hist[l - 1] >= hist[r + 1]):
                l -= 1
                min_height = min(min_height, hist[l])
            else:
                r += 1
                min_height = min(min_height, hist[r])
            max_area = max(max_area, min_height * (r - l + 1))
        return max_area
    if not hist:
        return 0
    return helper(0, len(hist) - 1)

