from django.shortcuts import render,redirect
from django.db import models
from django.views import  View
from .models import Voyage , utilisateur,mess,reservation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from .form import  UtilForm,UtilForm2,LoginForm,MessagesForm
from django.http import HttpResponseRedirect
from django.contrib import messages
#from gestionStock import settings
from django.core.mail import send_mail
from datetime import datetime
from django.conf import settings
import reportlab
import io
import mysql.connector
from django.http import FileResponse
from reportlab.pdfgen import canvas

# Create your views here.


#class Home(View):
 #   def get(self,request):
  #      return HttpResponse("<h1> Wellcome to our application FLC </h1>")

def Home(request):
    return render(request,'home.html')

#def logIn(request):
#
 #   if request.method == "POST":
  #      username=request.POST["username"]
   #     password=request.POST["password"]
    #    user=authenticate(request, username=username, password=password)
     #   if user is not None:
      #      login(request,user)
       #     first_name=user.first_name
        #    #last_name=User.last_name
         #   return render(request,'bonjour.html',{'first_name':first_name})
        #else :
         #   messages.error(request,'Mauvaise Authentification')
          #  return HttpResponseRedirect('login')
    #return render(request,'login.html')

def login_page(request):
    form = LoginForm()
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.success(request,'Bonjour, Vous êtes Bien connecté.') 
                return HttpResponseRedirect('listeVoyage')
            else:
                messages.success(request,'Mauvaise authentification') 
                message = 'Identifiants invalides.'
    return render(request, 'login2.html', context={'form': form, 'message': message})
    #def login_page(request):
#    form = forms.LoginForm()
 #   if request.method == 'POST':
  #      form = forms.LoginForm(request.POST)
   #     if form.is_valid():
    #        pass
    #return render(request, 'login.html', context={'form': form})
def dcx(request):
    logout(request)
    messages.success(request,'Vous avez été bien déconnecter')
    return HttpResponseRedirect('login2')

#def register(request):
 #   return render (request,'register.html')
#def test(request):
 #   return render (request,'test.html')

def apropos(request):
    return render (request,'apropos.html')

#def bonjour(request):
 #   return render (request,'bonjour.html')

#def contact(request):
 #   return render (request,'contact.html')

#@login_required(login_url="login")

class ListeVoyage(View):
    def get(self,request):
        #user=User.objects.all()
        Voyages = Voyage.objects.all()
        return render(request,'ListeVoyage.html',{'voyages':Voyages} )
    
class detailVoy(View):
    def get(self,request,num):
        Voyages = Voyage.objects.filter(num=num)
        return render(request,'detailVoy.html',{'voy':Voyages} )

class res(View):
    def get(self,request,num):
        nb=Voyage.objects.get(num=num)
        nbrpl=nb.nmbPlace-1
        usr=request.user.id
        conx=mysql.connector.connect(user="root",password="",host="localhost",database="dbvoyage")
        myc=conx.cursor()
        myc.execute("insert into base_reservation(numuser_id,pays_id)values(%s,%s)",(usr,num))
        id=myc._last_insert_id
        myc.execute("update base_voyage set nmbPlace=%s where num=%s",(nbrpl,num))
        conx.commit()
        myc.close()
        conx.close()
        nres=reservation.objects.filter(id=id)
        #usr=User.objects.filter(id=usr)
        #nres=reservation.objects.filter(numuser=usr,pays=num)
        print(nres)
        return render(request,'pdf.html',{'numres':nres} )
    

class ListeMessages(View):
    def get(self,request):
        #user=User.objects.all()
        mess1 = mess.objects.all()
        return render(request,'messages.html',{'mesg':mess1} )
    
#class NewUtil (View):
 #   def get(self,request):
  #      form=UtilForm()
   #     return render (request,'register2.html',{'form':form})
    
class contact(View):
    def get(self,request):
        form=MessagesForm
        return render(request, 'contact.html',{'form':form})
    def post(self,request):
        form=MessagesForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Nous avons Bien reçu votr message . Merci d'avoir Participer .")
            return HttpResponseRedirect('contact')
        return render(request,'contact.html',{'form':form})
  
   


  
