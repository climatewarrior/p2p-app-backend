#!/bin/bash

users=( "Joy"
        "Lisa"
        "Grace"
        "Chris"
        "Brandon"
        "Alex"
        "David"
        "Christine"
        "Regina"
        "Rebecca"
        "Sandy"
        "Mandy"
        "Gabe" )


answers=( "Shepherd Spinal Center does evaluations and assessments for those who use power chairs or who may need adapted vehicles. Check out: http://www.shepherd.org/patient-programs/outpatient-clinics/adapted-driving-services"
          "Consider attending or joining a local church or community organization. Check out classes and activities through local parks and recreation or search online for meet-ups and/or group meetings for activities that you might enjoy. For example, kayaking, movies, comics, etc." 
          "There are organizations that train dogs to assist people with disabilities or special healthcare needs to enhance their independence or their quality of life. Search the P2P Special Needs Database at http://p2pga.force.com/Provider under the General Services Category of Adaptations/Accessibility Services and the Specific Service of Canine Assistance to find information about organizations that provide trained service dogs to qualified individuals."
          "Depending on your age, disability, income and assets, you may qualify for government assistance which can help you pay your living expenses.  If you are in Georgia, COMPASS http://compass.ga.gov is a good place to begin and see if you qualify for services. To find out if you qualify for SSI (Supplemental Security Income), a federal program that assists individuals with disabilities who are unable to work due to a disability, start here: http://www.benefits.gov/ssa"
          "You may qualify for free cell phone and free minutes if you receive benefits from other low income programs. Contact: \nAssurance Wireless http://www.freegovernmentcellphones.net/free-cell-phone-providers/assurance-wireless \nReachOut Wireless http://www.freegovernmentcellphones.net/free-cell-phone-providers/reachout-wireless \nSafelink Wireless http://www.freegovernmentcellphones.net/free-cell-phone-providers/safelink-wireless \n Life Wireless http://www.freegovernmentcellphones.net/free-cell-phone-providers/life-wireless \n Budget Mobile http://www.freegovernmentcellphones.net/free-cell-phone-providers/budget-mobile"
          "Yes, check out this info on free or discounted prescription medication programs in GA http://www.dcor.state.ga.us/pdf/Drug_Assistance_Programs.pdf"
          "You can call P2P to talk with an ACA Navigator or check out www.healthcare.gov"
          "To register to vote in Georgia, you can \nDownload, complete, and mail in a Voter Registration Application found at http://sos.georgia.gov/elections/vrinfo.htm with a copy of a current and valid photo ID, a copy of a current utility bill, bank statement, government check, paycheck, or other government document that shows your name and address, or, \nContact your local county board of registrars' office (http://sos.georgia.gov/cgi-bin/countyregistrarsindex.asp) or election office, public library, public assistance office, recruitment office, schools and other government offices for a mail-in registration form. \nRegistration is offered when you renew or apply for your driver's license at Department of Motor Vehicle Safety drivers license posts. \nCollege students can obtain Georgia voter registration forms, or the necessary forms to register in any state in the U.S., from their school registrar's office or from the office of the Vice President of Academic Affairs."
          "A resume is usually a document you create to show employers your background and skills. It contains a lot of the same information as the job application but you can include extra things about yourself – such as, volunteer work, hobbies, sports, etc.  See this sample resume. "
          "A resume is usually a document you create to show employers your background and skills. It contains a lot of the same information as the job application but you can include extra things about yourself – such as, volunteer work, hobbies, sports, etc.  See this sample resume."
          "First, you need a high school diploma. \nSecond, you need to make sure the classes you are taking are preparing you for college.  Colleges require that you take a certain number of math, english, science, foreign language, etc.  \nMaybe you have heard teachers or parents talk about your transcripts – this is the official record from your high school showing all the courses you have taken and the grades you got. Colleges require a copy of your official transcripts so they can see what your grades have been in high school. This is the reason why those grades are so important! \nHave you heard people talking about the SATs or ACTs?  These are tests that colleges require students to take so that they can see how you compare to other students that are applying to college. SATs and ACTs are the most common, but there are some others – so you want to make sure you discuss with your school which ones you need and have it in you plan. High school students usually take them in their junior and senior years. \nColleges also look at other things besides grades when they are deciding if you are a good fit for their school. They want students that are well-rounded and offer other gifts – so, they will be looking at clubs, activities, sports, hobbies that you are involved with now.  Make sure you are including these things in your plan."
          "The Americans with Disabilities Act of 1990 (ADA) prohibits discrimination and ensures equal opportunity for persons with disabilities in employment, State and local government services, public accommodations, commercial facilities, and transportation.\nFor more info on ADA go to https://adata.org/FAQbooklet"
          "Check out www.georgiacollege411.org for information on Financial aid and planning for paying the cost of college. There are scholarships, grants, and financial aid resources, as well as the HOPE in GA.")



sudo python pyScript.py > questionIDs.log

declare questionIDsArr

while IFS=$'\t' read -r -a questionIDsArr
do
     COUNTER=0
     for answer in "${answers[@]}"
     do
        a="http://localhost:5000/questions/"
        b=${questionIDsArr[$COUNTER]}
        url=$a$b
        strEmail="@email.com"
        email=$username$strEmail
        username=${users[$COUNTER]}
        strPass="pass"
        pass=$username$strPass

        #Register user
        curl -i -H "Content-Type: application/json" -X POST -d '{"username":"'"$username"'","email":"'"$email"'","password":"'"$pass"'"}' http://localhost:5000/user

        #Post answer
        curl -u $username:$pass -i -H "Content-Type: application/json" -X PUT -d '{"answer": "'"$answer"'"}' $url

        COUNTER=$[COUNTER+1]
     done
done < questionIDs.log



#echo ${questionIDsArr[0]} >> log.log
#echo "${questionIDsArr[$COUNTER]}" >> log.log
#Start adding answers from Emily

