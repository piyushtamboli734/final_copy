from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Owenr , HostelMessImage , HostelMess
# Create your views here.
def login(req):
    if(req.session.get('owner_id')):
        return redirect('/owner/dashboard/')
    else:
        if 'Ophone' in req.POST and 'Opassword' in req.POST:
            data = Owenr.objects.get(Ophone=req.POST['Ophone'],Opassword=req.POST['Opassword'])
            if data:
                req.session['owner_id'] = data.id
                req.session['owner_name'] = data.Oname
                req.session['owner_email'] = data.Oemail
                req.session['owner_phone'] = data.Ophone
                # return HttpResponse(req.session.get('owner_name'))
                return redirect('/owner/dashboard')
            else:
                return render(req, 'owners/Registration_login.html', {'success': 'Owner Details Not Found..'})
        else:
            return render(req,'owners/Registration_login.html'); 


def registration(request):
    if request.method == 'POST':
        # Check if an owner with the provided email already exists
        is_duplicate = Owenr.objects.filter(Oemail=request.POST.get('Email')).exists()
        
        if is_duplicate:
            # Render the registration page with an error message
            return render(request, 'owners/Registration_login.html', {'error': 'An entry with this email already exists.'})
        else:
            # Create a new owner instance and save to the database
            owner = Owenr(
                Oname=request.POST.get('name'),
                Oemail=request.POST.get('Email'),
                Ophone=request.POST.get('phone'),
                Opassword=request.POST.get('password')
            )
            owner.save()
            # Render the registration page with a success message
            return render(request, 'owners/Registration_login.html', {'success': 'Owner details have been saved.'})
    else:
        # If not a POST request, redirect to the login page
        return redirect('/login/')
    

def logout(req):
    req.session.flush()
    return redirect('/login/')


# def get_all_session_values(request):
#     # Get all session key-value pairs
#     session_data = request.session.items()

#     # Print all session values (for debugging purposes)
#     for key, value in session_data:
#         print(f'{key}: {value}')

#     # You can also return or render them in a response if needed
#     return render(request, 'your_template.html', {'session_data': session_data})


def dashboard(req):
    if(req.session.get('owner_id')):
        hostels = HostelMess.objects.filter(ownerId=req.session.get('owner_id'))
        return render(req,'owners/dashboard.html',{ 'hostels' : hostels})
    else:
        return redirect('/login/')
    # return HttpResponse(req.session.get('owner_name'))


def upload_hostel_mess(request):
    if request.method == 'POST':
        # Retrieve text input values from the form
        name = request.POST.get('name')
        location = request.POST.get('location')
        contact = request.POST.get('contact')
        price = request.POST.get('price')
        ownerId = request.session.get('owner_id')
        
        # Retrieve the uploaded images
        images = request.FILES.getlist('images')

        # Create a new HostelMess entry
        hostel_mess = HostelMess(
            name=name,
            location=location,
            contact=contact,
            price=price,
            ownerId = ownerId
        )
        hostel_mess.save()

        # Save each uploaded image associated with the HostelMess entry
        for image in images:
            hostel_image = HostelMessImage(
                hostel_mess=hostel_mess,
                image=image
            )
            hostel_image.save()


        messages.success(request, 'Hostel/Mess details have been submitted for review.')
        # return HttpResponse("Hostel/Mess details have been submitted for review.")
        return redirect('/owner/dashboard')
    
    # return render(request, 'your_template_name.html')  # Replace 'your_template_name.html' with your actual template name
    return redirect('/owner/dashboard')


def index(req):
    # return HttpResponse(req.session.get('owner_id'))
    # hostel = HostelMess.objects.get()
    hostels = HostelMess.objects.prefetch_related('images').all()        
    # print(hostels)
    # return HttpResponse(hostels)
    return render(req,'user/dashborad.html',{ 'hostels' : hostels })
    


def hotelmessdetails(req,hostelId):
    if(req.session.get('owner_id')):
        # return HttpResponse(hostelId)
        hostelID = hostelId
        hostel = HostelMess.objects.filter(id=hostelID)
        images = HostelMessImage.objects.filter(hostel_mess_id=hostelID)
        return render(req,'owners/details.html',{'hostel' : hostel , 'images': images})
    else:
        return redirect('/login/')


def details(req,hostelId):
    # return HttpResponse(hostelId)
    hostelID = hostelId
    hostel = HostelMess.objects.filter(id=hostelID)
    images = HostelMessImage.objects.filter(hostel_mess_id=hostelID)
    return render(req,'user/details.html',{'hostel' : hostel , 'images': images})



def edit_hostel_mess(request, hostel_id):
    if(request.session.get('owner_id')):
        # Fetch the hostel by its ID or return a 404 if not found
        hostel = get_object_or_404(HostelMess, id=hostel_id)

        # If the form is submitted (POST request)
        if request.method == 'POST':
            # Retrieve the updated values from the form
            hostel.name = request.POST.get('name')
            hostel.location = request.POST.get('location')
            hostel.contact = request.POST.get('contact')
            hostel.price = request.POST.get('price')
            
            # Save the updated hostel information
            hostel.save()

            # Retrieve any new images uploaded
            new_images = request.FILES.getlist('images')
            if new_images:
                # Save each new image associated with the hostel
                for image in new_images:
                    HostelMessImage.objects.create(hostel_mess=hostel, image=image)

            # Optionally, remove existing images if the user has chosen to delete them
            delete_image_ids = request.POST.getlist('delete_images')
            if delete_image_ids:
                HostelMessImage.objects.filter(id__in=delete_image_ids).delete()

            # Display a success message
            messages.success(request, 'Hostel/Mess details have been updated successfully.')
            
            # Redirect to a desired page, e.g., dashboard
            return redirect('/owner/dashboard/')
        
        # Render the form with existing data (GET request)
        return render(request, 'owners/edit_hostel_mess.html', {'hostel': hostel})
    else:
        return redirect('/login/')

def delete_hostel_mess(request, hostel_id):
    if(request.session.get('owner_id')):
        # Fetch the HostelMess object by ID or return a 404 if not found
        hostel = get_object_or_404(HostelMess, id=hostel_id)

        # Delete the HostelMess and all related images
        hostel.delete()

        # Display a success message
        messages.success(request, 'Hostel/Mess and its associated images have been deleted successfully.')

        # Redirect to a desired page, e.g., the dashboard
        return redirect('/owner/dashboard/')
    else:
        return redirect('/login/')