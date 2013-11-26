#!/bin/bash

users=( "Joy"
        "Amy"
        "Timmy"
        "George"
        "Alex"
        "Chad"
        "Mike"
        "Brad"
        "Lisa"
        "Annie"
        "Abbie"
        "Mandy"
        "Seth" )


questions=( "I want to learn how to drive. Where can I go for help?" 
            "I would like some ideas on places that I can meet and make friends. Any suggestions?" 
            "Someone told me that I might be able to get a service dog to help me. How do I find out more?" 
            "I think I may qualify for government programs that assist people with disabilities who are unable to work. I am confused about where to start. Can someone point me in the right direction?"
            "What other programs are there to help me with some of the things I need?"
            "I have to take medication on a daily basis and am having trouble paying for it. Are there any programs to help me pay for prescription medication?"
            "I don’t qualify for Medicaid, but I still need low cost health insurance. Where do I look?"
            "How do I register to vote?"
            "I was asked to bring a resume to a job interview? What is a resume?"
            "I get nervous when I go on job interviews. Does anybody have any tips to help me develop good interviewing skills?"
            "I am only a freshman in high school, but I want to make sure I am getting ready for college. What can I do now to prepare?"
            "What is ADA?"
            "How do I pay for college?" )


title=( "Learning How To Drive"
        "Places To Meet Friends"
        "Service Dogs"
        "Government Programs with Disabilities"
        "General Programs for Help"
        "Paying for Prescription Medication"
        "Do Not Qualify for Medicaid"
        "Vote Registration"
        "Resume for Job Interview"
        "Good Interviewing Skills"
        "Freshman Preparing for College"
        "ADA"
        "Paying for College" )

tags=( "Driving,Learning"
        "Socializing,Friends"
        "Dogs,Service Dogs"
        "Government,Government Programs,Disabilities"
        "Programs,Help"
        "Medication,Prescription,Budget"
        "Medicaid,Health Insurance"
        "Voting,Voter Registration"
        "Employment,Jobs,Interviews,Resumes"
        "Employment,Jobs,Interviews,Nervous"
        "Freshman,High School,College,College Preparation"
        "ADA"
        "College,Expenses,Budget" )

COUNTER=0

#Register user then post his question
for question in "${questions[@]}"
do
        username=${users[$COUNTER]}
        strEmail="@email.com"
        strPass="pass"
        email=$username$strEmail
        pass=$username$strPass

        #Register user
        curl -i -H "Content-Type: application/json" -X POST -d '{"username":"'"$username"'","email":"'"$email"'","password":"'"$pass"'","gender":"male"}' http://localhost:5000/user

        #Ask sample question
        curl -u $username:$pass -i -H "Content-Type: application/json" -X POST -d '{"title": "'"${title[$COUNTER]}"'", "detailed": "'"$question"'", "tags":"'"${tags[$COUNTER]}"'"}' http://localhost:5000/questions

        COUNTER=$[COUNTER+1]
done

