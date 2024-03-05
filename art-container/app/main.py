from flask import Flask, request, Response
from art import text2art
from os import environ
import socket
import jwt
import json
import requests
import base64

app = Flask(__name__)

GREETING = environ.get("GREETING", "Welcome")
MIRROR_REQ = environ.get("MIRROR_REQ", None)
HOSTNAME = socket.gethostname()
REGION = environ.get("REGION", "eu-central-1")


def get_ip():
    # Taken from https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('169.254.169.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


IPADDR = socket.gethostbyname(get_ip())


def decode_amzn_oidc_data(oidc_header_data):
    jwt_headers = oidc_header_data.split('.')[0]
    decoded_jwt_headers = base64.b64decode(jwt_headers)
    decoded_jwt_headers = decoded_jwt_headers.decode("utf-8")
    decoded_json = json.loads(decoded_jwt_headers)
    return decoded_json['kid']


def get_alb_pub_key(kid):
    url = 'https://public-keys.auth.elb.' + REGION + '.amazonaws.com/' + kid
    req = requests.get(url)
    pub_key = req.text

    return pub_key


def get_ava_pub_key(kid):
    url = 'https://public-keys.prod.verified-access.' + \
        REGION + '.amazonaws.com/' + kid
    req = requests.get(url)
    pub_key = req.text

    return pub_key


def keywords(keyword):
    if not keyword:
        return "missing data"
    if keyword.find("echo") >= 0:
        return "Hallo Otto"
    return keyword


@app.route("/", defaults={'u_path': ''})
@app.route('/<path:u_path>', methods=['GET', 'POST'])
def rootpath(u_path):
    if u_path:
        artstring = text2art(u_path, font="starwars")
    else:
        artstring = text2art(GREETING, font="starwars")

    if u_path == "custom":
        if not request.data:
            errorstr = text2art("missing data", font="starwars")
            return Response(errorstr, mimetype='text')
        data = request.get_json()
        customtext = keywords(data.get("text", None))
        artstring = text2art(customtext, font="starwars")

    retstring = "{}\nmy-hostname: {}".format(artstring, HOSTNAME)
    retstring = "{}\nmy-ip:       {}".format(retstring, IPADDR)

    if MIRROR_REQ:
        retstring = "{}\n\nrequest-headers:\n\n{}".format(retstring,
                                                          request.headers)
        retstring = "{}\n\nrequest-data:\n\n{}".format(retstring,
                                                       request.data)

        amzn_oidc_data = request.headers.get('x-amzn-oidc-data', None)
        amzn_ava_data = request.headers.get('x-amzn-ava-user-context', None)

        if amzn_oidc_data:
            kid = decode_amzn_oidc_data(amzn_oidc_data)
            pub_key = get_alb_pub_key(kid)
            payload = jwt.decode(amzn_oidc_data, pub_key, algorithms=['ES256'])
            payload = json.dumps(payload, indent=4)

            retstring = "{}\n\ndecoded_oidc_payload:\n\n{}".format(retstring,
                                                                   payload)
        if amzn_ava_data:
            kid = decode_amzn_oidc_data(amzn_ava_data)
            pub_key = get_ava_pub_key(kid)
            payload = jwt.decode(amzn_ava_data, pub_key, algorithms=['ES384'])
            payload = json.dumps(payload, indent=4)

            retstring = "{}\n\ndecoded_ava_payload:\n\n{}".format(retstring,
                                                                  payload)
        retstring = "{}\n\n".format(retstring)

    # Fetch content from lattice service with error handling
    try:
        external_response = requests.get('<https://YourLatticeServiceDomain.com>')
        external_response.raise_for_status()
        external_content = external_response.text
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the request
        external_content = f"Error fetching content: The Amazon VPC Lattice is not reachable"

    # Add fetched content to the response
    retstring += f"\n\nContent from Amazon VPC Lattice service:\n\n{external_content}"

    return Response(retstring, mimetype='text')


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
