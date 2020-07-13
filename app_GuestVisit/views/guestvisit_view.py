# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from app_GuestVisit.models import guestvisit_model
import json,datetime
import os, xlrd

#访客预定登记界面
def visit_registry(request):
	if request.session.get('user_id',None):
		return render(request,'visit_registry.html',{'page':'visit_registry'})
	else:
		return login_page(request)

#访客预约查询界面
def search_appoint_page(request):
	if request.session.get('user_id',None):
		return render(request,'search_appoint_page.html',{'page':'search_appoint_page'})
	else:
		return login_page(request)

#发放临时厂牌
def index(request):
	today = datetime.datetime.now().strftime('%Y-%m-%d')
	if request.session.get('user_id',None):
		allplaces = guestvisit_model.get_in_out_place()
		return render(request,'index.html',{'page':'index','allplaces':allplaces,'today':today})
	else:
		return login_page(request)

#访客记录查询
def visit_record(request):
	if request.session.get('user_id',None):
		return render(request,'visit_record.html',{'page':'visit_record'})
	else:
		return login_page(request)

#临时厂牌回收
def recycle_record(request):
	if request.session.get('user_id',None):
		allplaces = guestvisit_model.get_in_out_place()
		return render(request,'recycle_record.html',{'page':'recycle_record','allplaces':allplaces})
	else:
		return login_page(request)

#客户访问确认界面
def visit_confirm(request):
	today = datetime.date.today().strftime('%Y-%m-%d')
	user_id = request.session.get('user_id',None)
	if user_id:
		result = guestvisit_model.visit_to_confirm()
		data = {'data':json.dumps(result),'page':'visit_confirm','today':today,'user_id':user_id}
		return render(request,'visit_confirm.html',data)
	else:
		return login_page(request)

#确认记录查询界面
def confirm_record_page(request):
	user_id = request.session.get('user_id',None)
	if user_id:
		return render(request,'confirm_record_page.html',{'page':'confirm_record_page','user_id':user_id})
	else:
		return login_page(request)

#发放临时厂牌前查询
def appointsearch(request):
	result = guestvisit_model.appointsearch()
	return HttpResponse(json.dumps({'appointlist':result}))

#确认客户
def approveCustomer(request):
	user_id = request.session.get('user_id',None)
	role_text = request.session.get('role_text',None)
	data_seq = request.GET.get('data_seq')
	if not user_id:
		data = {'result':False,'msg':'您未登录，清先登录','error':1}
	elif role_text.upper() != 'APPROVER':
		data = {'result':False,'msg':'您没有权限确认！','error':2}
	else:
		data = guestvisit_model.approveCustomer(data_seq,user_id)
	return HttpResponse(json.dumps(data))

#用户登录
#def login(request):
#	usernum = request.POST.get('usernum')
#	password = request.POST.get('password')
#	result = guestvisit_model.login(request,usernum,password)
#	return HttpResponse(json.dumps(result))

#用户登录
def login(request):
	user_id = request.POST.get('user_id')
	password = request.POST.get('password')
	keep_login = request.POST.get('keep_login')
	if user_id and password:
		data = guestvisit_model.login(request,user_id,password,keep_login)
		if data['result']:
			role_text = data['role_text']
			if role_text == 'User':								#普通用户权限
				return HttpResponseRedirect('visit_registry')
			elif role_text == 'Security':						#保安权限
				return HttpResponseRedirect('index')
			else:
				return HttpResponseRedirect('visit_confirm')	#管理员权限
		else:
			return render(request,'login_page.html',{'error':data['error']})
	else:
		return HttpResponseRedirect('login_page')

#用户注销
def logout(request):
	try:
		#request.session.clear()
		request.session['user_id'] = None
		request.session['user_name'] = None
		request.session['user_depart'] = None
		request.session['role_text'] = None
	except Exception as e:
		print(e)
	return HttpResponse(json.dumps({'result':True}))

