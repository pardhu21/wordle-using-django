from django.shortcuts import render, redirect
from django.contrib import messages

def default(request):
    return redirect('home')

def home(request):
    answer = request.session.get('answer')
    if request.session.get('guess_counter') == None:
        request.session['guess_counter'] = 0
    if answer is None:
        request.session['answer'] = 'WATER'
    for i in range(6):
        temp = request.session.get(str(i))
        if temp is None:
            request.session[str(i)] = [['', ''], ['', ''], ['', ''], ['', ''], ['', '']]
    return render(request, 'Wordle/home.html')

def check_word(request):
    if request.method == 'POST':
        answer = request.session['answer']
        guess = ''
        for i in range(1,6):
            guess += request.POST.get(str(i))
        guess_counter = request.session.get('guess_counter')
        request.session['guess_counter'] += 1
        result = get_result(guess, answer)
        request.session[str(guess_counter)] = result
        check_end(request, guess_counter)
        return redirect('home')

def get_result(guess, answer):
    result = []
    guess = guess.upper()
    answer = answer.upper()
    answer_list = list(enumerate(answer))
    answer_dict = dict((i,j) for i, j in answer_list)
    for i in range(5):
        if answer_dict[i] == guess[i]:
            del answer_dict[i]
            result.append([guess[i], 'green'])
        else:
            result.append([guess[i], 'grey'])
    for i in range(5):
        if guess[i] in answer_dict.values():
            result[i][1] = 'yellow'
            for j in answer_dict:
                if answer_dict[j] == guess[i]:
                    del answer_dict[j]
                    break
    return result
       
def check_end(request, guess_count):
    if check_win(request, guess_count):
        request.session['message'] = 'Correct'
        responses = ['Genius', 'Magnificent', 'Impressive', 'Splendid', 'Great', 'Phew']
        messages.info(request, responses[guess_count])
        return redirect('home')
    if guess_count == 5:
        request.session['message'] = request.session.get('answer').upper()
        return redirect('home')

def check_win(request, guess_count):
    correct_count = 0
    for i in range(5):
        if request.session[str(guess_count)][i][1] == 'green':
            correct_count += 1
    return correct_count == 5


def reset(request):
    try:
        for i in range(6):
            del request.session[str(i)]
        del request.session['guess_counter'], request.session['message'], request.session['answer']
    except:
        return redirect('home')
    return redirect('home')