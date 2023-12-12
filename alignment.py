import sys
for line in sys.stdin :
    line=line.rstrip()
    if line=='':
        continue
    elif line[0]==';':
        continue
    print(line)