def register(request):
    if request.method=="POST":
        username=request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        if User.objects.filter(username=username):
            messages.error(request,'ce username existe dèjà ')
            return HttpResponseRedirect('register2')
        if User.objects.filter(email=email):
            messages.error(request,'cet email existe dèjà ')
            return HttpResponseRedirect('register2')
        if not username.isalnum():
            messages.error(request,'La forme du username est inappropriée  ')
            return HttpResponseRedirect('register2')
        if password != password2 :
            messages.error(request,'Les mots de passe sont différents. Veuillez réentrer le meme mot de passe  ')
            return HttpResponseRedirect('register2')

        new_util=User.objects.create_user(username,email,password)
        new_util.first_name=first_name
        new_util.last_name=last_name
        new_util.save()
        messages.success(request,'VOTRE COMPTE A été créer avec Succés ')
        #message="Votre compte a été bien créer. Bienvenu parmi FLC FAMILLY"
        #title="Creation du compte avec succes"

        subject="Bienvenu sur FLC system Login"
        message="WELCOME"
        #changer apres attention 
        from django.template import loader
        mail=new_util.email
        fn=new_util.first_name
        ln=new_util.last_name
        html_message = loader.render_to_string('email.html',{'email':mail,'frst':fn,'lst':ln})#hna  
        from_email=settings.EMAIL_HOST_USER
        to_list=[new_util.email]
        send_mail(subject , message , from_email , to_list ,html_message=html_message)
        return HttpResponseRedirect('login2')
    return render (request,'register2.html')
#subjet="Test Email"
        #template='email.html'
        #context={
        #    'date':datetime.today().date,
         #   'email':email
        #}
        #receivers=[email]
        #has_send=send_email_with_html_body(
         #   subjet=subjet,
          #  receivers=receivers,
           # template=template,
            #context=context )
        #if has_send:
         #   return render(request,'register2.html',{"msg":"mail envoyé avec succes "})
        #return render(request,'register2.html')
   
#class register(View):
  #  def get(self,request):
  #      form=UtilForm2()
   #     if User.objects.filter(email=User.email):
    #        messages.error(request,"Cet email est déjà pris")
     #       return HttpResponseRedirect('register2')
      #  return render(request,'register2.html',{'form':form})
    #def post(self,request):
     #   form=UtilForm(request.POST,request.FILES)
      #  if form.is_valid():
       #     form.save()
        #    messages.success(request,'Votre compte a été créer avec succes . Bienvenue .')
         #   return HttpResponseRedirect('login')
        #return render(request,'register2.html',{'form':form})
   
    #def get(self,request):
     #   form=UtilForm()
      #  if utilisateur.objects.filter(email=utilisateur.email):
       #     messages.error(request,"Cet email est déjà pris")
        #    return HttpResponseRedirect('register')
        #return render(request,'register.html',{'form':form})
    #def post(self,request):
     #   form=UtilForm(request.POST,request.FILES)
      #  if form.is_valid():
       #     form.save()
        #    messages.success(request,'Votre compte a été créer avec succes . Bienvenue .')
         #   return HttpResponseRedirect('login')
        #return render(request,'register.html',{'form':form})
    
#if request.method=="POST":
     #   nom=request.POST['nom']
      #  prenom=request.POST['prenom']
       # email=request.POST['email']
        #pw=request.POST['pw']
        #pw2=request.POST['pw']
        #new_util=utilisateur.objects.create_User(nom,prenom,email,pw)
        #new_util.nom=nom
        #new_util.prenom=prenom
        #new_util.email=email
        #new_util.pw=pw
        #new_util.save()
        #messages.success(request,'Votre compte a été créer avec succes . Bienvenue .')
        #return HttpResponseRedirect('login')
    #return render(request,'register.html')


def some_view(request):
    def get(self,request,num):
        Voyages = Voyage.objects.filter(num=num)
        return render(request,'detailVoy.html',{'voy':Voyages} )
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    #p.drawString(100, 100, "Hello world.")
    p.drawString(50,800,'Bonjour votre réservetion est bien effectuer.')

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="Reservation.pdf")


 
from io import BytesIO #A stream implementation using an in-memory bytes buffer
                       # It inherits BufferIOBase
 
from django.http import HttpResponse
from django.template.loader import get_template
 
#pisa is a html2pdf converter using the ReportLab Toolkit,
#the HTML5lib and pyPdf.
 
from xhtml2pdf import pisa  
#difine render_to_pdf() function
 
def render_to_pdf(template_src, context_dict={}):
     template = get_template(template_src)
     html  = template.render(context_dict)
     result = BytesIO()
 
     #This part will create the pdf.
     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
     if not pdf.err:
         return HttpResponse(result.getvalue(), content_type='application/pdf')
     return None


from django.http import HttpResponse
from django.views.generic import View
 
#importing get_template from loader
from django.template.loader import get_template
 
class pdf(View):
    def get(self,request,num):
        Voyages = Voyage.objects.filter(num=num)
        return render(request,'pdf.html',{'voy':Voyages} )
 
#Creating our view, it is a class based view
class GeneratePdf(View):
     def get(self, request, *args, **kwargs):
        #getting the template
        pdf = render_to_pdf('pdf.html',)
        #return render(request,'pdf.html',{'voy':Voyages})
         #rendering the template
        return HttpResponse(pdf, content_type='application/pdf')


#import pdfkit
#pdfkit.from_string('pdf.html', 'reserve.pdf')


    
