from django.db import models
import time


class PoolEntrance(models.Model):
    ALL_DAY_PASS = 1
    HALF_AN_HOUR_PASS = 2
    AN_HOUR_PASS = 3
    AN_TWO_HOURS_PASS = 4
    MASSAGE = 5
    SWIMMING_LESSON = 6

    PASS_TYPE_CHOICES = (
        (ALL_DAY_PASS, 'karnet całodniowy'),
        (HALF_AN_HOUR_PASS, 'bilet 30 min'),
        (AN_HOUR_PASS, 'bilet 60 min'),
        (AN_TWO_HOURS_PASS, 'bilet 120 min')
    )

    ADDITIONAL_SERVICES_CHOICES = (
        (MASSAGE, 'masaż'),
        (SWIMMING_LESSON, 'lekcja pływania')
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    entrance_date = models.DateTimeField(auto_now_add=True)
    leave_date = models.DateTimeField(blank=True, null=True)
    permission_for = models.PositiveSmallIntegerField(choices=PASS_TYPE_CHOICES)
    additional_service = models.PositiveSmallIntegerField(choices=ADDITIONAL_SERVICES_CHOICES, null=True, blank=True)

    class Meta:
        ordering = ['entrance_date']

    @property
    def is_ended(self):
        return time.time() > self.leave_date.timestamp()


class Task(models.Model):
    creator = models.ForeignKey(to='users.CustomUser', on_delete=models.CASCADE, related_name='task_creator')
    responsible_person = models.ForeignKey(to='users.CustomUser', on_delete=models.CASCADE,
                                           related_name='task_executor')
    description = models.TextField()
    comment = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    is_done = models.BooleanField(default=False)


class News(models.Model):
    content = models.TextField()
    creator = models.ForeignKey(to='users.CustomUser', on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['creation_date']


class DaySchedule(models.Model):
    worker = models.ForeignKey(to='users.CustomUser', on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)

    def __str__(self):
        return f'{self.worker}, ${self.start_time}, ${self.end_time}'
