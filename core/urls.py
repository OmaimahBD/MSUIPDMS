from django.urls import path
from . import  views 
from django.contrib.auth import views as auth_views
from . import AdminCoorView, AdminChartsView


urlpatterns = [
   
    path('', views.home, name='home'),
    path('room', views.room, name='room'),
   
    path('LoginView/', views.LoginView, name='LoginView'),
    path('RegisterView/', views.RegisterView, name='RegisterView'),
    path('LogoutView/', views.LogoutView, name='LogoutView'),
    path('IntellectualProperty/<str:pk>/', views.intellectualProperty, name='IntellectualProperty'),
   
    path('AddIntellectualProperty/<str:pk>/', views.AddIntellectualProperty, name='AddIntellectualProperty'),
    path('preview/', views.preview, name='preview'),
    path('ajax/load-departments/', views.load_department, name='ajax_load_departments'),
    path('UpdateIntellectualProperty/<str:pk>', views.UpdateIntellectualProperty, name='UpdateIntellectualProperty'),
    path('profile/<str:pk>', views.userProfile, name='profile'),
    path('UpdateUser', views.UpdateUser, name='UpdateUser'),
    path('UpdatePassword', views.UpdatePassword, name='UpdatePassword'),
    path('DeleteIntellectualProperty/<str:pk>', views.DeleteIntellectualProperty, name='DeleteIntellectualProperty'),
    path('DeleteComment/<str:pk>', views.DeleteComment, name='DeleteComment'),
    path('DeleteReply/<str:pk>', views.DeleteReply, name='DeleteReply'),
    path('CollegePage/', views.CollegePage, name='CollegePage'),
    path('UploadedIP/', views.UploadedIP, name='UploadedIP'),
   
     

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
  
    path('NumIPCollege', AdminChartsView.NumIPCollege, name='NumIPCollege'),
    path('NumIPCollege1', AdminChartsView.NumIPCollege1, name='NumIPCollege1'),
    path('NumIp', AdminChartsView.NumIp, name='NumIp'),
    path('mostviewedip', AdminChartsView.mostviewedip, name='mostviewedip'),

    path('AdminHome', AdminCoorView.home, name='AdminHome'),
    path('AdminManageStudReq', AdminCoorView.ManageStudentRequest, name='AdminManageStudReq'),
    path('AdminAddCoor', AdminCoorView.addCoordinator, name='AdminAddCoor'),
    path('AdminList', AdminCoorView.viewCoordinator, name='AdminList'),
    path('AdminDeleteCoor/<str:pk>', AdminCoorView.deleteCoordinator, name='AdminDeleteCoor'),
    path('AdminEditCoor/<str:pk>', AdminCoorView.editCoordinator, name='AdminEditCoor'),
    path('AdminAddStudent/<str:pk>', AdminCoorView.addStudent, name='AdminAddStudent'),
    path('AdminStudList', AdminCoorView.viewStudent, name='AdminStudList'),
    path('AdminDeleteStud/<str:pk>', AdminCoorView.deleteStudent, name='AdminDeleteStud'),
    path('AdminEditStud/<str:pk>', AdminCoorView.editStudent, name='AdminEditStud'),
    path('AdminApproveStudent/<str:pk>', AdminCoorView.approveStudent, name='AdminApproveStudent'),
    path('AdminDisApproveStudent/<str:pk>', AdminCoorView.disapproveStudent, name='AdminDisApproveStudent'),
    path('AdminActivateStudent/<str:pk>', AdminCoorView.activateStudent, name='AdminActivateStudent'),
    path('AdminDeactivateStudent/<str:pk>', AdminCoorView.deactivateStudent, name='AdminDeactivateStudent'),
    path('AdminManageStudUpload', AdminCoorView.ManageStudentUpload, name='AdminManageStudUpload'),
    path('AdminApproveUpload/<str:pk>', AdminCoorView.approveUpload, name='AdminApproveUpload'),
    path('AdminDisApproveUpload/<str:pk>', AdminCoorView.disapproveUpload, name='AdminDisApproveUpload'),
    path('AdminIPList', AdminCoorView.viewIP, name='AdminIPList'),
    path('AdminAddIntellectualProperty/<str:pk>/', AdminCoorView.AddIntellectualProperty, name='AdminAddIntellectualProperty'),
    path('ajax/load-departments/', AdminCoorView.load_department, name='ajax_load_departments'),
    path('Admincheckplag/<str:pk>', AdminCoorView.checkPlagiarism, name='Admincheckplag'),
    path('AdminIntellectualProperty/<str:pk>/', AdminCoorView.intellectualProperty, name='AdminIntellectualProperty'),
    path('Adminprofile/<str:pk>', AdminCoorView.AdminProfile, name='Adminprofile'),
    path('AdminUpdateUser', AdminCoorView.AdminUpdateUser, name='AdminUpdateUser'),
    path('AdminUpdatePassword', AdminCoorView.AdminUpdatePassword, name='AdminUpdatePassword'),
 
   

    
    
]  