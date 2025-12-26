from django.db.models import Manager, Q


class DocumentManager(Manager):

    def search(self, **kwargs):
        s = kwargs.get('s', None)
        q_and = Q()
        if s:
            q = Q(
                Q(title__icontains=s) |
                Q(description__icontains=s) |
                Q(file_name__icontains=s)
            )
            q_and &= q

        return self.get_queryset().filter(q_and)