#发放临时厂牌
def release_tempcard(request):
	temp_card = request.GET.get('temp_card')
	#user_id = request.GET.get('user_id')
	data_seq = request.GET.get('data_seq')
	place_cd = request.GET.get('place_cd')

	user_id = request.session.get('user_id',None)
	role_text = request.session.get('role_text',None)
	if not user_id or not role_text:
		data = {'result':False,'msg':'您未登录，清先登录！','error':0}
	if role_text != 'APPROVER' and role_text != 'Security':
		data = {'result':False,'msg':'您没有权限发放临时厂牌!','error':1}
	else:
		data = guestvisit_model.release_tempcard(temp_card,user_id,data_seq,place_cd)

	return HttpResponse(json.dumps(data))

#回收厂牌前查询操作
def recycle_search(request):
	cardnolist = request.GET.get('cardnolist')
	if cardnolist:
		cardnolist = json.loads(cardnolist)
	
	result = guestvisit_model.recycle_search(cardnolist)
	return HttpResponse(json.dumps(result))

#一键回收厂牌
def recycle_all(request):
	data_seq_cardno_list = request.GET.get('data_seq_cardno_list')
	out_place = request.GET.get('out_place')
	user_id = request.session.get('user_id',None)
	role_text = request.session.get('role_text',None)
	if data_seq_cardno_list:
		data_seq_cardno_list = json.loads(data_seq_cardno_list)
	if not role_text or not user_id:
		data = {'result':False,'msg':'您未登录，清先登录！'}
	elif role_text != 'Security' and role_text != 'APPROVER':
		data = {'result':False,'msg':'没有操作执行权限！'}
	else:
		data = guestvisit_model.recycle_all(user_id,out_place,data_seq_cardno_list)
	return HttpResponse(json.dumps(data))

#访客记录查询
def record_search(request):
	visitor_name = request.GET.get('visitor_name')
	begindatetime = request.GET.get('begindatetime')
	enddatetime = request.GET.get('enddatetime')
	visit_status = request.GET.get('visit_status')
	if visit_status:
		visit_status = json.loads(visit_status)
	data = guestvisit_model.record_search(visitor_name,begindatetime,enddatetime,visit_status)
	return HttpResponse(json.dumps({'result':True,'datalist':data}))

def visit_register(request):
	schedule_date = request.GET.get('schedule_date')
	schedule_time = request.GET.get('schedule_time')
	visit_name = request.GET.get('visit_name')
	visit_company = request.GET.get('visit_company')
	identity_no = request.GET.get('identity_no')
	single_multiply = request.GET.get('single_multiply')

	#if identity_no:
	#	identity_no = json.loads(identity_no)
	identity_no = identity_no.replace('\'','\"')

	employee_id = request.session.get('user_id',None)
	role_text = request.session.get('role_text',None)

	if not employee_id or not role_text:
		data = {'result':False,'msg':'您未登录，请先登录!'}
	#elif role_text != 'User' and role_text != 'APPROVER':
	#	data = {'result':False,'msg':'您没有权限录入!'}
	else:
		data = guestvisit_model.visit_register(schedule_date,schedule_time,visit_name,
			visit_company,identity_no,employee_id,single_multiply)
	return HttpResponse(json.dumps(data))

#跳转至登录页面
def login_page(request):
	role_text = request.session.get('role_text',None)

	if role_text == 'User':
		return HttpResponseRedirect('visit_registry')
	elif role_text == 'APPROVER':
		return HttpResponseRedirect('visit_confirm')
	elif role_text == 'Security':
		return HttpResponseRedirect('index')

	return render(request,'login_page.html')

#跳转至注册界面
def register_page(request):
	return render(request,'register_page.html')

