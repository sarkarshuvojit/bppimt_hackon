from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from mechanize import Browser
import json
from .models import ArpanDaErCode

# Create your views here.

def home(request):
    return render(request, "home.html", {})

@csrf_exempt
def gen_path(request):
    x = json.loads(request.POST['data'])
    print x
    adj_mat = []
    i1 = j1 = 0
    num_cities = len(x)
    for i in x:
        tmp_mat = []
        for j in x:
            if i!=j:
                API_KEY = "AIzaSyDBOSr6_XxvISPGX54P9bPnooE3RUpRTp0"
                orig_coord = x[i]
                dest_coord = x[j]
                br = Browser()
                br.set_handle_robots(False)
                # print "https://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&key={2}".format(orig_coord, dest_coord, API_KEY)
                result = br.open("https://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&key={2}".format(orig_coord, dest_coord, API_KEY)).read()
                json_result = json.loads(result)
                tmp_mat.append(int(json_result['rows'][0]['elements'][0]['distance']['value']))
            else:
                tmp_mat.append(0)
        adj_mat.append(tmp_mat)



    obj = ArpanDaErCode()
    ans = ""
    ans = ArpanDaErCode.solve(obj, adj_mat, num_cities)
    print ans
    ret = {'data': [str(ii) for ii in ans]}

    return HttpResponse(str(json.dumps(ret)))
