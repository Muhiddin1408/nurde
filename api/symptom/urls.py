from rest_framework.routers import SimpleRouter

from api.symptom.views.symptom import SymptomView

router = SimpleRouter()
router.register(r'symptom', SymptomView)
urlpatterns = [

] + router.urls
