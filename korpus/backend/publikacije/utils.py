from .models import FajlPublikacije


def renumber_files(pub_id):
    files = FajlPublikacije.objects.filter(publikacija_id=pub_id).order_by('redni_broj')
    for i, f in enumerate(files):
        f.redni_broj = i + 1
        f.save()
