
def mString(number, M):
    return format(number, "b").zfill(M)

def getReconstructionValue(index, delta):
    return ((2 * index - 1) / 2) * delta