def generate(n, x):
  # To generate cylic sub-groups using the generator
  # [d] in the subgroup <[x]> of Z_n.
  group = []
  
  curr = x%n # curr is always mod n
  while True:
    curr = (curr+x)%n # next cylic element
    if curr in group:
      # reached cycle
      break

    group.append(curr) 
  return group




if __name__ == "__main__":
  group = generate(n=50, x=20)
  print("Cyclic SubGroup: ")
  print(group)

  print("Smallest Generator [d]: ")
  if 0 in group:
    group.remove(0)
  print(f'[{min(group)}]')
