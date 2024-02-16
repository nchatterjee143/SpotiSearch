from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from requests import post, get
import os
import base64
import json

load_dotenv()
id = os.getenv('CLIENT_ID')
secret = os.getenv('CLIENT_SECRET')
country_codes = {
    'AD': 'Andorra', 'AE': 'United Arab Emirates', 'AG': 'Antigua and Barbuda', 'AL': 'Albania', 'AM': 'Armenia',
    'AO': 'Angola', 'AR': 'Argentina', 'AT': 'Austria', 'AU': 'Australia', 'AZ': 'Azerbaijan', 'BA': 'Bosnia and Herzegovina',
    'BB': 'Barbados', 'BD': 'Bangladesh', 'BE': 'Belgium', 'BF': 'Burkina Faso', 'BG': 'Bulgaria', 'BH': 'Bahrain',
    'BI': 'Burundi', 'BJ': 'Benin', 'BN': 'Brunei Darussalam', 'BO': 'Bolivia', 'BR': 'Brazil', 'BS': 'Bahamas',
    'BT': 'Bhutan', 'BW': 'Botswana', 'BY': 'Belarus', 'BZ': 'Belize', 'CA': 'Canada', 'CH': 'Switzerland',
    'CI': "Côte d'Ivoire", 'CL': 'Chile', 'CM': 'Cameroon', 'CO': 'Colombia', 'CR': 'Costa Rica', 'CV': 'Cabo Verde',
    'CY': 'Cyprus', 'CZ': 'Czech Republic', 'DE': 'Germany', 'DJ': 'Djibouti', 'DK': 'Denmark', 'DM': 'Dominica',
    'DO': 'Dominican Republic', 'DZ': 'Algeria', 'EC': 'Ecuador', 'EE': 'Estonia', 'EG': 'Egypt', 'ES': 'Spain',
    'FI': 'Finland', 'FJ': 'Fiji', 'FM': 'Micronesia', 'FR': 'France', 'GA': 'Gabon', 'GB': 'United Kingdom',
    'GD': 'Grenada', 'GE': 'Georgia', 'GH': 'Ghana', 'GM': 'Gambia', 'GN': 'Guinea', 'GQ': 'Equatorial Guinea',
    'GR': 'Greece', 'GT': 'Guatemala', 'GW': 'Guinea-Bissau', 'GY': 'Guyana', 'HK': 'Hong Kong', 'HN': 'Honduras',
    'HR': 'Croatia', 'HT': 'Haiti', 'HU': 'Hungary', 'ID': 'Indonesia', 'IE': 'Ireland', 'IL': 'Israel',
    'IN': 'India', 'IS': 'Iceland', 'IT': 'Italy', 'JM': 'Jamaica', 'JO': 'Jordan', 'JP': 'Japan', 'KE': 'Kenya',
    'KG': 'Kyrgyzstan', 'KH': 'Cambodia', 'KI': 'Kiribati', 'KM': 'Comoros', 'KN': 'Saint Kitts and Nevis',
    'KR': 'South Korea', 'KW': 'Kuwait', 'KZ': 'Kazakhstan', 'LA': 'Lao People\'s Democratic Republic',
    'LB': 'Lebanon', 'LC': 'Saint Lucia', 'LI': 'Liechtenstein', 'LK': 'Sri Lanka', 'LR': 'Liberia', 'LS': 'Lesotho',
    'LT': 'Lithuania', 'LU': 'Luxembourg', 'LV': 'Latvia', 'MA': 'Morocco', 'MC': 'Monaco', 'MD': 'Moldova',
    'ME': 'Montenegro', 'MG': 'Madagascar', 'MH': 'Marshall Islands', 'MK': 'North Macedonia', 'ML': 'Mali',
    'MN': 'Mongolia', 'MO': 'Macao', 'MR': 'Mauritania', 'MT': 'Malta', 'MU': 'Mauritius', 'MV': 'Maldives',
    'MW': 'Malawi', 'MX': 'Mexico', 'MY': 'Malaysia', 'MZ': 'Mozambique', 'NA': 'Namibia', 'NE': 'Niger',
    'NG': 'Nigeria', 'NI': 'Nicaragua', 'NL': 'Netherlands', 'NO': 'Norway', 'NP': 'Nepal', 'NR': 'Nauru',
    'NZ': 'New Zealand', 'OM': 'Oman', 'PA': 'Panama', 'PE': 'Peru', 'PG': 'Papua New Guinea', 'PH': 'Philippines',
    'PK': 'Pakistan', 'PL': 'Poland', 'PS': 'Palestine', 'PT': 'Portugal', 'PW': 'Palau', 'PY': 'Paraguay',
    'QA': 'Qatar', 'RO': 'Romania', 'RS': 'Serbia', 'RU': 'Russia', 'RW': 'Rwanda', 'SA': 'Saudi Arabia',
    'SB': 'Solomon Islands', 'SC': 'Seychelles', 'SE': 'Sweden', 'SG': 'Singapore', 'SI': 'Slovenia', 'SK': 'Slovakia',
    'SL': 'Sierra Leone', 'SM': 'San Marino', 'SN': 'Senegal', 'SR': 'Suriname', 'ST': 'Sao Tome and Principe',
    'SV': 'El Salvador', 'SZ': 'Eswatini', 'TD': 'Chad', 'TG': 'Togo', 'TH': 'Thailand', 'TL': 'Timor-Leste',
    'TN': 'Tunisia', 'TO': 'Tonga', 'TR': 'Turkey', 'TT': 'Trinidad and Tobago', 'TV': 'Tuvalu', 'TW': 'Taiwan',
    'TZ': 'Tanzania', 'UA': 'Ukraine', 'UG': 'Uganda', 'US': 'United States', 'UY': 'Uruguay', 'UZ': 'Uzbekistan',
    'VC': 'Saint Vincent and the Grenadines', 'VN': 'Vietnam', 'VU': 'Vanuatu', 'WS': 'Samoa', 'XK': 'Kosovo',
    'ZA': 'South Africa', 'ZM': 'Zambia', 'ZW': 'Zimbabwe'
}

app = Flask(__name__)

def get_token():
    auth_string = f'{id}:{secret}'
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token/"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": f"Bearer {token}"}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    try:
        result = get(query_url, headers=headers)
        json_result = json.loads(result.content)["artists"]["items"]

        if len(json_result) == 0:
            return None
        return json_result[0]
    except:
        return None

def get_songs_by_artist(token, artist_id, country_code):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country={country_code}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        country_code = request.form['country']
        query = request.form['artist']
        token = get_token()
        if country_code in country_codes.keys():
            country = country_codes[country_code]
            result = search_for_artist(token, query)
            if result is not None:
                artist_name, artist_id = result['name'], result['id']
                songs = get_songs_by_artist(token, artist_id, country_code)
                return render_template('index.html', country_list=country_codes, songs=songs, artist_name=artist_name, country=country)
        return render_template('index.html', country_list=country_codes, error_message="Artist not found or Spotify does not operate in this country.")
    return render_template('index.html', country_list=country_codes)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
