from shop.models import Person
import re

# Need to hav the r for pattern matching in Python. Note to self
# Delete this note later
url_validation = r'[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'


def email_parser(content=None, people=None):
    # Parsing the content string for email query which can be handled multiple
    # different ways depending on the input string.
    print('Starting email parser. ')
    if content.startswith("@"):
        # From this we know we are looking an email url!
        # TODO: Think about maybe checking if the URL is a good url?
        people = Person.query.filter(Person.email.endswith(content)).all()
    elif re.match(url_validation, content) is not None:
        # Checking if the string is a URL since it did not start with @ symbol
        # TODO: Use potentially different retrieval method since the email
        # could be .com.somethingelse <-- search for these!
        people = Person.query.filter(Person.email.endswith(content)).all()
    elif '@' in content:
        # Split the string in order to get components
        if len(re.split('@', content)) == 2:
            print("Is normal email. Searching for it directly")
            people = Person.query.filter_by(email=content).all()
    else:
        print("Does not meet perameterization requirements. Returning None")
    return people


def proper_date(date_string=''):
    date_split = re.split('-', date_string)
    if len(date_split) == 3 and len(date_split[0]) == 4:
        return True
    elif len(date_split) == 3 and len(date_split[0]) == 2:
        # Date is missing leading century digits. Get mad.
        print('Dates must be in form 19XX or 20XX. Please try again.')
    else:
        print('Multiple problems with date. Try again.')
    return False


def date_range_parser(date_string='', split='', people=None):
    date_range = re.split(split, date_string)
    if proper_date(date_string=date_range[0]) and proper_date(date_string=date_range[1]):
        people = Person.query.filter(
            Person.date_of_birth >= date_range[0],
            Person.date_of_birth < date_range[1]
        ).all()
        print(people)
    return people


def date_parser(content='', people=None):
    print('Date parser started')
    # We want to be able to search dates of birth. Equal to or between for
    # for good functionality
    if content == '':
        # Nothing to do here, there was an error in data collection
        pass
    else:
        # We want to check if it is a date OR it is range of dates.
        # Parameterize the range statement to either TO, AND, /.
        content = content.upper()
        print('Content is:', content)
        if 'AND' in content:
            # Parse date range
            people = date_range_parser(content, ' AND ')
        elif '/' in content:
            # Parse date range
            people = date_range_parser(content, '/')
        elif 'TO' in content:
            # parse date range
            people = date_range_parser(content, ' TO ')
        # otherwise this is not a date range. Is a date, validate that it is.
        else:
            # Checking if the date is in the proper format.
            if proper_date(date_string=content):
                people = Person.query.filter_by(date_of_birth=content).all()
    return people


def post_parser(content='', type_of='none'):
    # Only need to have people since the .all() function in query will return
    # nothing if there is no people available. We will deal with the Person
    # return type in the main app script.
    # TODO Could possibly throw errors/send error messages to direct people
    # where they are going on with their search. Or use popup windows and keep
    # the table as the background.
    # TODO maybe combine all instances of autocap if's into 1 if which
    # autocaps. Nested if for autocap reuse
    people = None
    # checking what type we are looking for
    if content == '' or type_of == 'none':
        # Do nothing. Return the database table
        if (content == ''):
            print('No content passed.')
        else:
            print('Handling None query.')
        people = Person.query.order_by(Person.id).all()
    elif type_of == 'id':
        # check if the string is numeric, if so, proceed if not return nothing.
        print("Handling ID query.")
        if(content.isnumeric()):
            people = Person.query.filter_by(id=content).all()
        else:
            print('Is not a number! Please try again.')
    elif type_of == 'full_name':
        print("Handling Full Name query.")
        # splitting the data taken in by space
        # TODO: set up autocapitalization on the first letters of every new
        # word.
        search_split = re.split(' ', content)
        if len(search_split) == 2:
            # Get the person/people (unlikely) by filtering both the first and
            # last names.
            people = Person.query.filter_by(
                first_name=search_split[0]
            ).filter_by(last_name=search_split[1]).all()
        else:
            # TODO Name is non-standard first and/or last names
            print("Need to fix how we parse names.")
    elif type_of == 'first_name':
        # No data parsing to be done here, just search the first names for
        # match
        # TODO: set up autocapitalization on the first letters of every new
        # word.
        people = Person.query.filter_by(first_name=content).all()
    elif type_of == 'last_name':
        # No data parsing to be done here, just search the last names for match
        # TODO: set up autocapitalization on the first letters of every new
        # word.
        people = Person.query.filter_by(last_name=content).all()
    elif type_of == 'email':
        # Piping the request to the email parser
        print("Handling Email query.")
        people = email_parser(content=content)
    elif type_of == 'country':
        # TODO autocap again here
        people = Person.query.filter_by(country_of_birth=content).all()
    elif type_of == 'date_birth':
        people = date_parser(content=content)
    return people
