sudo ./addKarenQs.sh > testOutput.log

cat testOutput.log |grep uri > findOid.log

#python << END
#!/usr/bin/python
#with open("findOid.log") as f:
#    content = f.readlines()
#
#    output =""
#
#    for line in content:
#        index = line.find("$oid") + 8
#        output += line[index: index + 24] + "\t"
#    print output
#END

#arr=(`cat testOutput.log | grep uri`)
#echo $RESULT | cut -d '$' -f 1

#for mLine in `grep -n '$oid' "$RESULT"`
#do
#      echo 'mLine = '${mLine}
#      python << END
#      END
#done

