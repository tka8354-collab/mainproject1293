from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render

from django.contrib.auth import logout

from rest_framework.decorators import api_view

from rest_framework.response import Response


from .models import Questions, UserData , Result


# Create your views here.

                            # For Questions
def Home (request):
    return render(request ,'home.html')

def Give_Me_Questioncurd_Page(request):
    return render(request,'Questions/questioncurd.html')

def Give_Me_AddQuestion_Page(request):
    return render(request,'Questions/addquestion.html')

def Give_Me_ViewQuestion_Page(request):
    return render(request,'Questions/viewquestion.html')

def Give_Me_UpdateQuestion_Page(request):
    return render(request,'Questions/updatequestion.html')

def Give_Me_DeleteQuestion_Page(request):
    return render(request,'Questions/deletequestion.html')

def Give_Me_ShowAllQuestion_Page(request):
    qdata = Questions.objects.all()
    return render(request,'Questions/showallquestion.html',{'qdata':qdata})




def AddQuestions(request):
  qno = request.GET['qno']
  qtext = request.GET['qtext']
  op1 =request.GET['op1']
  op2 =request.GET['op2']
  op3 =request.GET['op3']
  op4 =request.GET['op4']
  subject = request.GET['subject']
  answer = request.GET['answer']

  Questions.objects.create(qno = qno , qtext = qtext ,op1 = op1, op2 = op2, op3 = op3 , op4 = op4 , subject = subject, ans = answer)
  return render (request,'Questions/addquestion.html' ,{'message' : 'Question add Successfully'})

def View_Question(request):
    qno = request.GET['qno']
    qdata = Questions.objects.get(qno=qno)
    return render (request,'Questions/viewquestion.html' ,{'qdata' : qdata})

def View_Question_Update(request):
    qno = request.GET['qno']
    qdata = Questions.objects.get(qno=qno)
    return render (request,'Questions/updatequestion.html' ,{'qdata' : qdata})

def UpdateQuestion(request):
    qno = request.GET['qno']
    qdata = Questions.objects.filter(qno=qno)
    qdata.update(
        qtext = request.GET['qtext'],
        op1 =request.GET['op1'],
        op2 =request.GET['op2'],
        op4 =request.GET['op4'],
        subject = request.GET['subject'],
        ans = request.GET['answer']
    )
    return render (request,'Questions/updatequestion.html' ,{'message' : 'Question update Successfully'})

def View_Question_Delete(request):
    qno = request.GET['qno']
    qdata = Questions.objects.get(qno=qno)
    return render (request,'Questions/deletequestion.html' ,{'qdata' : qdata})

def DeleteQuestion(request):
    qno = request.GET['qno']
    subject = request.GET['subject']

    Questions.objects.filter(qno=qno, subject=subject).delete()
    return render (request,'Questions/deletequestion.html' ,{'message' : 'Question delete Successfully'})


                                # For Student 



# Create your views here.
def GiveMeRagisterPage(request):
    return render(request,'Student/ragister.html')

def Ragister(request):
    uname = request.GET['username']
    passwd = request.GET['password']
    mobno = request.GET['mobno']

    UserData.objects.create(username = uname, password = passwd , mobno = mobno)
    return render(request,'Student/login.html',{'message': 'user ragister successfully'})

def GiveMeLoginPage(request):
    return render(request,'Student/login.html')

def Login(request):
    uname = request.GET['username']
    passwd = request.GET['password']

    request.session['username'] = uname

    udata = UserData.objects.get(username = uname)

    if (udata.password == passwd):
        request.session['answer'] = {}
        request.session['score'] = 0
        request.session['qno'] = 0
        return render(request,'Questions/subject.html')
    else :
        return render(request,'Student/login.html',{'message':'invalid password'})
    
def GiveMeUserCurdPage(request):
    return render(request,'Student/usercurd.html')


def GiveMeShowAllPage(request):
    udata = UserData.objects.all()
    return render(request,'Student/showall.html',{'udata':udata})
 

def AddUser(request):
    uname = request.GET['username']
    passwd = request.GET['password']
    mobno = request.GET['mobno']

    UserData.objects.create(username = uname, password = passwd , mobno = mobno)
    return render(request,'Student/usercurd.html',{'message': 'user ragister successfully'})

