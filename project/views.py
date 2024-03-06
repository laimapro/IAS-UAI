from django.shortcuts import render, redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from decouple import config
from django.contrib import messages
from django.utils.html import strip_tags

from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import InvitationForm, ParticipantInvitationForm
from mixins.custom_mixins import AdminOrCoordinatorRequiredMixin
from .models import Project
from instance.models import InstanceAttempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View


class CreateProjectView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Project
    fields = ['pj_name', 'pj_code']
    success_url = reverse_lazy('pj_list')
    success_message = "Project was created successfully"


class ListProjects(LoginRequiredMixin, ListView):
    model = Project
    # template_name = 'job/question_list.html'
    # paginate_by = 10
    # ordering = ['-id']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Project.objects.all()
        else:
            if user.type == 'COMPANY':
                queryset = Project.objects.filter(manager=user)
                return queryset.distinct()
            elif user.type == 'COORDINATOR':
                queryset = Project.objects.filter(coordinator=user)
                return queryset.distinct()
            elif user.type == 'PARTICIPANT':
                queryset = Project.objects.filter(id=user.participant.pj.id)
                return queryset.distinct()
            else:
                return Project.objects.none()


class DetailProject(LoginRequiredMixin, DetailView):
    model = Project
    context_object_name = 'obj'

    def get_object(self, queryset=None):
        # Use o UUID da URL para buscar o objeto correto
        uuid_str = self.kwargs.get('id')
        obj = get_object_or_404(self.model, id=uuid_str)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        instances = self.object.instances.all()
        instances_with_question_count = []

        for instance in instances:
            # question_count = QuestionInstance.objects.filter(instance_pj=instance).count()
            finished_instance = InstanceAttempt.objects.filter(user_id=user, instance_id=instance).first()
            instances_with_question_count.append((instance, finished_instance))

        context['instances_with_question_count'] = instances_with_question_count

        participants = self.object.user_project.all()
        context['participants'] = participants

        return context


class EditProject(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Project
    fields = ['pj_name', 'pj_code']
    success_url = reverse_lazy('pj_list')
    success_message = "Project was updated successfully"


class DeleteProject(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Project
    fields = ['pj_name', 'pj_code']
    success_url = reverse_lazy('list_projects')
    success_message = "Project was deleted successfully"


class InvitationView(LoginRequiredMixin, AdminOrCoordinatorRequiredMixin, View):
    template_name = 'project/project_invitation.html'

    def get_success_url(self):
        # Lógica para determinar o success_url
        project_id = self.kwargs.get('id')
        project_type = self.kwargs.get('type')
        return reverse_lazy('pj_invitation', kwargs={'type': project_type, 'id': project_id})

    def get(self, request, *args, **kwargs):
        project_id = kwargs.get('id')
        project_type = kwargs.get('type')
        form = InvitationForm(initial={'project_id': project_id, 'project_type': project_type})
        # print(kwargs)
        print(project_type)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = InvitationForm(request.POST)
        path_name = None
        if form.is_valid():
            print('Form válido')
            email = form.cleaned_data['email']
            project_id = form.cleaned_data['project_id']
            project_type = form.cleaned_data['project_type']

            if project_type == 1:
                path_name = 'coordinator_signup'
            elif project_type == 2:
                path_name = 'company_signup'

            invitation_link = self.request.build_absolute_uri(
                reverse_lazy(path_name, kwargs={'project_id': project_id})
            )
            # print(invitation_link)
            try:
                template_path = 'project/invite_message.html'
                template_data = {'invitation_link': invitation_link}
                html_message = render_to_string(template_path, template_data)
                plain_message = strip_tags(html_message)
                subject = config('EMAIL_SUBJECT_PREFIX')
                from_email = config('DEFAULT_FROM_EMAIL')
                recipient_list = [email]

                send_mail(
                    subject,
                    plain_message,  # Corpo do e-mail em texto puro
                    from_email,
                    recipient_list,
                    html_message=html_message,
                    fail_silently=False,
                )
                messages.success(self.request,
                                 f'Um convite foi enviado para o e-mail {email}.')
                # print('Um e-mail de ativação foi enviado. Por favor, verifique sua caixa de entrada ou spam.')
            except Exception as e:
                # Se houver algum erro, imprima a mensagem de erro
                print(f"Erro ao enviar o e-mail: {e}")
                messages.error(self.request,
                               'Ocorreu um erro ao enviar o e-mail. Tente novamente mais tarde.')

            return redirect(self.get_success_url())
        else:
            messages.error(request, 'Formulário inválido!')
            print('Formulário inválido!')
            return render(request, self.template_name, {'form': form})


class ParticipantInvitationView(LoginRequiredMixin, View):
    template_name = 'project/participant_invitation.html'

    def get_success_url(self):
        project_id = self.kwargs.get('id')
        return reverse_lazy('pj_invite', kwargs={'id': project_id})

    def get(self, request, *args, **kwargs):
        project_id = kwargs.get('id')
        form = ParticipantInvitationForm(initial={'project_id': project_id})
        # print(kwargs)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ParticipantInvitationForm(request.POST)

        if form.is_valid():
            print('Form válido')
            email = form.cleaned_data['email']
            project_id = form.cleaned_data['project_id']

            invitation_link = self.request.build_absolute_uri(
                reverse_lazy('participant_signup', kwargs={'project_id': project_id})
            )
            # print(invitation_link)
            try:
                template_path = 'project/invite_message.html'
                template_data = {'invitation_link': invitation_link}
                html_message = render_to_string(template_path, template_data)
                plain_message = strip_tags(html_message)
                subject = config('EMAIL_SUBJECT_PREFIX')
                from_email = config('DEFAULT_FROM_EMAIL')
                recipient_list = [email]

                send_mail(
                    subject,
                    plain_message,  # Corpo do e-mail em texto puro
                    from_email,
                    recipient_list,
                    html_message=html_message,
                    fail_silently=False,
                )
                messages.success(self.request,
                                 f'Um convite foi enviado para o e-mail {email}.')
            except Exception as e:
                print(f"Erro ao enviar o e-mail: {e}")
                messages.error(self.request,
                               'Ocorreu um erro ao enviar o e-mail de ativação. Tente novamente mais tarde.')
            return redirect(self.get_success_url())
        else:
            messages.error(request, 'Formulário inválido!')
            print('Formulário inválido!')
            return render(request, self.template_name, {'form': form})
