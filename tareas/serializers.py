
from rest_framework import serializers
from .models import Miembro, Tarea, Categoria, Evento
from django.contrib.auth.models import User


class MiembroSerializer(serializers.ModelSerializer):
    usuario_id = serializers.PrimaryKeyRelatedField(
        source="usuario", queryset=User.objects.all(), write_only=True, allow_null=True, required=False
    )
    usuario = serializers.SerializerMethodField(read_only=True)

    def get_usuario(self, obj):
        if obj.usuario:
            return {"id": obj.usuario.id, "username": obj.usuario.username, "email": obj.usuario.email}
        return None

    class Meta:
        model = Miembro
        fields = ["id", "nombre", "color_hex", "icono", "usuario", "usuario_id"]


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "nombre", "descripcion"]



class TareaSerializer(serializers.ModelSerializer):

    categoria = CategoriaSerializer(read_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(
        source="categoria", queryset=Categoria.objects.all(), write_only=True, allow_null=True, required=False
    )


    color = serializers.CharField(source="color_hex", required=False, allow_blank=True)
    color_hex = serializers.CharField(read_only=True)

    class Meta:
        model = Tarea
        fields = [
            "id",
            "nombre",
            "descripcion",
            "icono",
            "categoria",
            "categoria_id",
            "tag",
            "puntuacion",
            "color",  # Alias para color_hex (writable)
            "color_hex",  # Solo lectura
            "tiempo_estimado",
            "creado_por",
            "recurrencia_tipo",
            "recurrencia_dias",
            "recurrencia_dia_mes",
            "recurrencia_mes",
            "recurrencia_fecha_inicio",
            "recurrencia_fecha_fin",
        ]


class EventoSerializer(serializers.ModelSerializer):
    tarea = TareaSerializer(read_only=True)
    tarea_id = serializers.PrimaryKeyRelatedField(
        source="tarea", queryset=Tarea.objects.all(), write_only=True, required=False, allow_null=True
    )
    miembro = MiembroSerializer(read_only=True)
    miembro_id = serializers.PrimaryKeyRelatedField(
        source="miembro", queryset=Miembro.objects.filter(usuario__isnull=False, usuario__is_staff=False), write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = Evento
        fields = [
            "id",
            "tarea",
            "tarea_id",
            "miembro",
            "miembro_id",
            "inicio",
            "fin",
            "estado",
            "creado_por",
            "actualizado_en",
            "creado_en",
            "duracion_minutos",
        ]


