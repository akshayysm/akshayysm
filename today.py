import os
import requests

# Retrieve GitHub Token from environment
GH_TOKEN = os.getenv("GH_TOKEN")
USERNAME = "akshayysm"

headers = {"Authorization": f"bearer {GH_TOKEN}"} if GH_TOKEN else {}

def fetch_stats():
    # 1. Fallback to GitHub REST API if no token is set
    if not GH_TOKEN:
        print("Warning: GH_TOKEN secret not found. Using public REST API for basic metrics.")
        try:
            res = requests.get(f"https://api.github.com/users/{USERNAME}").json()
            repos_res = requests.get(f"https://api.github.com/users/{USERNAME}/repos?per_page=100").json()
            
            stars = sum(repo.get("stargazers_count", 0) for repo in repos_res) if isinstance(repos_res, list) else 0
            
            return {
                "repos": res.get("public_repos", 17),
                "contributed": 0,
                "stars": stars,
                "commits": 97,
                "followers": res.get("followers", 54)
            }
        except Exception as e:
            print(f"Error fetching REST fallback: {e}")
            return {
                "repos": 17,
                "contributed": 0,
                "stars": 0,
                "commits": 97,
                "followers": 54
            }

    # 2. Complete GraphQL Query for Authenticated Token Runs
    query = """
    query($user: String!) {
      user(login: $user) {
        followers {
          totalCount
        }
        repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
          totalCount
          nodes {
            stargazerCount
          }
        }
        contributionsCollection {
          contributionCalendar {
            totalContributions
          }
          totalCommitContributions
          restrictedContributionsCount
        }
        repositoriesContributedTo(first: 100, contributionTypes: [COMMIT, ISSUE, PULL_REQUEST]) {
          totalCount
        }
      }
    }
    """

    try:
        response = requests.post(
            "https://api.github.com/graphql",
            json={"query": query, "variables": {"user": USERNAME}},
            headers=headers
        )

        if response.status_code != 200:
            print(f"GraphQL API Error: {response.status_code} - {response.text}")
            return {}

        res_data = response.json()
        if "errors" in res_data:
            print("GraphQL Query Errors:", res_data["errors"])

        data = res_data.get("data", {}).get("user", {})
        if not data:
            return {}

        repos = data.get("repositories", {}).get("totalCount", 0)
        stars = sum(repo.get("stargazerCount", 0) for repo in data.get("repositories", {}).get("nodes", []))
        contributed = data.get("repositoriesContributedTo", {}).get("totalCount", 0)
        
        contrib_collection = data.get("contributionsCollection", {})
        calendar_total = contrib_collection.get("contributionCalendar", {}).get("totalContributions", 0)
        
        # Use total contributions from calendar, or fall back to commits count
        commits = calendar_total if calendar_total > 0 else (
            contrib_collection.get("totalCommitContributions", 0) + 
            contrib_collection.get("restrictedContributionsCount", 0)
        )
        followers = data.get("followers", {}).get("totalCount", 0)

        return {
            "repos": repos,
            "contributed": contributed,
            "stars": stars,
            "commits": commits,
            "followers": followers
        }
    except Exception as e:
        print(f"Error fetching GraphQL metrics: {e}")
        return {}

def generate_svg(stats):
    svg_template = f"""<svg xmlns="http://www.w3.org/2000/svg" width="850" height="420" viewBox="0 0 850 420" fill="none">
    <style>
        .bg {{ fill: #0d1117; rx: 10px; }}
        .title {{ font: bold 14px 'Fira Code', monospace; fill: #58a6ff; }}
        .text {{ font: 13px 'Fira Code', monospace; fill: #c9d1d9; white-space: pre; }}
        .label {{ fill: #d2a8ff; font-weight: bold; }}
        .val {{ fill: #79c0ff; }}
        .dim {{ fill: #8b949e; }}
        .green {{ fill: #7ee787; }}
        .red {{ fill: #ff7b72; }}
    </style>
    <rect width="100%" height="100%" class="bg"/>
    <text x="25" y="35" class="title">akshay@akshayysm --------------------------------------------------</text>
    <text x="25" y="60" class="text">. <tspan class="label">OS:</tspan> ............................................. macOS</text>
    <text x="25" y="80" class="text">. <tspan class="label">Uptime:</tspan> ......................................... 4 years, 1 months, 7 days</text>
    <text x="25" y="100" class="text">. <tspan class="label">Role:</tspan> ........................................... Builder</text>
    <text x="25" y="120" class="text">. <tspan class="label">IDE:</tspan> ............................................ VS Code</text>

    <text x="25" y="150" class="text">. <tspan class="label">Languages.Programming &amp; Technologies:</tspan> .......... Rust, TypeScript, Anchor, Solana</text>
    <text x="25" y="170" class="text">. <tspan class="label">Languages.Real:</tspan> ................................. English, Hindi, Kannada</text>

    <text x="25" y="200" class="dim">- Work --------------------------------------------------------</text>
    <text x="25" y="220" class="text">. <tspan class="label">Turbin3:</tspan> ........................................ 2x Graduate</text>

    <text x="25" y="250" class="dim">- Contact -----------------------------------------------------</text>
    <text x="25" y="270" class="text">. <tspan class="label">Email.Work:</tspan> .................................... akshaysm.dev@gmail.com</text>
    <text x="25" y="290" class="text">. <tspan class="label">LinkedIn:</tspan> ...................................... https://www.linkedin.com/in/akshay-meti</text>
    <text x="25" y="310" class="text">. <tspan class="label">X:</tspan> ............................................. https://x.com/akshaaytwt</text>
    <text x="25" y="330" class="text">. <tspan class="label">Discord:</tspan> ....................................... akshaaytwt</text>

    <text x="25" y="360" class="dim">- GitHub Stats ------------------------------------------------</text>
    <text x="25" y="380" class="text">. <tspan class="label">Repos:</tspan> .... <tspan class="val">{stats.get('repos', 0)}</tspan> {{<tspan class="label">Contributed:</tspan> <tspan class="val">{stats.get('contributed', 0)}</tspan>}} | <tspan class="label">Stars:</tspan> ......... <tspan class="val">{stats.get('stars', 0)}</tspan></text>
    <text x="25" y="400" class="text">. <tspan class="label">Commits:</tspan> ................... <tspan class="val">{stats.get('commits', 0)}</tspan> | <tspan class="label">Followers:</tspan> ..... <tspan class="val">{stats.get('followers', 0)}</tspan></text>
</svg>"""
    return svg_template

def main():
    stats = fetch_stats()
    svg_content = generate_svg(stats)
    with open("dark_mode.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)

if __name__ == "__main__":
    main()