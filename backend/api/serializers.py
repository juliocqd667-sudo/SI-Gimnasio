from rest_framework import serializers
from core.models import CustomUser, Administrativo, Cliente, Instructor, Nutricionista
from finanzas.models import Promocion, Suscripcion, Pago, Comprobante
from actividades.models import Rutina, Ejercicio, DetalleRutina, Sala, Disciplina, Horario, Reserva, Seguimiento, Antecedentes

# --- CORE ---
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'ci', 'telefono', 'is_superuser', 'is_cliente', 'is_instructor', 'is_nutricionista', 'is_administrativo', 'fecha_nacimiento', 'sexo', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not any(c.isupper() for c in value):
            raise serializers.ValidationError("La contraseña debe tener al menos una letra mayúscula.")
        if not any(c.islower() for c in value):
            raise serializers.ValidationError("La contraseña debe tener al menos una letra minúscula.")
        if not any(c.isdigit() for c in value):
            raise serializers.ValidationError("La contraseña debe tener al menos un número.")
        import re
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?`~]", value):
            raise serializers.ValidationError("La contraseña debe tener al menos un carácter especial.")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class ClienteSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = Cliente
        fields = '__all__'

class InstructorSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = Instructor
        fields = '__all__'

class NutricionistaSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = Nutricionista
        fields = '__all__'

class AdministrativoSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = Administrativo
        fields = '__all__'

# --- FINANZAS ---
class PromocionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promocion
        fields = '__all__'

class SuscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suscripcion
        fields = '__all__'

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'

class ComprobanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comprobante
        fields = '__all__'

# --- ACTIVIDADES ---
class RutinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rutina
        fields = '__all__'

class EjercicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ejercicio
        fields = '__all__'

class DetalleRutinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleRutina
        fields = '__all__'

class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = '__all__'

class DisciplinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplina
        fields = '__all__'

class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = '__all__'

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'

class SeguimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seguimiento
        fields = '__all__'

class AntecedentesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Antecedentes
        fields = '__all__'
