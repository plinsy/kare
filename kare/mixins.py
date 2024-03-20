from django.http import JsonResponse
from django.utils.functional import Promise

from app import Patient, PatientSerializer, Treatment, TreatmentSerializer


class JSONResponseMixin:
    """
    A mixin that can be used to render a JSON response
    """

    def render_to_json_response(self, context, **response_kwargs):
        return JsonResponse(self.get_data(context), **response_kwargs, safe=False)

    def get_data(self, context):
        return context

    def serialize_object(self, obj):
        """
        Recursively serialize objects to handle non-serializable types.
        """
        if (
            isinstance(obj, Patient)
            or str(obj.__class__) == "<class 'consultation.models.Patient'>"
        ):
            return PatientSerializer(obj).data
        elif (
            isinstance(obj, Treatment)
            or str(obj.__class__) == "<class 'consultation.models.Treatment'>"
        ):
            return TreatmentSerializer(obj).data
        elif isinstance(obj, Promise):
            return str(obj)
        elif isinstance(obj, (list, tuple)):
            return [self.serialize_object(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: self.serialize_object(value) for key, value in obj.items()}
        elif hasattr(obj, "__dict__"):
            return self.serialize_object(obj.__dict__)
        else:
            return obj
