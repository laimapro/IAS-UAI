# from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.http import Http404
from django.utils.translation import gettext_lazy as _

from project.models import Project
from users.models import Manager, Participant, Coordinator
from .forms import ParticipantCreationForm, ManagerCreationForm, CoordinatorCreationForm

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.contrib import messages
from django.core.mail import send_mail
from decouple import config
from uuid import UUID

import pdb


class ListCompanies(ListView):
    model = Manager


class DetailCompany(DetailView):
    model = Manager

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(kwargs)
        context['jobs'] = self.object.jobs.all()
        return context


class ListParticipants(ListView):
    model = Participant


class DetailParticipant(DetailView):
    model = Participant

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['mycv'] = self.object.mycv
        # context['language_skills'] = self.object.language_skills.all()
        # context['work_exp'] = self.object.work_experiences.all()
        # context['work_skills'] = self.object.work_skills.all()
        # context['social_skills'] = self.object.social_skills.all()
        # context['other_skills'] = self.object.other_skills.all()
        # context['accommodations'] = self.object.accommodations.all()
        return context


class ParticipantSignUp(CreateView):
    model = Participant
    form_class = ParticipantCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        pj_code = self.kwargs.get('project_id')
        form.instance.pj = Project.objects.get(id=pj_code)
        response = super().form_valid(form)
        # print('PJ CODE: ', pj_code)
        # print('OBJECT: ', self.object)

        self.object.is_active = False
        self.object.save()

        if form.instance.pj:
            activation_link = self.request.build_absolute_uri(
                reverse_lazy('user_activate', kwargs={'user_id': urlsafe_base64_encode(force_bytes(self.object.id)),
                                                      'token': default_token_generator.make_token(self.object)})
            )

            try:
                send_mail(
                    config('EMAIL_SUBJECT_PREFIX'),
                    f'Segue link de ativação: {activation_link}',
                    config('DEFAULT_FROM_EMAIL'),  # E-mail remetente
                    [form.instance.email],  # Lista de destinatários
                    fail_silently=False,  # Defina como True para não gerar exceções em caso de falha
                )
                messages.success(self.request,
                                 'Um e-mail de ativação foi enviado. Por favor, '
                                 'verifique sua caixa de entrada ou spam.')
            except Exception as e:
                print(f"Erro ao enviar o e-mail: {e}")
                messages.error(self.request,
                               'Ocorreu um erro ao enviar o e-mail. Tente novamente mais tarde.')

        return response


class CoordinatorSignUp(CreateView):
    model = Coordinator
    form_class = CoordinatorCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        codigo_projeto = self.kwargs.get('project_id', None)
        # projeto = Project.objects.get(id=codigo_projeto)

        self.object.type = Coordinator.Types.COORDINATOR
        self.object.is_active = False
        self.object.save()

        try:
            projeto = get_object_or_404(Project, id=codigo_projeto)
        except ValueError:
            self.object.delete()
            print('Projeto não encontrado.')
            projeto = None

        # print('PROJETO: ', projeto)
        if projeto:

            # Vincular o coordenador ao projeto
            projeto.coordinator = self.object
            projeto.save()

            activation_link = self.request.build_absolute_uri(
                reverse_lazy('user_activate', kwargs={'user_id': urlsafe_base64_encode(force_bytes(self.object.id)),
                                                      'token': default_token_generator.make_token(self.object)})
            )
            try:
                send_mail(
                    config('EMAIL_SUBJECT_PREFIX'),
                    f'Segue link de ativação: {activation_link}',
                    config('DEFAULT_FROM_EMAIL'),  # E-mail remetente
                    [self.object.email],  # Lista de destinatários
                    fail_silently=False,  # Defina como True para não gerar exceções em caso de falha
                )
                messages.success(self.request,
                                 'Um e-mail de ativação foi enviado. Por favor, verifique sua caixa de entrada ou spam.')
                # print('Um e-mail de ativação foi enviado. Por favor, verifique sua caixa de entrada ou spam.')
            except Exception as e:
                # Se houver algum erro, imprima a mensagem de erro
                print(f"Erro ao enviar o e-mail: {e}")
                messages.error(self.request,
                               'Ocorreu um erro ao enviar o e-mail de ativação. Tente novamente mais tarde.')
        else:
            self.object.delete()
            messages.error(self.request, 'Ocorreu um erro ao criar o objeto. Tente novamente mais tarde.')
            print('Ocorreu um erro ao criar o objeto. Tente novamente mais tarde.')

        return response


