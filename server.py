from flask import Flask, render_template,request,session,redirect
import random
from datetime import datetime
app = Flask(__name__)
app.secret_key = "Life Is Good."
@app.route('/')
def index():
    if "total_gold" not in session:
        session["total_gold"] = 0
    if 'activities' not in session:
        session['activities']= []
    return render_template('index.html',total_gold=session['total_gold'],activities=session['activities'])



def new_activities(activity):
    current_date_time =datetime.now().strftime("%m-%d-%Y %-I:%M %p")
    formatted_activity = f"{activity} ({current_date_time})"
    session['activities'].append(formatted_activity)

@app.route('/farm')
def farm():
    gold_earn = random.randint(10,20)
    session['total_gold'] += gold_earn
    new_activities(f'Earned {gold_earn} golds from the farm!')
    return render_template('farm.html',gold_earn=gold_earn,total_gold= session['total_gold'])
@app.route('/cave')
def cave():
    gold_earn = random.randint(5,10)
    session['total_gold'] += gold_earn
    new_activities(f'Earned {gold_earn} golds from the cave!')
    return render_template('cave.html',gold_earn=gold_earn,total_gold= session['total_gold'])
@app.route('/house')
def house():
    gold_earn = random.randint(2,5)
    session['total_gold'] += gold_earn
    new_activities(f'Earned {gold_earn} golds from the house!')
    return render_template('house.html',gold_earn=gold_earn,total_gold= session['total_gold'])

@app.route('/casino')
def casino():
    gold_earn = random.choice(list(range(0, 50)))
    gold_lose = random.choice(list(range(0, 50)))
    item = [gold_earn,gold_lose]
    random_choice = random.choice(item)
    new_activities(f'Earned {gold_earn} golds from casino!' if random_choice==gold_earn else f"Entered a casino and lost {gold_lose} golds.... Ouch!!")
    session['total_gold'] += gold_earn
    session['total_gold'] -= gold_lose
    return render_template('casino.html',gold_earn=gold_earn,gold_lose=gold_lose,random_choice=random_choice,total_gold=session['total_gold'],activities=session['activities'])
@app.route('/process_money', methods=['POST'])
def process_money():
    location = request.form.get('location')
    gold_earn = 0
    gold_lose = 0
    if location == 'farm':
        gold_earn = random.randint(10,20)
        new_activities(f'Earned {gold_earn} gold from the farm!')
    elif location == 'cave':
        gold_earn = random.randint(5,10)
        new_activities(f'Earned {gold_earn} gold from the cave!')
    elif location == 'house':
        gold_earn = random.randint(2,5)
        new_activities(f'Earned {gold_earn} gold from the house!')
    elif location == 'casino':
        redirect('/casino')
        
    session['total_gold']+= gold_earn
    session['total_gold']-= gold_lose
    return redirect('/')

@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True,port=5001)