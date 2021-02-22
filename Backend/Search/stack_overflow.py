from flask import Blueprint, render_template, request
from urllib.parse import quote_plus
import collections
import requests
import time
import json

stack_search_bp = Blueprint('stack_search__bp', __name__, template_folder='templates', static_folder='static')

"""
Returns the html from the templates directory
"""


@stack_search_bp.route('/')
def dashboard():
    """main drop page"""
    return render_template('home.html')


"""
Endpoint expects to be given one parameter from client
@query:    The desired tag to be scraped from stack overflow
Returns JSON array of posts, comments, votes etc
Default behaviour is merged list of top 10 and 10 most recent about the 
tag sorted by date
"""


# need to then fire off request to get top comments
# need to then merge comments and posts base on id
# need to then sort by datetime

@stack_search_bp.route('/Api/Search', methods=['POST'])
def search():
    begin = time.perf_counter()
    all_endpoints = [
        'https://api.stackexchange.com/2.2/search?pagesize=10&order=desc&sort=votes&'
        'site=stackoverflow&filter=!-n6SGLukb7szTV*u97CGO4G*x6qBoM)dlfqXq9LK5YwvLJSJ)akXRZ',
        'https://api.stackexchange.com/2.2/search?pagesize=10&order=desc&sort=creation&'
        'site=stackoverflow&filter=!-n6SGLukb7szTV*u97CGO4G*x6qBoM)dlfqXq9LK5YwvLJSJ)akXRZ'
    ]

    comment_base_endpoint = 'https://api.stackexchange.com/2.2/questions/'
    comment_post_endpoint = 'https://api.stackexchange.com/2.2/posts/'
    post_map = {}
    post_comm_map = collections.defaultdict(list)
    session = requests.Session()

    try:
        parameters = json.loads(request.form['query'])
        """
        parameters = {
            'query': 'java'
        }
        """
        # Generate finished endpoints for pulling 10 most recent and 10 most voted posts with tag
        for index in range(len(all_endpoints)):
            all_endpoints[index] = all_endpoints[index] + '&tagged=' + quote_plus(parameters)

        all_requests = [
            session.get(all_endpoints[0]),
            session.get(all_endpoints[1])
        ]

        for response in all_requests:  # iterate through all results of requests
            for post in response.json()['items']:  # iterate through all travel times for all restaurants
                comment_post_endpoint += str(post['question_id']) + ';'

        if comment_post_endpoint.endswith(';'):
            comment_post_endpoint = comment_post_endpoint[:-1]

        comment_post_endpoint += '/comments?pagesize=100&order=asc&sort=votes&site=stackoverflow&filter=!)Q2B_A497ZZ6FysK)6.gj97w'
        post_comm_req = session.get(comment_post_endpoint).json()['items']

        for item in post_comm_req:
            post_comm_map[item['post_id']].append({
                'created': item['creation_date'],
                'score': item['score'],
                'body': item['body_markdown']
            })

        for response in all_requests:  # iterate through all results of requests
            for index in range(len(response.json()['items'])):  # iterate through all travel times for all restaurants
                post = response.json()['items'][index]
                post_map[post['question_id']] = {
                    'created': post['creation_date'],
                    'score': post['score'],
                    'title': post['title'],
                    'body': post['body_markdown'],
                    'comments': post_comm_map[post['question_id']],
                    'solutions': {},
                }
                comment_base_endpoint += str(post['question_id']) + ';'  # generate url with all id for comment retrieval

        if comment_base_endpoint.endswith(';'):
            comment_base_endpoint = comment_base_endpoint[:-1]

        comment_base_endpoint += '/answers?pagesize=100&order=desc&sort=votes&site=stackoverflow&' \
                                 'filter=!*cCFgu5yS6rFkETtKY*uE)R5KPhWwQFDGF6Qa'
        comments = session.get(comment_base_endpoint)

        for comment in comments.json()['items']:
            if comment['is_accepted'] is True:
                comment_array = []
                if 'comments' in comment and len(comment['comments']) > 0:  # we have comments on the answer
                    for com in comment['comments']:
                        comment_array.append({
                            'created': com['creation_date'],
                            'score': com['score'],
                            'body': com['body_markdown']
                        })

                post_map[comment['question_id']]['solutions'] = {
                    'body': comment['body_markdown'],
                    'score': comment['score'],
                    'created': comment['creation_date'],
                    'comments': comment_array
                }
    except Exception as e:
        print(str(e))
        return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

    return post_map
