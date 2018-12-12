PLACES = [10**unit for unit in range(1, 10)]


cache = {}
cache2 = {}
bucketsToUpdate = set()


def _getBucketsToUpdate(number):
  buckets = []
  for place in PLACES:
    bucket = int(number / place) * place
    if bucket == 0:
      break
    buckets.append(int(number / place) * place)
  return set(buckets)
  

def _getBucketsToUpdate2(number):
  buckets = []
  cacheMissPositions = {}
  for indx, place in enumerate(PLACES):
    bucket = int(number / place) * place
    cachekey = str(bucket)

    if(bucket != 0):
      # print("appending", bucket)
      buckets.append(bucket)


    if(cachekey in cache2.keys() and cache2[cachekey] != None):
      # print("Cache hit", bucket)
      allBuckets = buckets + sorted(cache2[cachekey])
      for bucket in cacheMissPositions.keys():
        cache2[bucket] = set(allBuckets[cacheMissPositions[bucket]:])
        # print("Cache", bucket , cache2[bucket], allBuckets)

      return set(allBuckets)
    else:
      cacheMissPositions[str(bucket)] = indx

    if(bucket == 0 or place == PLACES[-1]):
      # print("Scan End, Caching intermideiates")
      # cache everything
      for bucket in cacheMissPositions.keys():
        cache2[bucket] = set(buckets[cacheMissPositions[bucket]:])
        # print("Cache", bucket , cache2[bucket])
      break

    
    
  # print("asdsad")
  return set(buckets)



def _getHigherBuckets(number, place=1, startingPlace = 1):
  if(number == 0):
    return set()

  cachekey = str(number)+"_"+str(place)
  if(cachekey in cache.keys() and cache[cachekey] != None):
    # print("cache hit for", number)
    return cache[cachekey]
  
  cache[cachekey] = set()
  
  unit = 10**place
  higherBuckets = _getHigherBuckets(int(number / (10**place))*(10**place), place+1, startingPlace)
  
  if(place != startingPlace):
    cache[cachekey] = higherBuckets.union(set([number]))
  else:
    cache[cachekey] = higherBuckets
  
  return cache[cachekey]
  
  # bucket = int(number / unit) * unit
  # if bucket == 0:
  #   return None
  # else:

  #   return localBuckets
  
  # set.add()
  # print(int(number / place) * place)
  


# def bucketify(startNum, endNum):
#   print("Bucketifying", startNum, "...", endNum)
#   place = 0
#   currentNum = startNum
#   direction = "raising"
#   print(currentNum)
#   toRetrieve = [currentNum]
#   while(currentNum != endNum):
#     currentNum, place, direction= _bucketify(currentNum, startNum, endNum, place, direction)
#     toRetrieve.append(currentNum)
#   print(sorted(list(set(toRetrieve))))

  
import time

# print(323166712-322136123)
# start = time.time()
# for i in range(323036123, 323166712):
#   _getBucketsToUpdate(i)
# end = time.time()
# print("Time Taken:", end-start)
# print("...........................")

start = time.time()
allUpdates = set()
for i in range(323036123, 323036123+2592000):
  for val in _getBucketsToUpdate2(i):
    allUpdates.add(val)
  # allUpdates = allUpdates.union(_getBucketsToUpdate2(i))
end = time.time()
print("Time Taken:", end-start)
print("Total Updates:",  len(allUpdates))
print("...........................")


# start = time.time()
# for i in range(323036123, 323166712):
#   _getHigherBuckets(i)
# end = time.time()
# print("Time Taken:", end-start)
# # bucketify(1518513475, 1518513532)

#  PROOF

# start = time.time()
# for i in range(322136123, 323166712):
#   assert (sorted(_getBucketsToUpdate2(i)) == sorted(_getBucketsToUpdate(i)))
# end = time.time()
# print("Time Taken:", end-start)
# print("...........................")
