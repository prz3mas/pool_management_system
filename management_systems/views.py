from django.shortcuts import render
from django.views.generic import ListView, TemplateView, CreateView, DeleteView, UpdateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.urls.exceptions import Resolver404
from django.http import HttpResponseRedirect
from .models import PoolEntrance, News, Task, DaySchedule
from django import forms
from users.models import CustomUser
from datetime import datetime


class PendingServicesListView(LoginRequiredMixin, ListView):
    model = PoolEntrance
    queryset = PoolEntrance.objects.filter(additional_service__isnull=False, leave_date__isnull=True)
    template_name = 'management_systems/pendingservice_list.html'

    def dispatch(self, request, *args, **kwargs):
        #print(request.user.get_user_type_display() == 'instruktor_pływania')
        if request.user.get_user_type_display() != 'masażysta' and \
                request.user.get_user_type_display() != 'instruktor pływania':
            raise PermissionDenied('Brak dostępu.')
        return super(PendingServicesListView, self).dispatch(request, *args, **kwargs)


class TaskAddCommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    success_url = reverse_lazy('task-list')
    fields = ['comment']
    template_name = 'management_systems/task_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.get_user_type_display() != 'sprzątaczka' and \
                request.user.get_user_type_display() != 'konserwator':
            raise PermissionDenied('Brak dostępu.')
        return super(TaskAddCommentUpdateView, self).dispatch(request, *args, **kwargs)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('task-list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.get_user_type_display() is not 'kierownik':
            raise PermissionDenied('Brak dostępu.')
        return super(TaskDeleteView, self).dispatch(request, *args, **kwargs)


class AddTaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    success_url = reverse_lazy('task-list')
    fields = ['responsible_person', 'description']

    def get_form(self, form_class=None):
        form = super(AddTaskCreateView, self).get_form()
        form.fields['responsible_person'].queryset = CustomUser.objects.exclude(user_type__in=[1, 6])
        return form

    def dispatch(self, request, *args, **kwargs):
        if request.user.get_user_type_display() is not 'kierownik' and \
                request.user.get_user_type_display() is not 'recepcjonistka':
            raise PermissionDenied('Tylko kierownik może dodawać newsy.')
        return super(AddTaskCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class TaskListView(LoginRequiredMixin, ListView):
    model = Task


class ArchivePoolEntranceListView(LoginRequiredMixin, ListView):
    model = PoolEntrance
    queryset = PoolEntrance.objects.filter(leave_date__isnull=False)

    def dispatch(self, request, *args, **kwargs):
        if request.user.get_user_type_display() is not 'recepcjonistka' and \
                request.user.get_user_type_display() is not 'kierownik':
            raise PermissionDenied('Brak dostępu.')
        return super(ArchivePoolEntranceListView, self).dispatch(request, *args, **kwargs)


class PoolEntranceListView(LoginRequiredMixin, ListView):
    model = PoolEntrance
    queryset = PoolEntrance.objects.filter(leave_date__isnull=True)

    def dispatch(self, request, *args, **kwargs):
        if request.user.get_user_type_display() is not 'recepcjonistka' and \
                request.user.get_user_type_display() is not 'kierownik':
            raise PermissionDenied('Brak dostępu.')
        return super(PoolEntranceListView, self).dispatch(request, *args, **kwargs)


class PoolEntranceCreateView(LoginRequiredMixin, CreateView):
    model = PoolEntrance
    template_name = 'management_systems/poolentrance_form.html'
    fields = ['first_name', 'last_name', 'permission_for', 'additional_service']

    def get_success_url(self):
        return reverse('pool-management')

    def dispatch(self, request, *args, **kwargs):
        if request.user.get_user_type_display() is not 'recepcjonistka' and \
                request.user.get_user_type_display() is not 'kierownik':
            raise PermissionDenied('Brak dostępu.')
        return super(PoolEntranceCreateView, self).dispatch(request, *args, **kwargs)


class PoolEntranceUpdateView(LoginRequiredMixin, UpdateView):
    model = PoolEntrance
    fields = ['first_name', 'last_name', 'additional_service', 'leave_date']
    template_name = 'management_systems/poolentrance_update_form.html'

    def get_success_url(self):
        return reverse_lazy('pool-management')

    def dispatch(self, request, *args, **kwargs):
        if request.user.get_user_type_display() is not 'recepcjonistka' and \
                request.user.get_user_type_display() is not 'kierownik':
            raise PermissionDenied('Brak dostępu.')
        return super(PoolEntranceUpdateView, self).dispatch(request, *args, **kwargs)


class PoolEntranceDeleteView(LoginRequiredMixin, DeleteView):
    model = PoolEntrance
    success_url = reverse_lazy('pool-management')

    def dispatch(self, request, *args, **kwargs):
        if request.user.get_user_type_display() is not 'recepcjonistka' and \
                request.user.get_user_type_display() is not 'kierownik':
            raise PermissionDenied('Brak dostępu.')
        return super(PoolEntranceDeleteView, self).dispatch(request, *args, **kwargs)


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'management_systems/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logged_user_data'] = CustomUser.objects.get(id=self.request.user.id)
        context['messages'] = News.objects.all()
        return context


class NewsCreateView(LoginRequiredMixin, CreateView):
    model = News
    template_name = 'management_systems/news_form.html'
    fields = ['content']

    def get_success_url(self):
        return reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.get_user_type_display() is not 'kierownik':
            raise PermissionDenied('Tylko kierownik może dodawać newsy.')
        return super(NewsCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class WorkerWeeklyScheduleListView(LoginRequiredMixin, ListView):
    model = DaySchedule

    def get_queryset(self):
        today_day_num = datetime.now().weekday()
        actual_date = str(datetime.now().date()).split('-')
        year = int(actual_date[0])
        month = int(actual_date[1])
        day = int(actual_date[2])

        if today_day_num == 0:
            queryset = DaySchedule.objects.filter(worker=self.request.user, start_time__gte=datetime(year, month, day),
                                                  start_time__lte=datetime(year, month, day + 7))
            for day in queryset:
                day.day_number = day.start_time.weekday()

        else:
            diff_to_monday = today_day_num
            days_till_monday = day - diff_to_monday
            queryset = DaySchedule.objects.filter(worker=self.request.user,
                                                  start_time__gte=datetime(year, month, days_till_monday),
                                                  start_time__lte=datetime(year, month, days_till_monday + 7))

            for day in queryset:
                day.day_number = day.start_time.weekday()

        return queryset


class WorkerDayScheduleCreateView(LoginRequiredMixin, CreateView):
    fields = ['worker', 'start_time', 'end_time']
    model = DaySchedule

    def get_success_url(self):
        return reverse('pool-management')

    def dispatch(self, request, *args, **kwargs):
        if request.user.get_user_type_display() is not 'kierownik':
            raise PermissionDenied('Tylko kierownik może dodawać grafik.')
        return super(WorkerDayScheduleCreateView, self).dispatch(request, *args, **kwargs)


def close_visit(request, pk=None):
    try:
        record = PoolEntrance.objects.get(id=pk)
        record.leave_date = datetime.now()
        record.save()
        return HttpResponseRedirect(reverse('pool-management'))
    except ObjectDoesNotExist:
        raise Resolver404("Podano błędne id")


def change_task_status(request, pk=None):
    try:
        task = Task.objects.get(id=pk)
        task.is_done = not task.is_done
        task.save()
        return HttpResponseRedirect(reverse('task-list'))
    except ObjectDoesNotExist:
        raise Resolver404('Podano błędne id')


def complete_service(request, pk=None):
    try:
        service = PoolEntrance.objects.get(id=pk)
        service.leave_date = datetime.now()
        service.save()
        return HttpResponseRedirect(reverse('pending-services'))
    except ObjectDoesNotExist:
        raise Resolver404('Podano błędne id')
