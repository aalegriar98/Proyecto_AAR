from django.db import models
from django.contrib.auth.models import User


class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = 'roles'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.nombre_rol


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    nombre = models.CharField(max_length=50)
    correo = models.CharField(max_length=50, unique=True)
    telefono = models.CharField(max_length=15)
    area = models.CharField(max_length=30)
    id_rol = models.ForeignKey(Rol, on_delete=models.PROTECT, db_column='id_rol')

    class Meta:
        db_table = 'usuarios'

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=30, unique=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'categorias'

    def __str__(self):
        return self.nombre_categoria


class Herramienta(models.Model):
    ESTADOS_HERRAMIENTA = [
        ('Disponible', 'Disponible'),
        ('Prestado', 'Prestado'),
        ('En mantención', 'En mantención'),
    ]

    id_herramienta = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    marca = models.CharField(max_length=30)
    modelo = models.CharField(max_length=30)
    numero_serie = models.CharField(max_length=50, unique=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_HERRAMIENTA)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, db_column='id_categoria')

    class Meta:
        db_table = 'herramientas'

    def __str__(self):
        return self.nombre


class Prestamo(models.Model):
    ESTADOS_PRESTAMO = [
    ('Prestado', 'Prestado'),
    ('Devuelto', 'Devuelto'),
]

    id_prestamo = models.AutoField(primary_key=True)
    fecha_prestamo = models.DateField()
    fecha_devolucion = models.DateField()
    fecha_entrega_real = models.DateField(blank=True, null=True)
    estado_prestamo = models.CharField(max_length=20, choices=ESTADOS_PRESTAMO)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, db_column='id_usuario')
    id_herramienta = models.ForeignKey(Herramienta, on_delete=models.PROTECT, db_column='id_herramienta')

    class Meta:
        db_table = 'prestamos'

    def __str__(self):
        return f'Préstamo {self.id_prestamo}'


class Mantenimiento(models.Model):
    TIPOS_MANTENIMIENTO = [
        ('Preventivo', 'Preventivo'),
        ('Correctivo', 'Correctivo'),
    ]

    id_mantenimiento = models.AutoField(primary_key=True)
    fecha_mantenimiento = models.DateField()
    tipo_mantenimiento = models.CharField(max_length=30, choices=TIPOS_MANTENIMIENTO)
    descripcion = models.CharField(max_length=150)
    id_herramienta = models.ForeignKey(Herramienta, on_delete=models.PROTECT, db_column='id_herramienta')

    class Meta:
        db_table = 'mantenimientos'

    def __str__(self):
        return f'Mantenimiento {self.id_mantenimiento}'