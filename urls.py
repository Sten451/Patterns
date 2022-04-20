
# front controller
def secret_front(request):
    request['data'] = "key"


def other_front(request):
    request['key'] = 'key'
 

fronts = [secret_front, other_front]

