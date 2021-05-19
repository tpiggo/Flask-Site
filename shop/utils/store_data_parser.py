from shop.models import Hardwarestore, Grocerystore, Appearlstore

# Utility function for accessing the tables about the store data.
def get_searched_data(store, search, input_type):
    # get the store type
    t_store = Appearlstore
    returnable_data = []
    if store == "hardwarestore":
        t_store = Hardwarestore
    elif store == "grocerystore":
        t_store = Grocerystore
    
    # Get the internal data
    if input_type == "purchase_id":
        returnable_data = [t_store.query.get(int(search)).get_as_dict()]
    elif input_type == "purchase_amount":
        data = t_store.query.filter_by(amount=float(search)).all()
        returnable_data = [ret.get_as_dict() for ret in data]
    else:
        search = search.capitalize()
        data = t_store.query.filter_by(type_of_payment=search).all()
        returnable_data = [ret.get_as_dict() for ret in data]
    return returnable_data