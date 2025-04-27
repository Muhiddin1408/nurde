from rest_framework.routers import SimpleRouter

from api.symptom.views.symptom import SymptomView, DiagnosesView

router = SimpleRouter()
router.register(r'symptom', SymptomView, basename='symptom')
router.register(r'diagnoses', DiagnosesView, basename='diagnoses')
urlpatterns = [

] + router.urls
