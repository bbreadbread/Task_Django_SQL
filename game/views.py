from django.shortcuts import render, redirect
from random import randint
from .models import Users, Records
from datetime import datetime

def index(request):
    # Получаем 5 последних посетителей
    last_visitors = Users.objects.order_by('-DateOfVisit')[:5]
    
    if request.method == 'POST':
        player_name = request.POST.get('player_name')
        if player_name:
            # Создаем/обновляем пользователя
            user, created = Users.objects.get_or_create(
                Name=player_name,
                defaults={'DateOfVisit': datetime.now()}
            )
            if not created:
                user.DateOfVisit = datetime.now()
                user.save()
            
            request.session['player_name'] = player_name
            return redirect('game')
    
    return render(request, 'game/index.html', {
        'last_visitors': last_visitors
    })

def game_view(request):
    # Инициализация игры
    if 'target_number' not in request.session:
        request.session['target_number'] = randint(1, 100)
        request.session['attempts'] = 0
    
    # Обработка попытки
    message = None
    if request.method == 'POST':
        if 'restart' in request.POST:
            # Сброс игры без редиректа
            request.session['target_number'] = randint(1, 100)
            request.session['attempts'] = 0
            return redirect('game')
        
        guess = int(request.POST.get('guess', 0))
        request.session['attempts'] += 1
        
        if guess == request.session['target_number']:
            # Сохраняем результат
            user = Users.objects.get(Name=request.session['player_name'])
            Records.objects.create(
                user=user,
                NumberOfAttempts=request.session['attempts']
            )
            
            message = f"Поздравляем, {user.Name}! Вы угадали число {guess} за {request.session['attempts']} попыток."
            del request.session['target_number']
            del request.session['attempts']
        elif guess < request.session['target_number']:
            message = f"Число больше {guess}"
        else:
            message = f"Число меньше {guess}"
    
    # Получаем топ-5 результатов
    records_data = Records.objects.select_related('user').order_by('NumberOfAttempts')[:5]
    
    return render(request, 'game/game.html', {
        'player_name': request.session.get('player_name', 'Гость'),
        'message': message,
        'records_data': records_data
    })

def privacy(request):
    return render(request, 'game/privacy.html')