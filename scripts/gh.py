import sys, os, json
from subprocess import Popen, PIPE

api_url = 'https://api.github.com/repos/tikzit/tikzit'

tok = os.getenv('GITHUB_TOKEN', '')

if tok == '':
	print("Must set GITHUB_TOKEN environment variable.")
	sys.exit(1)

# pretty-print JSON responses
def pr(j): print(json.dumps(j, indent=2))

# call GitHub API with curl
def gh(s, args=[], quiet=True, parse=True, auth=True):
    cmd = (["curl"] +
           (["-s"] if quiet else []) +
           args +
           (["-H", "Authorization: token " + tok] if auth else []) +
           [s if 'https://' in s else api_url + '/' + s])
    # ONLY UN-COMMENT FOR TESTING:
    # print(' '.join(cmd))
    p = Popen(cmd, stdout=PIPE)
    resp = p.stdout.read()
    if parse: return json.loads(resp if resp else '{}')
    else: return resp

def get_release(n):
  rs = [r for r in gh('releases') if r['name'] == n]
  if len(rs) > 0: return rs[0]
  else: return None
