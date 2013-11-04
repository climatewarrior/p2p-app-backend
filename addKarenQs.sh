#!/bin/bash

# Add Johnny (question poser)
curl -i -H "Content-Type: application/json" -X POST -d '{"username":"Johnny","email":"johnny@email.com","password":"johnnypass"}' http://localhost:5000/register


questions=( "I want to learn how to drive. Where can I go for help?" 
            "I would like some ideas on places that I can meet and make friends. Any suggestions?" 
            "Someone told me that I might be able to get a service dog to help me. How do I find out more?" 
            "I think I may qualify for government programs that assist people with disabilities who are unable to work. I am confused about where to start. Can someone point me in the right direction?"
            "What other programs are to help me with some of the things I need?"
            "I have to take medication on a daily basis and am having trouble paying for it. Are there any programs to help me pay for prescription medication?"
            "I don’t qualify for Medicaid, but I still need low cost health insurance. Where do I look?"
            "How do I register to vote?"
            "I was asked to bring a resume to a job interview? What is a resume?"
            "I get nervous when I go on job interviews. Does anybody have any tips to help me develop good interviewing skills?"
            "I am only a freshman in high school, but I want to make sure I am getting ready for college. What can I do now to prepare?"
            "What is ADA?"
            "How do I pay for college?" )


#Start adding sample questions from Johnny
for question in "${questions[@]}"
do
        curl -u Johnny:johnnypass -i -H "Content-Type: application/json" -X POST -d '{"title": "Test Question", "detailed": "'"$question"'", "tags":""}' http://localhost:5000/questions
done

