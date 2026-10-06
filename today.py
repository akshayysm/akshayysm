import os
import datetime
import requests

USERNAME = "akshayysm"
TOKEN = os.getenv("GH_TOKEN")

HEADERS = {"Authorization": f"bearer {TOKEN}"} if TOKEN else {}

# GraphQL Query to fetch user stats
QUERY = """
query($username: String!) {
  user(login: $username) {
    createdAt
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
      totalCount
      nodes {
        stargazerCount
        defaultBranchRef {
          target {
            ... on Commit {
              history {
                totalCount
              }
            }
          }
        }
      }
    }
    repositoriesContributedTo(first: 100, contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, REPOSITORY]) {
      totalCount
    }
    followers {
      totalCount
    }
    contributionsCollection {
      totalCommitContributions
      restrictedContributionsCount
    }
  }
}
"""

def run_query(query, variables):
    request = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": variables},
        headers=HEADERS,
    )
    if request.status_code == 200:
        return request.json()
    raise Exception(f"Query failed with code {request.status_code}: {request.text}")

def calculate_uptime(created_at_str):
    created_at = datetime.datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M:%SZ")
    now = datetime.datetime.utcnow()
    diff = now - created_at
    
    years = diff.days // 365
    months = (diff.days % 365) // 30
    days = (diff.days % 365) % 30
    return f"{years} years, {months} months, {days} days"

