from django.db import models

class CommentReviewAbstractModel(models.Model):
    """Абстрактная модель для комментариев и отзывов."""

    author = models.ForeignKey(
        User,
        related_name='comments',
        verbose_name='Автор',
        on_delete=models.CASCADE
    )
    text = models.TextField('Введите текст')
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )
    
    class Meta:
        abstract = True
        