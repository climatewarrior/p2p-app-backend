#!/usr/bin/python
with open("findOid.log") as f:
        content = f.readlines()

output =""

for line in content:
    index = line.find("$oid") + 8
    output += line[index: index + 24] + "\t"


print output
