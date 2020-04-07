#!/bin/bash
egrep '^1((10*1)|(01*0))*10*$' p1.txt > output1.txt

egrep '(^|.*\s)(red\s([0-9a-zA-Z]*\s){0,2}pick-?up\struck|pick-?up\struck\s([0-9a-zA-Z]*\s){0,2}red).*\$[0-9].*' p2.txt > output2.txt

egrep '(^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[012])-(19|20)\d\d$)|(^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.(19|20)\d\d$)|(^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/(19|20)\d\d$)|(^(0[1-9]|[12][0-9]|3[01])-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-(19|20)\d\d$)|(^(0[1-9]|[12][0-9]|3[01])\.(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.(19|20)\d\d$)|(^(0[1-9]|[12][0-9]|3[01])/(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)/(19|20)\d\d$)' p3.txt > output3.txt

cat ee_classes.html | egrep -o 'EE [5-7][0-9]{2}.*?([4]\.[0] units).*?DEN' | egrep -o 'EE [5-7][0-9]{2}'| sed 's/ \<span/(4.0 units)/g' | sed 's/\<\/strong\>//g' >> output4.txt
# cat temp1|egrep -o "EE [5-7]{1}[0-9a-zA-Z]+\w+[-a-zA-Z ',:]+[3]\.[0 ]+DEN" | sed 's/3.0 DEN/(3.0 units)/g' > output4.txt
# cat temp1|egrep -o "EE [5-7]{1}[0-9a-zA-Z]+\w+[-a-zA-Z ',:]+[4]\.[0 ]+DEN" | sed 's/4.0 DEN/(4.0 units)/g' > temp2 
# cat temp2 >> output4.txt
# rm temp1
# rm temp2

egrep -o '(((//)|(/\*))(.*)?)|(^.*\*/)' p5.cpp > output5.txt

$cat > output6.txt
cat p6.txt | while read line
do
    
    if [[ "$line" =~ ^[a-z]{0,3}[0-9]{2,8}[A-Z]{3,}$ ]]
    then
        echo  "VALID" >> output6.txt
    else
        echo  "INVALID" >> output6.txt
    fi
done