class CompanySignUp(CreateView):
    model = Manager
    form_class = ManagerCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        codigo_projeto = self.kwargs.get('project_id', None)

        self.object.type = Manager.Types.COMPANY
        self.object.is_active = False
        self.object.save()

        projeto = Project.objects.get(id=codigo_projeto)
        print('OBJ Projeto: ', projeto)

        if projeto:

            projeto.manager = self.object
            projeto.save()

            activation_link = self.request.build_absolute_uri(
                reverse_lazy('user_activate', kwargs={'user_id': urlsafe_base64_encode(force_bytes(self.object.id)),
                                                      'token': default_token_generator.make_token(self.object)})
            )
            try:
                send_mail(
                    config('EMAIL_SUBJECT_PREFIX'),
                    f'Segue link de ativação: {activation_link}',
                    config('DEFAULT_FROM_EMAIL'),  # E-mail remetente
                    [self.object.email],  # Lista de destinatários
                    fail_silently=False,  # Defina como True para não gerar exceções em caso de falha
                )
                messages.success(self.request,
                                 'Um e-mail de ativação foi enviado. Por favor, verifique sua caixa de entrada ou spam.')
                # print('Um e-mail de ativação foi enviado. Por favor, verifique sua caixa de entrada ou spam.')
            except Exception as e:
                # Se houver algum erro, imprima a mensagem de erro
                print(f"Erro ao enviar o e-mail: {e}")
                messages.error(self.request,
                               'Ocorreu um erro ao enviar o e-mail de ativação. Tente novamente mais tarde.')
        else:
            # Se o projeto não foi encontrado, remova o objeto
            self.object.delete()
            messages.error(self.request, 'Ocorreu um erro ao criar o objeto. Tente novamente mais tarde.')
            print('Ocorreu um erro ao criar o objeto. Tente novamente mais tarde.')

        return response


class UserActivateView(TemplateView):
    template_name = 'users/activate.html'  # Página de sucesso

    def get(self, request, *args, **kwargs):
        my_user = get_user_model()

        try:
            user_id_bytes = urlsafe_base64_decode(kwargs['user_id'])
            user_id_str = user_id_bytes.decode('utf-8')  # Converta bytes para string
            user = my_user.objects.get(id=UUID(user_id_str))
            if default_token_generator.check_token(user, kwargs['token']):
                # Ativar a conta
                user.is_active = True
                user.save()
                messages.success(self.request, 'Ativação realizada com sucesso!')
                return super().get(request, *args, **kwargs)
            else:
                raise Http404("Token inválido.")
        except my_user.DoesNotExist:
            raise Http404("Usuário não encontrado.")


class ParticipantEditView(SuccessMessageMixin, UpdateView):
    model = Participant
    template_name = 'users/participant_edit.html'
    fields = ['name', 'email', 'picture', 'picture_description', 'social_name', 'title_pronoun',
              'gender_identity', 'other_gender', 'sexual_orientation', 'other_orientation',
              'desability', 'other_desability', 'birth_date', 'language']
    success_url = reverse_lazy('participant_edit')
    success_message = _("Profile was updated successfully")

    def get_object(self, *args, **kwargs):
        obj = self.model.objects.get(pk=self.request.user)
        return obj


class CompanyEditView(SuccessMessageMixin, UpdateView):
    model = Manager
    template_name = 'users/manager_edit.html'
    fields = ['language', 'profile_manager', 'social_name', 'title_pronoun', 'phone_manager', 'email_manager', 'is_resp',
              'name', 'picture', 'picture_description', 'banner', 'banner_description', 'email', 'phone'
              ]
    success_url = reverse_lazy('company_edit')
    success_message = _("Profile was updated successfully")

    def get_object(self, *args, **kwargs):
        obj = self.model.objects.get(pk=self.request.user)
        return obj


class CoordinatorEditView(SuccessMessageMixin, UpdateView):
    model = Coordinator
    template_name = 'users/coordinator_edit.html'
    fields = ['language', 'social_name','name', 'email', 'picture', 'picture_description',
              'social_name', 'title_pronoun', 'gender_identity', 'other_gender', 'sexual_orientation',
              'other_orientation', 'desability', 'other_desability',
              ]
    success_url = reverse_lazy('coordinator_edit')
    success_message = _("Profile was updated successfully")

    def get_object(self, *args, **kwargs):
        obj = self.model.objects.get(pk=self.request.user)
        return obj