#用户注册
def user_register(request):
	user_id = request.POST.get('user_id')
	user_name = request.POST.get('user_name')
	password = request.POST.get('password')
	re_password = request.POST.get('re_password')
	phone = request.POST.get('phone')
	depart = request.POST.get('depart')
	email = request.POST.get('email')
	
	data = guestvisit_model.user_register(user_id,user_name,password,phone,depart,email)
	return HttpResponse(json.dumps(data))

#修改密码
def update_passwd(request):
	oldpasswd = request.POST.get('oldpasswd')
	newpasswd = request.POST.get('newpasswd')
	user_id = request.session.get('user_id',None)
	if not user_id:
		data = {'result':False,'msg':r'出现异常！'}
	else:
		data = guestvisit_model.update_passwd(user_id,oldpasswd,newpasswd)
	return HttpResponse(json.dumps(data))

#个人预约查询
def get_appoint_data(request):
	user_id = request.GET.get('user_id')
	begindate = request.GET.get('begindate')
	enddate = request.GET.get('enddate')
	if enddate:
		enddate += ' 23:59:59'

	if not user_id:
		user_id = request.session.get('user_id',None)
	if not begindate:
		begindate = datetime.datetime.today().strftime('%Y-%m-%d')
	if not enddate:
		enddate = datetime.datetime.today().strftime('%Y-%m-%d')

	'''
	data = {
		"code":0,"msg":"","count":1000,
		"data":[
			{
				"index":"10000","visit_name":"张三","visit_date":"2018-10-26","visit_time":"12:30:00",
				"visit_phone":"17620521992","visit_company":"杭州阿里巴巴科技集团","visit_identify":"430524xxx",
				"visit_cardno":"粤B.94332","visit_reason":"某楼某层某机器坏了，要请某公司某人来修理。。。",
				"is_approver": "审批中"
			},
			{
				"index":"10000","visit_name":"张三","visit_date":"2018-10-26","visit_time":"12:30:00",
				"visit_phone":"17620521992","visit_company":"杭州阿里巴巴科技集团","visit_identify":"430524xxx",
				"visit_cardno":"粤B.94332","visit_reason":"某楼某层某机器坏了，要请某公司某人来修理。。。",
				"is_approver": "已审批"
			}
		]
	}
	#data2 = guestvisit_model.get_appoint_data(user_id,begindate,enddate)
	'''

	data = {
		'code': 0, 'msg': '','count': 100,
		'data': guestvisit_model.get_appoint_data(user_id,begindate,enddate)
	}
	return HttpResponse(json.dumps(data))

#删除个人预约
def del_per_appoint(request):
	data_seq = request.GET.get('data_seq')
	result = guestvisit_model.del_per_appoint(data_seq)
	return HttpResponse(json.dumps({'result':result}))

def update_per_appoint(request):
	visit_name = request.GET.get('visit_name')
	schedule_date = request.GET.get('schedule_date')
	schedule_time = request.GET.get('schedule_time')
	visit_phone = request.GET.get('visit_phone')
	visit_company = request.GET.get('visit_company')
	visit_identify = request.GET.get('visit_identify')
	visit_cardno = request.GET.get('visit_cardno')
	visit_reason = request.GET.get('visit_reason')
	data_seq = request.GET.get('data_seq')
	is_approver = request.GET.get('is_approver')

	result = guestvisit_model.update_per_appoint(data_seq,is_approver,visit_name,schedule_date,
		schedule_time,visit_phone,visit_company,visit_identify,visit_cardno,visit_reason)
	return HttpResponse(json.dumps({'result':result}))

#获取确认数据
def get_confirm_data(request):
	data = {
		"code":0,"msg":"","count":1000
	}

	'''
	,"data":[
		{
			"index":"10000","visit_name":"张三","visit_date":"2018-10-26","visit_time":"12:30:00",
			"confirm_time":"2018-10-30 12:50:00","visit_company":"NSTD精密马达","visit_depart":"采购部",
			"register_name": "赵若曼"
		}
	]
	'''
	
	begindate = request.GET.get('begindate')
	enddate = request.GET.get('enddate')
	if not begindate:
		begindate = datetime.date.today().strftime('%Y-%m-%d')
	if not enddate:
		enddate = datetime.date.today().strftime('%Y-%m-%d')
	begintime = begindate + ' 00:00:00'
	endtime = enddate + ' 23:59:59'
	data['data'] = guestvisit_model.get_confirm_data(begintime,endtime)
	return HttpResponse(json.dumps(data))

