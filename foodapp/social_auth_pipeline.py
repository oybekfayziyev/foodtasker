from .models import Customer, Driver

def save_profile(backend, user, request, response, *args, **kwargs):
    if backend.name == 'facebook':
        avatar = 'https://graph.facebook.com/%s/picture?type=normal' %response['id']
       
    # if request['user_type'] == 'driver' and not Driver.objects.filter(user_id = user.id):
    #     Driver.objects.create(user_id=user.id, avatar=avatar)
    # elif request['user_type'] == 'customer' and not Customer.objects.filter(user_id=user.id):
    #     Customer.objects.create(user_id=user.id,avatar = avatar)


        