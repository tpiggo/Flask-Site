from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from shop.models import Person, Grocerystore, Hardwarestore, Appearlstore, shop_db
from shop.utils.person_data_parser import post_parser
from shop.utils.store_data_parser import get_searched_data

shop = Blueprint(
    'shop',
    __name__,
    static_folder='static',
    template_folder='templates'
)

type_of_store = ["appearlstore", "hardwarestore", "grocerystore"]

@shop.route('/home')
@shop.route('/')
def index():
    if request.args.get('navsearch') is not None:
        data = request.args.get('navsearch')
        return redirect(url_for('search', navsearch=data))
    return render_template('shop_index.html')


@shop.route('/search', methods=["GET", "POST"])
def search(data=None):
    # Handling search page get.
    print('Started the search page.')
    # We send data to this page using the navsearch. We know the data_passed
    # will be in the navsearch argument.
    if request.args.get('navsearch') is not None:
        data = request.args.get('navsearch')
    elif data is None:
        data = 'No search was received'
    return render_template('search.html', string=data)

#Rotue for the person search. The search is synchronous.
@shop.route('/people', methods=["GET", "POST"])
def search_people(person=None, people=None):
    print('Starting search page!')
    if request.method == 'POST':
        print('Handling POST')
        people = post_parser(
            content=request.form.get('content'),
            type_of=request.form.get('type_of')
        )

        # Checking if type of people is a person or not. If it is not,
        # it will be iterable. If it is, set people to None and Person is to
        # be used. Otherwise, Person is None.
        if people == []:
            person = None
            people = None
        elif type(people) == Person:
            person = people
            people = None
        # render the template from the post request.
        return render_template(
            'people.html',
            people=people,
            person=person
        )
    elif request.args.get('navsearch') is not None:
        # Handling the seach bar search.
        data = request.args.get('navsearch')
        return redirect(url_for('search', navsearch=data))
    # Getting all the entries of the database of people
    people = Person.query.order_by(Person.id).all()
    return render_template('people.html', people=people, person=person)

# Route for rendering the first page of the store data.
@shop.route('/purchases', methods=['GET'])
def purchases_page():
    if request.args.get('navsearch') is not None:
        data = request.args.get('navsearch')
        return redirect(url_for('search', navsearch=data))
    return render_template('purchases.html')

# Async route for retrieving the data about companies.
@shop.route('/get-purchases', methods=["POST"])
def search_purchases():
    print(request.json)
    data = []
    if (request.json['store_selector'] == "all"):
        for store in type_of_store:
            data += get_searched_data(
                store,
                request.json['input_for_sorting'],
                request.json['type_select']
                )
    else:
        data = get_searched_data(
            request.json['store_selector'],
            request.json['input_for_sorting'],
            request.json['type_select']
            )
    # Return the list of elements to the front end.
    return jsonify(response = data)