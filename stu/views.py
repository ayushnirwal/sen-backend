from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from .models import Student
from prof.models import ValidTokens,LecInstances,AttendanceRecord,Code
import json
from stu.models import Student
from datetime import datetime

# Create your views here.

@csrf_exempt
def login(request):
    if request.method == "POST":
        
        username = json.loads(request.body)["username"]
        password = json.loads(request.body)["password"]


        #authenticate 
        user = authenticate(username=username, password=password)

        if user is not None:

            if not ValidTokens.objects.filter(user_obj = user).exists():
                #create token
                token = hash(username + password)%1000000000  # json while receiving token was changing unexpectedly so shortened the no
                newToken=ValidTokens()
                newToken.token = token
                newToken.user_obj = user
                newToken.save()

            else:
                token = ValidTokens.objects.filter(user_obj = user)[0].token

            

            

            #create response obj

            data={
                "token":token
            }
            return JsonResponse(data)
        else:
            #wrong credentials
            data={
                "msg":"wrong credentials"
            }
            return JsonResponse(data)

        

        
        #send resposnse
        


@csrf_exempt
def logout(request):
    if request.method == "POST":
        token = json.loads(request.body)["token"]
        token_objs = ValidTokens.objects.filter(token = token)
        
        if token_objs.exists():
            token_objs[0].delete()

            data = {
                "msg":"logged out"
            }
        else:
            data = {
                "msg":"invalid token"
            }

        return JsonResponse(data)

@csrf_exempt
def getCourseList(request):
    if request.method == "POST":
        token = json.loads(request.body)["token"]

        token_objs = ValidTokens.objects.filter(token = token)
        
        if token_objs.exists():
            user_obj = token_objs[0].user_obj
            course_str = Student.objects.filter(user_obj = user_obj)[0].courses 
            courses = course_str.split(",")

            data = {
                "courses":courses
            }
        else:
            data = {
                "msg":"invalid token"
            }

        return JsonResponse(data)


@csrf_exempt
def markMe(request):
    if request.method == "POST":
        token = json.loads(request.body)["token"]
        QR = json.loads(request.body)["QR"]

        token_objs = ValidTokens.objects.filter(token = token)
        
        if token_objs.exists():
            # splice QR into course,lec_hash and code 
            # index   0->course   1->lec_hash   2->code in data
            
            # check code
            if Code.objects.filter(code = QR).exists():

                studentID = token_objs[0].user_obj.username

                AttRec = AttendanceRecord()
                AttRec.studentID = studentID
                AttRec.course = data[0]
                AttRec.lecID = data[1]
                AttRec.save() 

            else : 
                data = {
                "msg":"invalid QR",
            }

        else:
            data = {
                "msg":"invalid token"
            }

        return JsonResponse(data)



@csrf_exempt
def getStats(request):
    if request.method == "POST":
        token = json.loads(request.body)["token"]
        course = json.loads(request.body)["course"]

        token_objs = ValidTokens.objects.filter(token = token)
        

        if token_objs.exists():
            user_obj = token_objs[0].user_obj
            course_str = Student.objects.filter(user_obj = user_obj)[0].courses 
            courses = course_str.split(",")

            if course in courses:

                total_lecs =  LecInstances.objects.filter( course = course ).count() 
                Attended = AttendanceRecord.objects.filter( course = course ).count()
                
                Sheet = []

                lec_instances = LecInstances.objects.filter( course = course )

                for lec_instance in lec_instances:
                    if AttendanceRecord.objects.filter(lecID = lec_instance.lec_hash , studentID = user_obj.username).exists():
                        Sheet.append({"Date" : lec_instance.date , "Attended" : True })

                    else:
                        Sheet.append({"Date" : lec_instance.date , "Attended" : False })

                data={
                    "Total" : total_lecs,
                    "Attended" : Attended,

                    "Sheet":Sheet
                }

            else:
                data = {
                "msg":"invalid course"
            }

        else:
            data = {
                "msg":"invalid token"
            }

        return JsonResponse(data)
    
