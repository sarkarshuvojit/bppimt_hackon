from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from mechanize import Browser
import json
from .models import ArpanDaErCode

# Create your views here.



#index view, links to a template home.html
def home(request):
    return render(request, "home.html", {})



#acts kind of like a rest API, takes JSON data as POST with coordinates of points on the map then uses GoogleMaps API to get distances between them, creates an adjacency matrix and then gets the sequence of shortest average distance from the model
@csrf_exempt
def gen_path(request):
    x = json.loads(request.POST['data'])    #fetches data
    print x
    adj_mat = []    #creates empty adjacency matrix
    i1 = j1 = 0
    num_cities = len(x)
    for i in x:
        tmp_mat = []
        for j in x:
            if i!=j:
                API_KEY = "AIzaSyDBOSr6_XxvISPGX54P9bPnooE3RUpRTp0"
                orig_coord = x[i]
                dest_coord = x[j]
                br = Browser()  #creates mechanize instance
                br.set_handle_robots(False)
                # print "https://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&key={2}".format(orig_coord, dest_coord, API_KEY)
                result = br.open("https://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&key={2}".format(orig_coord, dest_coord, API_KEY)).read()    #makes a call to GoogleMapsAPI
                json_result = json.loads(result)
                tmp_mat.append(int(json_result['rows'][0]['elements'][0]['distance']['value']))
            else:
                tmp_mat.append(0)
        adj_mat.append(tmp_mat)



    obj = ArpanDaErCode()
    ans = ""
    ans = ArpanDaErCode.solve(obj, adj_mat, num_cities) #gets sequence from model
    print ans
    ret = {'data': [str(ii) for ii in ans]}

    return HttpResponse(str(json.dumps(ret)))   #returns the sequens in JSON format for the JS to handle
