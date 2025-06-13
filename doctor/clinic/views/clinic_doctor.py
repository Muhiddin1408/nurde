from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist# Assume a serializer exists

from apps.basic.models import AdminClinic
from apps.clinic.models import Clinic
from doctor.clinic.serializers.clinic_doctor import AdminClinicSerializer


class AdminClinicDoctorView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        try:
            # Validate required fields
            clinic_id = data.get('clinic_id')
            role_type = data.get('type')

            if not clinic_id or not role_type:
                return Response(
                    {'error': 'clinic_id and type are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Verify clinic exists
            try:
                clinic = Clinic.objects.get(id=clinic_id)
            except Clinic.DoesNotExist:
                return Response(
                    {'error': 'Invalid clinic_id'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Verify valid role type
            if role_type not in dict(AdminClinic.TYPE_CHOICES).keys():
                return Response(
                    {'error': 'Invalid type value'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Verify user has a specialist profile
            try:
                specialist = request.user.specialist
            except AttributeError:
                return Response(
                    {'error': 'User is not associated with a specialist'},
                    status=status.HTTP_403_FORBIDDEN
                )

            # Check for existing AdminClinic entry (optional, depending on requirements)
            if AdminClinic.objects.filter(specialist=specialist, clinic=clinic).exists():
                return Response(
                    {'error': 'Specialist is already associated with this clinic'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create AdminClinic instance
            admin_clinic = AdminClinic.objects.create(
                specialist=specialist,
                clinic=clinic,
                type=role_type,
                status=True  # Set status explicitly if needed
            )

            # Serialize response (optional, for better client feedback)
            serializer = AdminClinicSerializer(admin_clinic)
            return Response(
                {'msg': 'Admin clinic doctor added', 'data': serializer.data},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {'error': f'An error occurred: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )