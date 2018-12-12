

def _bucketify(currentNum, startNum, endNum, place, direction):
  if(direction == "raising"):
    # Check if reached top of search
    if( (currentNum +  10**(place)) > endNum ):
      # print("reached top of search, lowering started")
      direction = "lowering"
    # Check if place needs to be updated
    elif( currentNum % ( 10**(place+1) ) == 0 ):
      # print("Incrementing place")
      place+=1
    # Add Number to Retrieval List
    else:
      currentNum += 10**(place)
      print(currentNum)


  if(direction == "lowering"):
    # Check if adding pushes value beyond required endNum
    if( (currentNum +  10**(place)) > endNum ):
      # print("Decrementing place")
      place-=1
    # Add Number to Retrieval List
    else:
      currentNum += 10**(place)
      print(currentNum)

  return currentNum, place, direction




def bucketify(startNum, endNum):
  print("Bucketifying", startNum, "...", endNum)
  place = 0
  currentNum = startNum
  direction = "raising"
  print(currentNum)
  toRetrieve = [currentNum]
  while(currentNum != endNum):
    currentNum, place, direction= _bucketify(currentNum, startNum, endNum, place, direction)
    toRetrieve.append(currentNum)
  print(sorted(list(set(toRetrieve))))

  







bucketify(1518513475, 1518513532)