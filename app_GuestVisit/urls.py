from django.contrib import admin
from django.urls import path
from app_GuestVisit.views import guestvisit_view

urlpatterns = [
    #path('',automachine_view.index),
    #path('get_data_by_month',automachine_view.get_data_by_month),
    path('index',guestvisit_view.index),
    path('visit_record',guestvisit_view.visit_record),
    path('recycle_record',guestvisit_view.recycle_record),
    path('appointsearch',guestvisit_view.appointsearch),
    path('visit_confirm',guestvisit_view.visit_confirm),
    path('approveCustomer',guestvisit_view.approveCustomer),
    path('login',guestvisit_view.login),
    path('logout',guestvisit_view.logout),
    path('release_tempcard',guestvisit_view.release_tempcard),
    path('recycle_search',guestvisit_view.recycle_search),
    path('recycle_all',guestvisit_view.recycle_all),
    path('record_search',guestvisit_view.record_search),
    path('visit_registry',guestvisit_view.visit_registry),          #客户预定界面
    path('visit_register',guestvisit_view.visit_register),          #客户预定操作
    path('login_page',guestvisit_view.login_page),
    path('register_page',guestvisit_view.register_page),
    path('user_register',guestvisit_view.user_register),
    path('update_passwd',guestvisit_view.update_passwd),
    path('search_appoint_page',guestvisit_view.search_appoint_page),#个人预约查询界面
    path('get_appoint_data',guestvisit_view.get_appoint_data),      #获取个人预约查询数据接口
    path('del_per_appoint',guestvisit_view.del_per_appoint),        #删除个人预约
    path('update_per_appoint',guestvisit_view.update_per_appoint),  #更新个人预约信息
    path('confirm_record_page',guestvisit_view.confirm_record_page),#个人确认历史记录查询界面
    path('get_confirm_data',guestvisit_view.get_confirm_data),      #获取个人确认记录数据
    path('download_template',guestvisit_view.download_template),    #下载上传数据模板
    path('uploaddata',guestvisit_view.uploaddata),                  #文件上传
    path('get_readcsv_data',guestvisit_view.get_readcsv_data),      #读取上传的CSV数据
    path('register_from_excel',guestvisit_view.register_from_excel),#通过Excel批量上传数据
]