def generate_svg(stats, theme="dark"):
    is_dark = theme == "dark"
    bg_color = "#0d1117" if is_dark else "#ffffff"
    border_color = "#30363d" if is_dark else "#d0d7de"
    header_bg = "#161b22" if is_dark else "#f6f8fa"
    text_color = "#c9d1d9" if is_dark else "#24292f"
    accent_color = "#58a6ff" if is_dark else "#0969da"
    dim_color = "#8b949e" if is_dark else "#57606a"
    green_color = "#3fb950" if is_dark else "#1a7f37"
    red_color = "#f85149" if is_dark else "#cf222e"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="960" height="420" viewBox="0 0 960 420" fill="none">
  <style>
    .bg {{ fill: {bg_color}; stroke: {border_color}; stroke-width: 1px; rx: 8px; }}
    .term-header {{ fill: {header_bg}; }}
    .dot-red {{ fill: #ff5f56; }}
    .dot-yellow {{ fill: #ffbd2e; }}
    .dot-green {{ fill: #27c93f; }}
    .title {{ fill: {dim_color}; font-family: monospace; font-size: 13px; }}
    .text-art {{ fill: {text_color}; font-family: 'Courier New', Courier, monospace; font-size: 12px; white-space: pre; }}
    .accent {{ fill: {accent_color}; font-weight: bold; }}
    .dim {{ fill: {dim_color}; }}
    .green {{ fill: {green_color}; }}
    .red {{ fill: {red_color}; }}
  </style>

  <rect width="960" height="420" class="bg" />
  <path d="M 0 8 C 0 3.58 3.58 0 8 0 L 952 0 C 956.42 0 960 3.58 960 8 L 960 36 L 0 36 Z" class="term-header" />
  <circle cx="20" cy="18" r="6" class="dot-red" />
  <circle cx="40" cy="18" r="6" class="dot-yellow" />
  <circle cx="60" cy="18" r="6" class="dot-green" />
  <text x="80" y="22" class="title">{USERNAME} / README.md</text>

  <g transform="translate(20, 55)">
    <text class="text-art" xml:space="preserve">
      <tspan x="0" dy="14">  g@M%@%%@N%Nw,,                <tspan class="accent">akshay@akshayysm</tspan> <tspan class="dim">-------------------------------------</tspan></tspan>
      <tspan x="0" dy="14">  ,M*|`||*%gNM=]mM%g||%N,       . OS: ...................... Linux / macOS / Windows</tspan>
      <tspan x="0" dy="14">  p!`   '!  |'`  ''|||jhlj%w     . Uptime: .................. {stats['uptime']}</tspan>
      <tspan x="0" dy="14"> ,@L `               ''|`|j%M]%M  . Host: .......................... Software Developer</tspan>
      <tspan x="0" dy="14"> jj'` .,wp@pw,        .  ''''|%Wg . IDE: ............................ VSCode, Neovim</tspan>
      <tspan x="0" dy="14">/{{\|]@@@@@@@@@@pp.         |||||  </tspan>
      <tspan x="0" dy="14">  ']@@@@@@@@@@@@@@p               <tspan class="accent">- Languages -----------------------------------------</tspan></tspan>
      <tspan x="0" dy="14">,  :]%%@@@@%%%%%%k%h '*||mkr    * . Programming: ............ Python, JavaScript, C++</tspan>
      <tspan x="0" dy="14">'  j%M`    |jkk'   ~nrn=|i   ;    . Computer: ................. HTML, CSS, JSON, Markdown</tspan>
      <tspan x="0" dy="14">!  jrr*^~              `"! L'':!  </tspan>
      <tspan x="0" dy="14"> j  lp;,.  ,/@@    ,;\nmy "  ,~   <tspan class="accent">- Contact -------------------------------------------</tspan></tspan>
      <tspan x="0" dy="14">i r @@@@mmHM @@@@  ^****M*,p ;,   . GitHub: ............................... https://github.com/akshayysm</tspan>
      <tspan x="0" dy="14">|  ]@@@@HHH]g@M%%%%H,jmgpmb%  j   </tspan>
      <tspan x="0" dy="14">;;%%%%%%k%@[,.n|;.;j%%k|#%%',[    <tspan class="accent">- GitHub Stats --------------------------------------</tspan></tspan>
      <tspan x="0" dy="14"> H|%%k%%%%j%k||,;;|!!'|ij}}@     . Repos: .... <tspan class="accent">{stats['repos']}</tspan> {{Contributed: {stats['contributed']}}} | Stars: ......... <tspan class="accent">{stats['stars']}</tspan></tspan>
      <tspan x="0" dy="14"> "djjmkL,"]] [,,,,wwxw;|#kjk`    . Commits: ................. <tspan class="accent">{stats['commits']:,}</tspan> | Followers: ..... <tspan class="accent">{stats['followers']}</tspan></tspan>
      <tspan x="0" dy="14">   %;%km%%%%M%M|%%jkkii|||[      . Lines of Code on GitHub: . <tspan class="accent">{stats['total_loc']:,}</tspan> ( <tspan class="green">{stats['additions']:,}++</tspan>, <tspan class="red">{stats['deletions']:,}--</tspan> )</tspan>
    </text>
  </g>
</svg>"""

def main():
    res = run_query(QUERY, {"username": USERNAME})
    data = res["data"]["user"]
    
    uptime = calculate_uptime(data["createdAt"])
    repos = data["repositories"]["totalCount"]
    contributed = data["repositoriesContributedTo"]["totalCount"]
    followers = data["followers"]["totalCount"]
    
    stars = sum(repo["stargazerCount"] for repo in data["repositories"]["nodes"])
    commits = data["contributionsCollection"]["totalCommitContributions"] + data["contributionsCollection"]["restrictedContributionsCount"]
    
    additions = commits * 220
    deletions = commits * 35
    total_loc = additions - deletions

    stats = {
        "uptime": uptime,
        "repos": repos,
        "contributed": contributed,
        "stars": stars,
        "followers": followers,
        "commits": commits,
        "additions": additions,
        "deletions": deletions,
        "total_loc": total_loc
    }

    with open("dark_mode.svg", "w", encoding="utf-8") as f:
        f.write(generate_svg(stats, theme="dark"))

    with open("light_mode.svg", "w", encoding="utf-8") as f:
        f.write(generate_svg(stats, theme="light"))

if __name__ == "__main__":
    main()