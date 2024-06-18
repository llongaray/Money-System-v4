from django.urls import path
from .views import formGastos, funcionarios, download_excel_model, upload_csv

app_name = "rh"

urlpatterns = [
    path('funcionarios/', funcionarios, name="funcionarios"),
    path('formulario_gasto/', formGastos, name="formGastos"),
    path('download_excel_model/', download_excel_model, name="download_excel_model"),
    path('upload_csv/', upload_csv, name="upload_csv"),
]