def ShowUser(request):
    try : 
        uname = request.GET['username']
        udata = UserData.objects.get(username = uname)
        return render(request,'Student/usercurd.html',{'udata':udata})
    except :
         return render(request,'Student/usercurd.html',{'message': 'user not Found'})

def UpdateUser(request):
    uname = request.GET['username']
    udata = UserData.objects.filter(username = uname)
    udata.update(password = request.GET['password'], mobno = request.GET['mobno'])
    print(connection.queries)
    return render(request,'Student/usercurd.html',{'message': 'user update successfully'})

def DeleteUser(request):
    uname = request.GET['username']
    UserData.objects.filter(username = uname).delete()
    return render(request,'Student/usercurd.html',{'message': 'user delete successfully'})

def DeleteUserForShowAllPage(request):
    uname = request.GET['username']
    UserData.objects.filter(username = uname).delete()
    udata = UserData.objects.all()
    return render(request,'Student/showall.html',{'udata':udata})


def StartTest(request):
    subject = request.GET['subject']

    request.session['subject'] = subject

    queryset = Questions.objects.filter(subject = subject).values()

    # select * from questions where subject =  request.GET['subject'];

    listallquestions = list(queryset)

    request.session['listallquestions'] = listallquestions

    return render (request,'starttest.html',{"question":listallquestions[0]})

def NextQuestion(request):
   allquestions =  request.session['listallquestions'] 
   questionindex = request.session['qno']

   if 'op' in request.GET:
       allanswer = request.session['answer']  # {}
       allanswer[request.GET["qno"]] = [request.GET["qno"],request.GET["qtext"],request.GET["op"],request.GET["answer"]]

    #    allanswer = {1: [1, 2+2, 4, 4]}

   try:
        if questionindex <= len(allquestions):
             request.session['qno']+=1
             question = allquestions[request.session['qno']]
   except:
         return render (request,'starttest.html',{"message":"Go to previous question"}) 
    
   return render (request,'starttest.html',{"question":question})  

def PreviousQuestion(request):
   allquestions =  request.session['listallquestions'] 
   questionindex = request.session['qno']

   if 'op' in request.GET:
       allanswer = request.session['answer']  # {}
       allanswer[request.GET["qno"]] = [request.GET["qno"],request.GET["qtext"],request.GET["op"],request.GET["answer"]]

   try:
        if questionindex > 0 :
             request.session['qno']-=1
             question = allquestions[request.session['qno']]
   except:
         return render (request,'starttest.html',{"message":"Go to next question"}) 
    
   return render (request,'starttest.html',{"question":question}) 

def End_Test(request):
    if 'op' in request.GET:
       allanswer = request.session['answer']  # {}
       allanswer[request.GET["qno"]] = [request.GET["qno"],request.GET["qtext"],request.GET["op"],request.GET["answer"]]
       request.session['answer']= allanswer

    response = request.session['answer'].values()

    # allanswer = {1: [1, 2+2, 4, 4]}

    # response.values()   #  [1, 2+2, 4, 4]

    for ans in response:
        if ans[2] == ans[3]:
            request.session['score']+=1

    finalscore = request.session['score']

    uname = request.session['username']

    userdb = UserData.objects.get(username = uname)

    Result.objects.create(
        username= userdb,
        subject = request.GET['subject'],
        marks = finalscore
    )
    return render(request,'Result/score.html',{'response':response, 'finalscore':finalscore})


def GetAllResultPage(request):
    rdb= Result.objects.all()
    return render (request, 'Result/allresult.html',{'rdb':rdb})


def LogoutUser(request):
    logout(request)
    return render(request,'Student/login.html')


from .serializer import userdataserilizer

@api_view(['GET'])
def Student_info(request):
  return HttpResponse("{rollno : 101, name:Pritik}")

@api_view(["GET"])
def GetStudent(request,uname):
    udb =  UserData.objects.get(username = uname)
    response = Response({"username" : udb.username,"password": udb.password , "mobno":udb.mobno})
    return response

@api_view(["GET"])
def GetStudent1(request,uname):
    udb =  UserData.objects.get(username = uname)
    useri = userdataserilizer(udb)
    response = Response(useri.data)
    return response

@api_view(['GET'])
def Allstudent(request):
    udb = UserData.objects.all().values()
    uquery = list(udb)
    # useri = userdataserilizer(udb)
    response = Response(uquery)
    return response