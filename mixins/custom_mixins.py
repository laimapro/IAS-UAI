from django.contrib.auth.mixins import UserPassesTestMixin


class AdminOrCoordinatorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.type == 'COORDINATOR'
