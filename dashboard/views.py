from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, CreateView, View

from instance.models import InstanceAttemptAnswer, Instance
from project.models import Project
from users.models import Manager
# from post.models import Post
# from job.models import Job, JobCategory
from .models import Contact
from question.models import Category, Question
import pandas as pd
import io


class Home(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_companies'] = Manager.objects.all()[:5]
        # context['latest_jobs'] = Job.objects.all().order_by('-created_at', '-updated_at')[:8]
        # context['latest_posts'] = Post.objects.all().order_by('-created_at', '-updated_at')[:8]
        # context['job_areas'] = JobCategory.objects.all().order_by('title')
        return context


class AboutUs(TemplateView):
    template_name = 'about_us.html'


class SignUpView(TemplateView):
    template_name = "register.html"


class TermsService(TemplateView):
    template_name = "terms_service.html"


class Privacy(TemplateView):
    template_name = "privacy.html"


class Conditions(TemplateView):
    template_name = "conditions.html"


class Research(TemplateView):
    template_name = "research.html"


# class Dashboard(TemplateView):
#     template_name = "dashboard.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['latest_companies'] = Manager.objects.all()[:5]
#         # context['latest_jobs'] = Job.objects.all()[:6]
#         # context['latest_posts'] = Post.objects.all()[:6]
#         return context


# class JobDetail(DetailView):
#     model = Job


class ContactUs(CreateView):
    model = Contact
    fields = ['name', 'email', 'phone', 'message']
    success_url = reverse_lazy('contact_us')


class Dashboard(View):
    template_name = 'dashboard/filtered_reports.html'

    def get_context_data(self, **kwargs):
        context = {}
        user_coordinator = None
        user_manager = None

        if hasattr(self.request.user, 'coordinator'):
            print('Coordinator ID: ', self.request.user.coordinator.id)
            user_coordinator = self.request.user.coordinator
        elif hasattr(self.request.user, 'manager'):
            print('Manager ID: ', self.request.user.manager.id)
            user_manager = self.request.user.manager

        # Filtrando os dados do banco de dados
        queryset = self.get_queryset()
        categories = Category.objects.all()
        instances = Instance.objects.all()

        if user_coordinator:
            projects_user = Project.objects.filter(coordinator=user_coordinator)
            print('User PJ: ', user_coordinator)
            print('Project Manager: ', projects_user)
        if user_manager:
            projects_user = Project.objects.filter(manager=user_manager)
            print('User PJ: ', user_manager)
            print('Project Manager: ', projects_user)

        # Obtendo parâmetros de filtragem
        category_id = self.request.GET.get('category_id')
        correct_option = self.request.GET.get('correct_option')
        instance_id = self.request.GET.get('instance_id')
        participant_id = self.request.GET.get('participant_id')

        # Filtrando os resultados do queryset para incluir apenas os projetos do usuário logado
        if user_coordinator or user_manager:
            queryset = queryset.filter(instance_attempt_id__instance_id__instance_project__in=projects_user)

        # Convertendo os dados em um DataFrame do Pandas
        data = {
            'Participant': [attempt.instance_attempt_id.user_id.name for attempt in queryset],
            'Category': [attempt.question_id.category.title for attempt in queryset],
            'Question': [attempt.question_id.title for attempt in queryset],
            'Option': [attempt.option_id.text for attempt in queryset],
            'Score': [attempt.likert_scale if attempt.option_id.correct else 0 for attempt in queryset],
            'AttemptNumber': [attempt.attempt_number for attempt in queryset]
        }
        df = pd.DataFrame(data)

        context['total_scores'] = df.to_dict(orient='records')
        context['categories'] = categories
        context['instances'] = instances

        return context

    def export_to_excel(self, queryset):
        # Convertendo os dados em um DataFrame do Pandas
        data = {
            'Participant': [attempt.instance_attempt_id.user_id.name for attempt in queryset],
            'Category': [attempt.question_id.category.title for attempt in queryset],
            'Question': [attempt.question_id.title for attempt in queryset],
            'Option': [attempt.option_id.text for attempt in queryset],
            'Score': [attempt.likert_scale if attempt.option_id.correct else 0 for attempt in queryset],
            'AttemptNumber': [attempt.attempt_number for attempt in queryset]  # Incluindo attempt_number
        }
        df = pd.DataFrame(data)

        # Criando um buffer para armazenar o arquivo Excel
        excel_buffer = io.BytesIO()
        df.to_excel(excel_buffer, index=False)
        excel_buffer.seek(0)

        # Retornando o arquivo Excel como resposta HTTP
        response = HttpResponse(excel_buffer,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=filtered_reports.xlsx'
        return response

    def get_queryset(self):
        queryset = InstanceAttemptAnswer.objects.all()

        # Adicione sua lógica de filtragem aqui
        category_id = self.request.GET.get('category_id')
        correct_option = self.request.GET.get('correct_option')
        instance_id = self.request.GET.get('instance_id')
        participant_id = self.request.GET.get('participant_id')

        if category_id:
            queryset = queryset.filter(question_id__category_id=category_id)

        if correct_option in ['True', 'False']:
            queryset = queryset.filter(option_id__correct=correct_option)

        if instance_id:
            queryset = queryset.filter(instance_attempt_id__instance_id=instance_id)

        if participant_id:
            queryset = queryset.filter(instance_attempt_id__user_id=participant_id)

        return queryset

    def get(self, request, *args, **kwargs):
        # Obter os dados filtrados
        queryset = self.get_queryset()

        # Verificar se a exportação para Excel foi solicitada
        if 'export_excel' in request.GET:
            return self.export_to_excel(queryset)

        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)
