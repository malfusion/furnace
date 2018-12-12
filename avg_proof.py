import numpy as np
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def case1(arr):
  # Case 1: Use the accumulated average (pixel wise) and cut out required portion, then bind range to min and max.
  total = np.zeros((100,100))

  for n in range(arr.shape[2]):
    for i in range(100):
      for j in range(100):
        total[i][j] += arr[i,j,n]

  #Accumulated average
  total = total/arr.shape[2]
  cutout1 = total[20:40, 20:40]
  cutout1max = (cutout1.max())
  cutout1min = (cutout1.min())
  cutout1 = (cutout1 - cutout1min) / (cutout1max-cutout1min)
  cutout1 = np.floor(cutout1 * 255)
  # print(cutout1)
  # print(cutout1.shape)
  return cutout1

def case2(arr):
  
  # Case 2: Use the accumulated average (pixel wise) for the required pixels, then bind range to min and max.
  total = np.zeros((20,20))

  for n in range(arr.shape[2]):
    for i in range(20,40):
      for j in range(20,40):
        total[i-20][j-20] += arr[i,j,n]

  cutout2 = total/arr.shape[2]
  cutout2max = (cutout2.max())
  cutout2min = (cutout2.min())
  cutout2 = (cutout2 - cutout2min) / (cutout2max-cutout2min)
  cutout2 = np.floor(cutout2 * 255)
  # print(cutout2)
  # print(cutout2.shape)
  return cutout2

if __name__ == "__main__":
  arr = np.random.randint(0,100, (100,100,10))
  cutout1 = case1(arr)
  cutout2 = case2(arr)
  if(np.array_equal(cutout1, cutout2)):
    print(bcolors.OKGREEN + "Proof is accurate, sustainable and final." + bcolors.ENDC)
  else:
    print(bcolors.FAIL + "Proof Failed." + bcolors.ENDC)

# Result: As long as we are precomputong "PIXEL WISE AVERAGES" between frames, nothing will be disrupted. We only need to compute cutout and binding at runtime.

# Method:
# 1. Store 10MA, 100MA, 1000MA, etc
# 2. On demand, get the appropriate intervals and calculate accurate average
# 3. On the result, perform the cutout and then perform binding to min-max range
# 4. We might need to maintain floating point averages in order to avoid losing too much precision.






