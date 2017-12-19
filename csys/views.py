from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.core.files.uploadedfile import InMemoryUploadedFile
from csys.models import Cron
import csys.cmodels as cm
import xlrd
import os
import json


def ound(x):
    return '%.4f' % x

# Create your views here.
def csys_upload(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == 'POST':
                _ctype = request.POST.get('ctype')
                _term = request.POST.get('term')
                _year = request.POST.get('year')
                _area = request.POST.get('area')
                _seat = request.POST.get('seat')
                name = _ctype + '_' + _term + '_' + _year + '_' + _area + '_' + _seat
                file = request.FILES.get("inputfile", None)
                json_obj = {}
                try:
                    path = "row_upload_xlsx"
                    if not os.path.exists(path):
                        os.mkdir(path)
                    des = open(os.path.join(path, file.name), 'wb+')
                    for chunk in file.chunks():
                        des.write(chunk)
                    des.close()
                    data = xlrd.open_workbook(os.path.join(path, file.name))
                    sheet = data.sheet_by_index(0)
                    path = "data"
                    if not os.path.exists(path):
                        os.mkdir(path)
                    for i in range(1, sheet.nrows):
                        row_title = str(sheet.cell(i, 0).value)
                        row_data = sheet.row_values(i, 1)
                        json_obj[row_title] = row_data

                    with open(path + '/' + name + '.json', 'w', encoding='utf-8') as json_file:
                        json_file.write(json.dumps(json_obj))
                        cron = Cron(ctype=_ctype,term=_term,year=_year,area=_area,seat=_seat)
                        cron.save()

                except Exception as e:
                    return HttpResponse(e)

                return HttpResponse(name)
raw_path = "raw_upload_xlsx"
def csys_handle_data(request):
    # if request.user.is_authenticated:
        type = request.POST.get("type")
        term = request.POST.get("term")
        seat = request.POST.get("seat")
        na = type + term + seat
        file = request.FILES.get('myfile', None)
        try:
            if not os.path.exists(raw_path):
                os.mkdir(raw_path)
            des = open(os.path.join(raw_path, na), 'wb+')
            for chunk in file.chunks():
                des.write(chunk)
            des.close()
        except Exception as e:
            return HttpResponse(e)
        res = []
        if na == '111':
            n = ['SPAD','含水率','花青素','叶绿素a含量','叶绿素b含量','类胡萝卜素含量','总叶绿素含量','叶绿素a浓度','叶绿素b浓度','总叶绿素浓度','类胡萝卜浓度']
            t = [1268, 399, 1099,353,338,1663,338,338,1905,1913,514]
            f = get_data(na, t)
            res.append({'n': n[0], 't': t[0], 'f': ound(f[0]), 'z': ound(cm.m11101(f[0]))})
            res.append({'n': n[1], 't': t[1], 'f': ound(f[1]), 'z': ound(cm.m11102(f[1]))})
            res.append({'n': n[2], 't': t[2], 'f': ound(f[2]), 'z': ound(cm.m11103(f[2]))})
            res.append({'n': n[3], 't': t[3], 'f': ound(f[3]), 'z': ound(cm.m11104(f[3]))})
            res.append({'n': n[5], 't': t[5], 'f': ound(f[5]), 'z': ound(cm.m11106(f[5]))})
            res.append({'n': n[6], 't': t[6], 'f': ound(f[6]), 'z': ound(cm.m11107(f[6]))})
            res.append({'n': n[7], 't': t[7], 'f': ound(f[7]), 'z': ound(cm.m11108(f[7]))})
            res.append({'n': n[8], 't': t[8], 'f': ound(f[8]), 'z': ound(cm.m11109(f[8]))})
            res.append({'n': n[9], 't': t[9], 'f': ound(f[9]), 'z': ound(cm.m11110(f[9]))})
            res.append({'n': n[10], 't': t[10], 'f': ound(f[10]), 'z': ound(cm.m11111(f[10]))})
        if na == '112':
            n = ['SPAD','株高','生物量','LAI']
            t = [1905,2491,2477,2443]
            f = get_data(na, t)
            res.append({'n': n[0], 't': t[0], 'f': ound(f[0]), 'z': ound(cm.m11201(f[0]))})
            res.append({'n': n[1], 't': t[1], 'f': ound(f[1]), 'z': ound(cm.m11202(f[1]))})
            res.append({'n': n[2], 't': t[2], 'f': ound(f[2]), 'z': ound(cm.m11203(f[2]))})
            res.append({'n': n[3], 't': t[3], 'f': ound(f[3]), 'z': ound(cm.m11204(f[3]))})
        if na == '121':
            n = ['含水率','叶绿素a浓度','叶绿素B浓度','总叶绿素浓度','叶绿素a含量','叶绿素b含量','总叶绿素含量']
            t = [759,1367,345,364,684,354,684]
            f = get_data(na, t)
            res.append({'n': n[0], 't': t[0], 'f': ound(f[0]), 'z': ound(cm.m12101(f[0]))})
            res.append({'n': n[1], 't': t[1], 'f': ound(f[1]), 'z': ound(cm.m12102(f[1]))})
            res.append({'n': n[2], 't': t[2], 'f': ound(f[2]), 'z': ound(cm.m12103(f[2]))})
            res.append({'n': n[3], 't': t[3], 'f': ound(f[3]), 'z': ound(cm.m12104(f[3]))})
            res.append({'n': n[4], 't': t[4], 'f': ound(f[4]), 'z': ound(cm.m12105(f[4]))})
            res.append({'n': n[5], 't': t[5], 'f': ound(f[5]), 'z': ound(cm.m12106(f[5]))})
            res.append({'n': n[6], 't': t[6], 'f': ound(f[6]), 'z': ound(cm.m12107(f[6]))})
        if na == '122':
            n = ['株高', '生物量', 'LAI']
            t = [342,2425,2362]
            f = get_data(na, t)
            res.append({'n': n[0], 't': t[0], 'f': ound(f[0]), 'z': ound(cm.m12201(f[0]))})
            res.append({'n': n[1], 't': t[1], 'f': ound(f[1]), 'z': ound(cm.m12202(f[1]))})
            res.append({'n': n[2], 't': t[2], 'f': ound(f[2]), 'z': ound(cm.m12203(f[2]))})
        if na == '131':
            n = ['SPAD','含水率','叶绿素a浓度','叶绿素b浓度','总叶绿素浓度','叶绿素a含量','叶绿素b含量','总叶绿素含量']
            t = [361,351,383,383,383,383,383,344]
            f = get_data(na, t)
            res.append({'n': n[0], 't': t[0], 'f': ound(f[0]), 'z': ound(cm.m12301(f[0]))})
            res.append({'n': n[1], 't': t[1], 'f': ound(f[1]), 'z': ound(cm.m12302(f[1]))})
            res.append({'n': n[2], 't': t[2], 'f': ound(f[2]), 'z': ound(cm.m12303(f[2]))})
            res.append({'n': n[3], 't': t[3], 'f': ound(f[3]), 'z': ound(cm.m12304(f[3]))})
            res.append({'n': n[4], 't': t[4], 'f': ound(f[4]), 'z': ound(cm.m12305(f[4]))})
            res.append({'n': n[5], 't': t[5], 'f': ound(f[5]), 'z': ound(cm.m12306(f[5]))})
            res.append({'n': n[6], 't': t[6], 'f': ound(f[6]), 'z': ound(cm.m12307(f[6]))})
            res.append({'n': n[7], 't': t[7], 'f': ound(f[7]), 'z': ound(cm.m12307(f[7]))})
        if na == '211':
            n = ['SPAD', '叶绿素a', '叶绿素b', '类胡萝卜素','色素总含量','含水率']
            t = [1103,2105,1874,1885,1435,1512]
            f = get_data(na, t)
            res.append({'n': n[0], 't': t[0], 'f': ound(f[0]), 'z': ound(cm.m2111(f[0]))})
            res.append({'n': n[1], 't': t[1], 'f': ound(f[1]), 'z': ound(cm.m2112(f[1]))})
            res.append({'n': n[2], 't': t[2], 'f': ound(f[2]), 'z': ound(cm.m2113(f[2]))})
            res.append({'n': n[3], 't': t[3], 'f': ound(f[3]), 'z': ound(cm.m2114(f[3]))})
            res.append({'n': n[4], 't': t[4], 'f': ound(f[4]), 'z': ound(cm.m2115(f[4]))})
            res.append({'n': n[5], 't': t[5], 'f': ound(f[5]), 'z': ound(cm.m2116(f[5]))})
        if na == '212':
            n = ['SPAD', 'LAI']
            t = [612, 2473]
            f = get_data(na, t)
            res.append({'n': n[0], 't': t[0], 'f': ound(f[0]), 'z': ound(cm.m2121(f[0]))})
            res.append({'n': n[1], 't': t[1], 'f': ound(f[1]), 'z': ound(cm.m2122(f[1]))})
        if na == '222':
            n = ['SPAD', 'LAI', '株高']
            t = [710,1092,640]
            f = get_data(na, t)
            res.append({'n': n[0], 't': t[0], 'f': ound(f[0]), 'z': ound(cm.m2221(f[0]))})
            res.append({'n': n[1], 't': t[1], 'f': ound(f[1]), 'z': ound(cm.m2222(f[1]))})
            res.append({'n': n[2], 't': t[2], 'f': ound(f[2]), 'z': ound(cm.m2223(f[2]))})
        if na == '221':
            n = ['叶片含水率', 'SPAD', '叶绿素a', '叶绿素b', '类胡萝卜素','色素总含量']
            t = [701,608,644,643,379,643]
            f = get_data(na, t)
            res.append({'n': n[0], 't': t[0], 'f': ound(f[0]), 'z': ound(cm.m2211(f[0]))})
            res.append({'n': n[1], 't': t[1], 'f': ound(f[1]), 'z': ound(cm.m2212(f[1]))})
            res.append({'n': n[2], 't': t[2], 'f': ound(f[2]), 'z': ound(cm.m2213(f[2]))})
            res.append({'n': n[3], 't': t[3], 'f': ound(f[3]), 'z': ound(cm.m2214(f[3]))})
            res.append({'n': n[4], 't': t[4], 'f': ound(f[4]), 'z': ound(cm.m2215(f[4]))})
            res.append({'n': n[5], 't': t[5], 'f': ound(f[5]), 'z': ound(cm.m2216(f[5]))})
        if na == '232':
            n = ['SPAD', 'LAI', '株高']
            t = [606,1080,600]
            f = get_data(na, t)
            res.append({'n': n[0], 't': t[0], 'f': ound(f[0]), 'z': ound(cm.m2321(f[0]))})
            res.append({'n': n[1], 't': t[1], 'f': ound(f[1]), 'z': ound(cm.m2322(f[1]))})
            res.append({'n': n[2], 't': t[2], 'f': ound(f[2]), 'z': ound(cm.m2323(f[2]))})
        if na == '231':
            n = ['叶片含水率','SPAD', '叶绿素a', '叶绿素b', '类胡萝卜素','色素总含量']
            t = [581,697,696,1604,1593,697]
            f = get_data(na, t)
            res.append({'n': n[0], 't': t[0], 'f': ound(f[0]), 'z': ound(cm.m2311(f[0]))})
            res.append({'n': n[1], 't': t[1], 'f': ound(f[1]), 'z': ound(cm.m2312(f[1]))})
            res.append({'n': n[2], 't': t[2], 'f': ound(f[2]), 'z': ound(cm.m2313(f[2]))})
            res.append({'n': n[3], 't': t[3], 'f': ound(f[3]), 'z': ound(cm.m2314(f[3]))})
            res.append({'n': n[4], 't': t[4], 'f': ound(f[4]), 'z': ound(cm.m2315(f[4]))})
            res.append({'n': n[5], 't': t[5], 'f': ound(f[5]), 'z': ound(cm.m2316(f[5]))})
        if na == '312':
            n = ['SPAD','LAI','株高','生物量']
            t = [518,517,939,645]
            f = get_data(na, t)
            res.append({'n': n[0], 't': t[0], 'f': ound(f[0]), 'z': ound(cm.m3121(f[0]))})
            res.append({'n': n[1], 't': t[1], 'f': ound(f[1]), 'z': ound(cm.m3122(f[1]))})
            res.append({'n': n[2], 't': t[2], 'f': ound(f[2]), 'z': ound(cm.m3123(f[2]))})
            res.append({'n': n[3], 't': t[3], 'f': ound(f[3]), 'z': ound(cm.m3124(f[3]))})
        if na == '311':
            n = ['SPAD','新叶绿素','花青素','新叶绿素N']
            t = [1912,339,1903,1903]
            f = get_data(na, t)
            res.append({'n': n[0], 't': t[0], 'f': ound(f[0]), 'z': ound(cm.m3111(f[0]))})
            res.append({'n': n[1], 't': t[1], 'f': ound(f[1]), 'z': ound(cm.m3112(f[1]))})
            res.append({'n': n[2], 't': t[2], 'f': ound(f[2]), 'z': ound(cm.m3113(f[2]))})
            res.append({'n': n[3], 't': t[3], 'f': ound(f[3]), 'z': ound(cm.m3114(f[3]))})
        if na == '322':
            n = ['SPAD','LAI','株高','生物量']
            t = [979,584,978,373]
            f = get_data(na, t)
            res.append({'n': n[0], 't': t[0], 'f': ound(f[0]), 'z': ound(cm.m3221(f[0]))})
            res.append({'n': n[1], 't': t[1], 'f': ound(f[1]), 'z': ound(cm.m3222(f[1]))})
            res.append({'n': n[2], 't': t[2], 'f': ound(f[2]), 'z': ound(cm.m3223(f[2]))})
            res.append({'n': n[3], 't': t[3], 'f': ound(f[3]), 'z': ound(cm.m3224(f[3]))})
        if na == '321':
            n = ['SPAD','新叶绿素','花青素','新叶绿素N']
            t = [979,748,683,338]
            f = get_data(na, t)
            res.append({'n': n[0], 't': t[0], 'f': ound(f[0]), 'z': ound(cm.m3211(f[0]))})
            res.append({'n': n[1], 't': t[1], 'f': ound(f[1]), 'z': ound(cm.m3212(f[1]))})
            res.append({'n': n[2], 't': t[2], 'f': ound(f[2]), 'z': ound(cm.m3213(f[2]))})
            res.append({'n': n[3], 't': t[3], 'f': ound(f[3]), 'z': ound(cm.m3214(f[3]))})
        if na == '332':
            n = ['SPAD','LAI','株高','生物量']
            t = [1905,664,1928,2481]
            f = get_data(na, t)
            res.append({'n': n[0], 't': t[0], 'f': ound(f[0]), 'z': ound(cm.m3321(f[0]))})
            res.append({'n': n[1], 't': t[1], 'f': ound(f[1]), 'z': ound(cm.m3322(f[1]))})
            res.append({'n': n[2], 't': t[2], 'f': ound(f[2]), 'z': ound(cm.m3323(f[2]))})
            res.append({'n': n[3], 't': t[3], 'f': ound(f[3]), 'z': ound(cm.m3324(f[3]))})
        if na == '331':
            n = ['SPAD','新叶绿素','花青素','新叶绿素N']
            t = [696,702,700,347]
            f = get_data(na, t)
            res.append({'n': n[0], 't': t[0], 'f': ound(f[0]), 'z': ound(cm.m3311(f[0]))})
            res.append({'n': n[1], 't': t[1], 'f': ound(f[1]), 'z': ound(cm.m3312(f[1]))})
            res.append({'n': n[2], 't': t[2], 'f': ound(f[2]), 'z': ound(cm.m3313(f[2]))})
            res.append({'n': n[3], 't': t[3], 'f': ound(f[3]), 'z': ound(cm.m3314(f[3]))})
        if na == '412':
            n = ['SPAD','LAI','生物量','株高']
            t = [704,764,734,403]
            f = get_data(na, t)
            res.append({'n': n[0], 't': t[0], 'f': ound(f[0]), 'z': ound(cm.m4121(f[0]))})
            res.append({'n': n[1], 't': t[1], 'f': ound(f[1]), 'z': ound(cm.m4122(f[1]))})
            res.append({'n': n[2], 't': t[2], 'f': ound(f[2]), 'z': ound(cm.m4123(f[2]))})
            res.append({'n': n[3], 't': t[3], 'f': ound(f[3]), 'z': ound(cm.m4124(f[3]))})
        if na == '422':
            n = ['SPAD','LAI','生物量','株高']
            t = [695,408,697,408]
            f = get_data(na, t)
            res.append({'n': n[0], 't': t[0], 'f': ound(f[0]), 'z': ound(cm.m4221(f[0]))})
            res.append({'n': n[1], 't': t[1], 'f': ound(f[1]), 'z': ound(cm.m4222(f[1]))})
            res.append({'n': n[2], 't': t[2], 'f': ound(f[2]), 'z': ound(cm.m4223(f[2]))})
            res.append({'n': n[3], 't': t[3], 'f': ound(f[3]), 'z': ound(cm.m4224(f[3]))})
        if na == '432':
            n = ['SPAD','LAI','生物量','株高']
            t = [1291,1119,1356,537]
            f = get_data(na, t)
            res.append({'n': n[0], 't': t[0], 'f': ound(f[0]), 'z': ound(cm.m4321(f[0]))})
            res.append({'n': n[1], 't': t[1], 'f': ound(f[1]), 'z': ound(cm.m4322(f[1]))})
            res.append({'n': n[2], 't': t[2], 'f': ound(f[2]), 'z': ound(cm.m4323(f[2]))})
            res.append({'n': n[3], 't': t[3], 'f': ound(f[3]), 'z': ound(cm.m4324(f[3]))})
        if na == '411':
            n = ['SPAD','叶绿素a浓度','叶绿素b浓度','类胡萝卜素浓度','总叶绿素浓度','N','P','K','含水率']
            t = [700,698,699,396,699,702,405,700,447]
            f = get_data(na, t)
            res.append({'n': n[0], 't': t[0], 'f': ound(f[0]), 'z': ound(cm.m4111(f[0]))})
            res.append({'n': n[1], 't': t[1], 'f': ound(f[1]), 'z': ound(cm.m4112(f[1]))})
            res.append({'n': n[2], 't': t[2], 'f': ound(f[2]), 'z': ound(cm.m4113(f[2]))})
            res.append({'n': n[3], 't': t[3], 'f': ound(f[3]), 'z': ound(cm.m4114(f[3]))})
            res.append({'n': n[4], 't': t[4], 'f': ound(f[4]), 'z': ound(cm.m4115(f[4]))})
            res.append({'n': n[5], 't': t[5], 'f': ound(f[5]), 'z': ound(cm.m4116(f[5]))})
            res.append({'n': n[6], 't': t[6], 'f': ound(f[6]), 'z': ound(cm.m4117(f[6]))})
            res.append({'n': n[7], 't': t[7], 'f': ound(f[7]), 'z': ound(cm.m4118(f[7]))})
            res.append({'n': n[8], 't': t[8], 'f': ound(f[8]), 'z': ound(cm.m4119(f[8]))})
        if na == '421':
            n = ['SPAD','叶绿素a浓度','叶绿素b浓度','类胡萝卜素浓度','总叶绿素浓度','N','P','K','含水率']
            t = [576,340,703,338,705,700,693,345,454]
            f = get_data(na, t)
            res.append({'n': n[0], 't': t[0], 'f': ound(f[0]), 'z': ound(cm.m4211(f[0]))})
            res.append({'n': n[1], 't': t[1], 'f': ound(f[1]), 'z': ound(cm.m4212(f[1]))})
            res.append({'n': n[2], 't': t[2], 'f': ound(f[2]), 'z': ound(cm.m4213(f[2]))})
            res.append({'n': n[3], 't': t[3], 'f': ound(f[3]), 'z': ound(cm.m4214(f[3]))})
            res.append({'n': n[4], 't': t[4], 'f': ound(f[4]), 'z': ound(cm.m4215(f[4]))})
            res.append({'n': n[5], 't': t[5], 'f': ound(f[5]), 'z': ound(cm.m4216(f[5]))})
            res.append({'n': n[6], 't': t[6], 'f': ound(f[6]), 'z': ound(cm.m4217(f[6]))})
            res.append({'n': n[7], 't': t[7], 'f': ound(f[7]), 'z': ound(cm.m4218(f[7]))})
            res.append({'n': n[8], 't': t[8], 'f': ound(f[8]), 'z': ound(cm.m4219(f[8]))})
        if na == '431':
            n = ['SPAD','叶绿素a浓度','叶绿素b浓度','类胡萝卜素浓度','总叶绿素浓度','N','P','K','含水率']
            t = [696,1298,450,466,1401,690,617,548,873]
            f = get_data(na, t)
            res.append({'n': n[0], 't': t[0], 'f': ound(f[0]), 'z': ound(cm.m4311(f[0]))})
            res.append({'n': n[1], 't': t[1], 'f': ound(f[1]), 'z': ound(cm.m4312(f[1]))})
            res.append({'n': n[2], 't': t[2], 'f': ound(f[2]), 'z': ound(cm.m4313(f[2]))})
            res.append({'n': n[3], 't': t[3], 'f': ound(f[3]), 'z': ound(cm.m4314(f[3]))})
            res.append({'n': n[4], 't': t[4], 'f': ound(f[4]), 'z': ound(cm.m4315(f[4]))})
            res.append({'n': n[5], 't': t[5], 'f': ound(f[5]), 'z': ound(cm.m4316(f[5]))})
            res.append({'n': n[6], 't': t[6], 'f': ound(f[6]), 'z': ound(cm.m4317(f[6]))})
            res.append({'n': n[7], 't': t[7], 'f': ound(f[7]), 'z': ound(cm.m4318(f[7]))})
            res.append({'n': n[8], 't': t[8], 'f': ound(f[8]), 'z': ound(cm.m4319(f[8]))})
        if na == '512':
            n = ['SPAD','LAI','株高','生物量']
            t = [1975,1916,1914,1955]
            f = get_data(na, t)
            res.append({'n': n[0], 't': t[0], 'f': ound(f[0]), 'z': ound(cm.m5121(f[0]))})
            res.append({'n': n[1], 't': t[1], 'f': ound(f[1]), 'z': ound(cm.m5122(f[1]))})
            res.append({'n': n[2], 't': t[2], 'f': ound(f[2]), 'z': ound(cm.m5123(f[2]))})
            res.append({'n': n[3], 't': t[3], 'f': ound(f[3]), 'z': ound(cm.m5124(f[3]))})
        if na == '522':
            n = ['SPAD','LAI','株高','生物量']
            t = [338,424,1946,1942]
            f = get_data(na, t)
            res.append({'n': n[0], 't': t[0], 'f': ound(f[0]), 'z': ound(cm.m5221(f[0]))})
            res.append({'n': n[1], 't': t[1], 'f': ound(f[1]), 'z': ound(cm.m5222(f[1]))})
            res.append({'n': n[2], 't': t[2], 'f': ound(f[2]), 'z': ound(cm.m5223(f[2]))})
            res.append({'n': n[3], 't': t[3], 'f': ound(f[3]), 'z': ound(cm.m5224(f[3]))})
        if na == '532':
            n = ['SPAD','LAI','株高','生物量']
            t = [1931,1966,1947,2399]
            f = get_data(na, t)
            res.append({'n': n[0], 't': t[0], 'f': ound(f[0]), 'z': ound(cm.m5321(f[0]))})
            res.append({'n': n[1], 't': t[1], 'f': ound(f[1]), 'z': ound(cm.m5322(f[1]))})
            res.append({'n': n[2], 't': t[2], 'f': ound(f[2]), 'z': ound(cm.m5323(f[2]))})
            res.append({'n': n[3], 't': t[3], 'f': ound(f[3]), 'z': ound(cm.m5324(f[3]))})
        if na == '511':
            n = ['SPAD','叶绿素a','叶绿素b','类胡萝卜素','总叶绿素浓度','叶片含水率']
            t = [707,352,352,348,352,1899]
            f = get_data(na, t)
            res.append({'n': n[0], 't': t[0], 'f': ound(f[0]), 'z': ound(cm.m5111(f[0]))})
            res.append({'n': n[1], 't': t[1], 'f': ound(f[1]), 'z': ound(cm.m5112(f[1]))})
            res.append({'n': n[2], 't': t[2], 'f': ound(f[2]), 'z': ound(cm.m5113(f[2]))})
            res.append({'n': n[3], 't': t[3], 'f': ound(f[3]), 'z': ound(cm.m5114(f[3]))})
            res.append({'n': n[4], 't': t[4], 'f': ound(f[4]), 'z': ound(cm.m5115(f[4]))})
            res.append({'n': n[5], 't': t[5], 'f': ound(f[5]), 'z': ound(cm.m5116(f[5]))})
        if na == '521':
            n = ['SPAD','叶绿素a','叶绿素b','类胡萝卜素','总叶绿素浓度','叶片含水率']
            t = [655,704,560,652,399,926]
            f = get_data(na, t)
            res.append({'n': n[0], 't': t[0], 'f': ound(f[0]), 'z': ound(cm.m5211(f[0]))})
            res.append({'n': n[1], 't': t[1], 'f': ound(f[1]), 'z': ound(cm.m5212(f[1]))})
            res.append({'n': n[2], 't': t[2], 'f': ound(f[2]), 'z': ound(cm.m5213(f[2]))})
            res.append({'n': n[3], 't': t[3], 'f': ound(f[3]), 'z': ound(cm.m5214(f[3]))})
            res.append({'n': n[4], 't': t[4], 'f': ound(f[4]), 'z': ound(cm.m5215(f[4]))})
            res.append({'n': n[5], 't': t[5], 'f': ound(f[5]), 'z': ound(cm.m5216(f[5]))})
        if na == '531':
            n = ['SPAD','叶绿素a','叶绿素b','类胡萝卜素','总叶绿素浓度','叶片含水率']
            t = [360,351,351,352,351,370]
            f = get_data(na, t)
            res.append({'n': n[0], 't': t[0], 'f': ound(f[0]), 'z': ound(cm.m5311(f[0]))})
            res.append({'n': n[1], 't': t[1], 'f': ound(f[1]), 'z': ound(cm.m5312(f[1]))})
            res.append({'n': n[2], 't': t[2], 'f': ound(f[2]), 'z': ound(cm.m5313(f[2]))})
            res.append({'n': n[3], 't': t[3], 'f': ound(f[3]), 'z': ound(cm.m5314(f[3]))})
            res.append({'n': n[4], 't': t[4], 'f': ound(f[4]), 'z': ound(cm.m5315(f[4]))})
            res.append({'n': n[5], 't': t[5], 'f': ound(f[5]), 'z': ound(cm.m5316(f[5]))})
        return JsonResponse({'data': res})

def get_data(filename, bc):
    try:
        data = xlrd.open_workbook(os.path.join(raw_path, filename))
        sheet = data.sheet_by_index(0)
        f = []
        for i in range(len(bc)):
            f.append(sheet.cell_value(1, bc[i]-337))
    except Exception:
        return 0
    return f
