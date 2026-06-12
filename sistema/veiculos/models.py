from django.db import models
from django.core.exceptions import ValidationError


def validate_tamanho_banner(banner):
    limite = 5 * 1024 * 1024  # 5MB
    if banner.size > limite:
        raise ValidationError('Banner muito grande. O limite é 5MB.')


class SetMusical(models.Model):
    YOUTUBE = 'youtube'
    SOUNDCLOUD = 'soundcloud'
    TIPO_CHOICES = [
        (YOUTUBE, 'YouTube'),
        (SOUNDCLOUD, 'SoundCloud'),
    ]
    nome = models.CharField(max_length=200)
    url = models.URLField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descricao = models.TextField(blank=True)
    data = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-data', 'nome']
        verbose_name = 'Set'
        verbose_name_plural = 'Sets'

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"


class Evento(models.Model):
    nome = models.CharField(max_length=200)
    data = models.DateField()
    hora = models.TimeField()
    local = models.CharField(max_length=200)
    banner = models.ImageField(blank=True, null=True, upload_to='eventos/banners/', validators=[validate_tamanho_banner])
    descricao = models.TextField(blank=True)
    capacidade = models.IntegerField(null=True, blank=True)
    link_ingresso = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['data', 'hora']

    def __str__(self):
        return f"{self.nome} - {self.data}"
