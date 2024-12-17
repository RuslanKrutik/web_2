from flask import Blueprint, redirect, render_template, request, url_for, session

lab6 = Blueprint('lab6', __name__)

offices = []
for i in range(1, 11):
    offices.append({"number": i, "tenant": "", "price": 1000 + i % 3})  # Цена аренды

@lab6.route('/lab6/')
def main():
    total_rent = sum(office['price'] for office in offices if office['tenant'] != '')
    return render_template('lab6/lab6.html', offices=offices, total_rent=total_rent)

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data.get('id')

    if data['method'] == 'info':
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': id
        }

    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized',
            },
            'id': id
        }
    
    if data['method'] == 'booking':
        office_number = data['params']
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] != '':
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 2,
                            'message': 'Already booked'
                        },
                        'id': id
                    }
                office['tenant'] = login
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }
    
    if data['method'] == 'cancellation':
        office_number = data['params']
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] == '':
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 3,
                            'message': 'Office is not booked'
                        },
                        'id': id
                    }
                if office['tenant'] != login:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 4,
                            'message': 'Cannot cancel someone else\'s booking'
                        },
                        'id': id
                    }
                office['tenant'] = ''
                return {
                    'jsonrpc': '2.0',
                    'result': 'Cancellation successful',
                    'id': id
                }

    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found',
        },
        'id': id
    }
