from django.db import models

# Create your models here.


class User(models.Model):
    email = models.EmailField(verbose_name='이메일')
    password = models.CharField(max_length=128, verbose_name='비밀번호')
    level = models.CharField(max_length=8, verbose_name='등급', choices=(#choice는 level종류, 어떻게 보일지 미리 결정
        ('admin', '관리자'),
        ('user', 'user')
    ))
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')

    # 모델을 문자여로 변환
    def __str__(self):
        return self.email


class Meta:
        db_table = 'project_user'
        verbose_name = '사용자'
        verbose_name_plural = '사용자'