#下载模板
def download_template(request):
    import mimetypes
    from django.http import StreamingHttpResponse
    from wsgiref.util import FileWrapper
    from urllib import parse

    '''
    def file_iterator(file_name, chunk_size=512):#用于形成二进制数据
        with open(file_name,'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    the_file_name ="config/访客登记模板.xls"#要下载的文件路径
    response =StreamingHttpResponse(file_iterator(the_file_name))#这里创建返回
    response['Content-Type'] = 'application/vnd.ms-excel'#注意格式 
    filename = 'download_template.xls'
    response['Content-Disposition'] = 'attachment;filename={0}'.format(filename)
	'''

    the_file = 'config/访客登记模板.xls'
    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(the_file, 'rb'), chunk_size),
                           content_type=mimetypes.guess_type(the_file)[0])
    response['Content-Length'] = os.path.getsize(the_file)
    response['Content-Disposition'] = "attachment; filename="+parse.quote("访客登记模板")+".xls"
    return response

#文件上传保存
def uploaddata(request):
	from guest_visit.settings import MEDIA_ROOT
	from django.core.files.base import ContentFile
	from django.core.files.storage import default_storage

	'''
	filename = "whatever.xyz" # received file name
	file_obj = request.data['file']
	with default_storage.open('tmp/'+filename, 'wb+') as destination:
	    for chunk in file_obj.chunks():
	        destination.write(chunk)
	'''
	try:
		file = request.FILES.get('file')
		file_path = os.path.join(MEDIA_ROOT,file.name).replace('\\','/')
		path = default_storage.save(file_path, ContentFile(file.read()))
		tmp_file = os.path.join(MEDIA_ROOT, path)	#存储临时文件目录及文件名
	except Exception as e:
		print(e)

	return HttpResponse(json.dumps({'tmp_file':tmp_file}))

#读取上传的CSV文件数据
def get_readcsv_data(request):
	tmp_file = request.GET.get('tmp_file')

	#读取上传的Excel文件中的数据
	data = {"code":0,"msg":"","count":1000}
	data2 = []
	if tmp_file:
		workbook = xlrd.open_workbook(tmp_file)
		allsheets = workbook.sheets()
		if allsheets:
			uploadsheet = allsheets[0]
			row_number = uploadsheet.nrows
			for i in range(row_number):
				if i > 1:
					visitor = {}
					visitor['index'] = i-1
					visitor['visit_name'] = str(uploadsheet.cell(i,0).value).split('.')[0].strip()
					visitor['visit_phone'] = str(uploadsheet.cell(i,1).value).split('.')[0].strip()
					visitor['visit_company'] = str(uploadsheet.cell(i,2).value).split('.')[0].strip()
					visitor['visit_identify'] = str(uploadsheet.cell(i,3).value).split('.')[0].strip()
					visitor['visit_cardno'] = str(uploadsheet.cell(i,4).value).split('.')[0].strip()
					visitor['visit_reason'] = str(uploadsheet.cell(i,5).value).split('.')[0].strip()
					data2.append(visitor)

		if os.path.exists(tmp_file):	#删除上传的CSV文件.
			os.remove(tmp_file)
	data['data'] = data2
	return HttpResponse(json.dumps(data))

#通过Excel批量录入数据
def register_from_excel(request):
	visit_data = request.GET.get('visit_data')
	if visit_data:
		visit_data = json.loads(visit_data)

	data = guestvisit_model.register_from_excel(visit_data)
	return HttpResponse(json.dumps(data))
