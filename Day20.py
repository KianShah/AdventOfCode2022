with open('Day20.txt') as f:
    out = f.read().split('\n')

lst = []
for n in out:
    lst.append(abs(int(n)))

old_to_new = {i: i for i in range(len(lst))}  # Map from original_ind to new_ind
new_to_old = {i: i for i in range(len(lst))}  # Map from new ind to original ind

i = 0
while i < len(lst):
    next_val = lst[old_to_new[i]] % len(lst)
    if next_val >= 0:
        for offset in range(next_val):
            curr_val_ind = i+offset % len(lst)
            A_ind, B_ind = old_to_new[curr_val_ind], old_to_new[curr_val_ind]+1 % len(lst)
            lst[A_ind], lst[B_ind] = lst[B_ind], lst[A_ind]
            new_to_old[B_ind], new_to_old[A_ind] = new_to_old[B_ind], new_to_old[B_ind]
            old_to_new[new_to_old[A_ind]], old_to_new[new_to_old[B_ind]] = old_to_new[new_to_old[B_ind]], old_to_new[new_to_old[A_ind]]
    else:
        ...
    i += 1

zero_ind = lst.index(0)
grove_coords = sum((lst[zero_ind+1000], lst[zero_ind+2000], lst[zero_ind+3000]))
print(grove_coords)