from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from .models import ValidTokens,Prof,LecInstances,AttendanceRecord,Code
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
        print(token)
        token_objs = ValidTokens.objects.filter(token = token)
        
        if token_objs.exists():
            token_objs[0].delete()

            data = {
                "msg":"logged out"
            }
            print("logged out")
        else:
            data = {
                "msg":"invalid token"
            }
            print("invalid token")

        return JsonResponse(data)


@csrf_exempt
def getCourseList(request):
    if request.method == "POST":
        token = json.loads(request.body)["token"]

        token_objs = ValidTokens.objects.filter(token = token)
        
        if token_objs.exists():
            user_obj = token_objs[0].user_obj
            course_str = Prof.objects.filter(user_obj = user_obj)[0].courses 
            courses = course_str.split(",")
            print (courses)

            data = {
                "courses":courses
            }
        else:
            data = {
                "msg":"invalid token"
            }

        return JsonResponse(data)


# create lec instance

@csrf_exempt
def createLecInstance(request):
    if request.method == "POST":
        token = json.loads(request.body)["token"]
        course = json.loads(request.body)["course"]

        token_objs = ValidTokens.objects.filter(token = token)
        
        if token_objs.exists():
            user_obj = token_objs[0].user_obj
            course_str = Prof.objects.filter(user_obj = user_obj)[0].courses 
            courses = course_str.split(",")

            # check if course exist
            if course in courses:

            
                lec_instance = LecInstances()
                lec_instance.course = course
                lec_instance.lec_hash = hash( str(token) + str(course) )%1000000000
                lec_instance.save()
                data = {
                    "hash": hash( str(token) + str(course) )%1000000000
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


#potentially buggy
@csrf_exempt
def delLecInstance(request):
    if request.method == "POST":
        token = json.loads(request.body)["token"]
        course = json.loads(request.body)["course"]

        token_objs = ValidTokens.objects.filter(token = token)
        
        if token_objs.exists():
            user_obj = token_objs[0].user_obj
            course_str = Prof.objects.filter(user_obj = user_obj)[0].courses 
            courses = course_str.split(",")

            # check if course exist
            if course in courses:

                #check if Instance exists already 
                if LecInstances.objects.filter(course=course).exists():

                    LecInstances.objects.filter(course=course)[0].delete()
                    
                    data = {
                        "msg":"deleted"
                    }
                    

                else:
                    #create Lec instance

                    

                    data = {
                        "msg":"no instance"
                    }

            else:

                data = {
                    "msg":"invalid course"
                }
            
        else:
            data = {
                "msg":"invalid token"
            }
        print(data)
        return JsonResponse(data)




# getQR

@csrf_exempt
def getQR(request):
    if request.method == "POST":
        token = json.loads(request.body)["token"]
        course = json.loads(request.body)["course"]
        lec_hash = json.loads(request.body)["hash"]

        token_objs = ValidTokens.objects.filter(token = token)
        
        if token_objs.exists():
            user_obj = token_objs[0].user_obj
            course_str = Prof.objects.filter(user_obj = user_obj)[0].courses 
            courses = course_str.split(",")

            # check if course exist
            if course in courses:

                # if code exixts then delete
                if Code.objects.filter(course = course).exists():
                    Code.objects.filter( course = course )[0].delete()

                qr = str(course) +"_"+ str(lec_hash) + "_" + str(hash (str(token) + str(course) + str(lec_hash) + str( datetime.now() ) )%1000000000)

                data = {
                    "qr": qr
                }

                code = Code()

                code.code = qr
                code.course = course
                code.save()

            else:

                data = {
                    "msg":"invalid course"
                }
            
        else:
            data = {
                "msg":"invalid token"
            }

        return JsonResponse(data)

# getStats
@csrf_exempt
def getStats(request):
    if request.method == "POST":
        token = json.loads(request.body)["token"]

        token_objs = ValidTokens.objects.filter(token = token)
        
        if token_objs.exists():
            user_obj = token_objs[0].user_obj
            course_str = Prof.objects.filter(user_obj = user_obj)[0].courses 
            courses = course_str.split(",")
            
            data = {}
            # check if course exist
            for course in courses:

                #total lec of each course

                total_lecs = ( LecInstances.objects.filter( course = course ).count() )
                
            
                students = Student.objects.all()

                filtered_students = [] # students who took this course (only username)

                for student in students:
                    stu_courses = student.courses.split(",")
                    if course in stu_courses:
                        filtered_students.append(student.user_obj.username)

                # counting unique instances of course,username to find how many lecs a particular student has attended of this particular lec
                data_segment = {}
                data_segment["total"]=total_lecs
                for student in filtered_students:
                    Attended = AttendanceRecord.objects.filter(course=course,studentID=student).count()
                    data_segment[student] = Attended

                # add "course" : [ {studentID: attended} ] to final response]
                
                data[course]=data_segment
                
            
            
            
            print(data)
            
            
        else:
            data = {
                "msg":"invalid token"
            }

        return JsonResponse(data,safe=False)
