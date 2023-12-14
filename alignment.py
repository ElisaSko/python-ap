import sys
import re
seq=''
var=''
where='seq'

for line in sys.stdin :
    line=line.rstrip()
    if line =='' or line[0]==';':
        continue
    if where=='seq':
        if re.search('seq', line) :
            where='var'
        else:
            seq += line
    elif where=='var':
        if re.search('seq', line) :
            where='next'
        else:
            var += line
    elif where == 'next':
          print (f"'seq:'{seq} \n 'var:' {var}")
          seq=''
          var=''
          where = 'seq'