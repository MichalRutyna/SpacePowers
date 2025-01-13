from django.shortcuts import render


def base(request):
    context = {'nations': [
        {
            'name': "Anglia",
        },
        {
            'name': "Brazil",
        },
    ],
    }
    return render(request, 'base.html', context)
