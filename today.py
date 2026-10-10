import os
import base64
import requests

# Retrieve GitHub Token from environment
GH_TOKEN = os.getenv("GH_TOKEN")
USERNAME = "akshayysm"

headers = {"Authorization": f"bearer {GH_TOKEN}"} if GH_TOKEN else {}

# Bright color palette for the Satoshi figure
COLOR_HOODIE = "#c9d1d9"  # Bright GitHub text white/gray
COLOR_MASK = "#f0e68c"    # Bright golden/khaki for the mask

# Broadened ASCII Art lines
ASCII_LINES = [
    "                                             =*####%#==",
    "                                         =#%@@@%%#%@@%@%#*+",
    "                                       .%%@@@%++++***+@@@%%#*",
    "                                      %@@@%--=*==+=+=+**%@@%%##",
    "                                    -%@@@%.:==+++*==++*++*@@@%%*",
    "                                   =%@@%@.-++*++*++*+=+++##@@%@%*",
    "                                  =%@@@@+.=*+*++*****==++**@@@%@%#",
    "                                 *@@@@@%#%%%%%%@+%%@%%%%%%=@@@@%@%%",
    "                                +%@@@@@#@%%#%%%#+%%#%%%%%%%#@@@@@@%",
    "                               %@@@@#@%+##*+===+%*=-****++#@@@@%@%%",
    "                             %%@@@@@@%@=:==+#::+*##=+++++***%@@@%@@%%%",
    "                            +%%@@@@@%%%---+++-%%%%##+++++++**@@@@%@%##%",
    "                            %%@@@@@@#%@***###@%@@@%%*++*++%##@@@@%@%#%%",
    "                           %%%@@@@@@#%@*%%*#:-++*+=++**+*%%+@@@@@%@@%%%%",
    "                           %%%@@@@@@#%@@%%+==%%%%%*+*+**%%=%@@@@@@@@%#**",
    "                           %%%@@@@@@%@@@%%@%+==+=+=*@#%%%*%@@@@@%@@@%#**",
    "                           %%%%@@@@@%@@@@@@@%%%#%#####%#%@@@@@@#@@@@####",
    "                           %%%%@@@@@%@@@@%@#*+++###@###%@@@@@@@%@@@@#%##",
    "                           %%#@@@@@@@@@@@@%%#+++*##%##%@@@@@@@@@@@@%#%%%",
    "                            %%@%@@@@@@@@@@@@%###%#%#@@@@@@@@@@%@@@@#@%%%",
    "                            %%#@@@@@@%@@@@@@@@@@%@@@@@@@@@@@@%@@@@#@%%%%",
    "                             %*@@@@@%%@@@@@@@@@@@@@@@@@%%%@@*@@@@%@@@%%%",
    "                             %%%@@@@@*%@%%%@@@%%#%#@@%%##%@%%%%*@%@@%%%%",
    "                             %%@#@@@@%%@%%%@@%%%##%%%####@@*#%%@%@@@%%%%",
    "                             %%%@#@@@%#@%%*%@%%+#%%##*+%@@###@@@%@%y%%%%",
    "                             %%%%@%%@@*%@%**+%@+%%**+*#%@%#@@@@%@@%%%%%",
    "                             %%%%%@@%@#%@##+=+%##%++-+@%%@@@@@@@@@%%%%%",
    "                            ===#%@@@%%@@#@##=++**++++##@@@@@@@@@@@%%%%%",
    "                           *%%#%#%#@@@@@%@%=++++++-+@@@@@@@@@@@%%%%%%%%%",
    "                          =%%*%#.*#%@@@@@@%%%%%#%%@@@@@@@@@@%%%%%%%%%%#**",
    "                        :--*%@@@%####%%@@%@@@@@@@@@@@@@@@@%#%%%%%@%%%%%%%#**",
    "                   +-#:++***##%@@@@%##%#%%%@@@@@@@@@@@%%%%%%#%@@%%%%%%%%%%%%%%%",
    "               =+#=###:#####=###*+*############%%@%%%%%#%%###%@%%%%%%%#%%%%%%%%%%%%%%%chain",
    "            -:=***%++###%%#-*#%**############%%%%####%%%%##%%@%%%%%%%#%#%##%%%%%%%%%%%%%#",
    "           :..+**#%#***#%##.*%%**#######%%###%%####%%%%%%%%%@%%%%%%%%%#%%%%%#%%%%%%%%%%%%%#",
    "          -:=**#%%##@*%%==%%*+*#################%###%%%%%@@@%%%%%%%%##%%#%%%%%%%%%%%%%%%%%",
    "         =-++*%%%%#@#%%.#####%#####%%%############%%%%###%%%%%#@%%%%%#%@@#@%%%%%%%%%%%%%%%%",
        "        :==*#%%%%%@@%%+##%%%%#######%%%########%%%%%####@%@%@####%%%%###@@#@%%%%%%%%%%%@%%%",
    "        ++*#%%%@@@@#%+#%%%#####%%%%##%%%######%%%%%#%####@%%@@####%%%%%#%@@#@%%%%%%%%%%%%%%",
    "       -=+##%@@%@@@%%#%%%#####%%%%%%%########%%%%%%@#%####@%%@%##%#%%%%%@%%@@#@%%%%%%%%%%%%%#",
    "       ==+**#%@@@@%%#%%*##%%%%%%%%%%%%%####%%%%%%%@#%%#%@@@@@%%%%%@%%%#%@@@@@%@%%%%%%%%%%%@@",
    "       =++*##%@@@%#%##%%%%%%%%%%%%%%%%%%##%%%%%%%%%%%%%%%%%%%%%@%@%%%#@@@@@%%@%%%%%%%%%%@@",
    "       ==+#*#%@@@@+%%%#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@%%%%%%%%%@@%%%%%%%%%@@@@%%@%%%%%%%%%@@",
    "      *==+*##%@@@%#%##%%%%%%####%%%%%%%%%%%%%%%%%%%%%%%%%@@@@@@@%%%%%%%%%@%@@@@%%%%%%%%%%@@@",
    "      +==+*%%%@@@*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@@@@@@%%%%%%%%%%@@@@@@%%%%%%%%%@@@@",
    "      ===*%%%@@@+%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@%%%%%%%#%%%%%%#+"
]

def load_solana_image_base64():
    """Reads solanaLogoMark.png and returns a base64 encoded data URI."""
    img_filename = "solanaLogoMark.png"
    if os.path.exists(img_filename):
        with open(img_filename, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
            return f"data:image/png;base64,{encoded_string}"
    return ""

def fetch_stats():
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
        except Exception:
            return {"repos": 17, "contributed": 0, "stars": 0, "commits": 97, "followers": 54}

    query = """
    query($user: String!) {
      user(login: $user) {
        followers { totalCount }
        repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
          totalCount
          nodes { stargazerCount }
        }
        contributionsCollection {
          contributionCalendar { totalContributions }
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
            return {}

        data = response.json().get("data", {}).get("user", {})
        if not data:
            return {}

        repos = data.get("repositories", {}).get("totalCount", 0)
        stars = sum(repo.get("stargazerCount", 0) for repo in data.get("repositories", {}).get("nodes", []))
        contributed = data.get("repositoriesContributedTo", {}).get("totalCount", 0)
        
        contrib_collection = data.get("contributionsCollection", {})
        calendar_total = contrib_collection.get("contributionCalendar", {}).get("totalContributions", 0)
        commits = calendar_total if calendar_total > 0 else (
            contrib_collection.get("totalCommitContributions", 0) + 
            contrib_collection.get("restrictedContributionsCount", 0)
        )
        followers = data.get("followers", {}).get("totalCount", 0)

        return {"repos": repos, "contributed": contributed, "stars": stars, "commits": commits, "followers": followers}
    except Exception:
        return {}

def generate_svg(stats):
    ascii_tspans = ""
    # Shifted start_y down from 26 to 34 so the figure moves down toward the bottom border
    start_y = 34
    line_height = 8.8
    for i, line in enumerate(ASCII_LINES):
        color = COLOR_MASK if 3 <= i <= 6 else COLOR_HOODIE
        y_pos = start_y + (i * line_height)
        ascii_tspans += f'    <tspan x="15" y="{y_pos:.1f}" fill="{color}">{line}</tspan>\n'

    solana_b64 = load_solana_image_base64()

    svg_template = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1020" height="480" viewBox="0 0 1020 480" fill="none">
    <style>
        .outer-border {{ fill: #161b22; rx: 14px; stroke: #30363d; stroke-width: 1.5px; }}
        .inner-bg {{ fill: #0d1117; rx: 10px; }}
        .ascii {{ font: 6px/1 'Fira Code', 'Courier New', monospace; white-space: pre; }}
        .title {{ font: bold 13px 'Fira Code', monospace; fill: #58a6ff; }}
        .text {{ font: 12px 'Fira Code', monospace; fill: #c9d1d9; white-space: pre; }}
        .section-header {{ font: bold 12px 'Fira Code', monospace; fill: #79c0ff; white-space: pre; }}
        .label {{ fill: #d2a8ff; font-weight: bold; }}
        .val {{ fill: #79c0ff; }}
        .dim {{ fill: #484f58; }}
    </style>
    
    <!-- Outer Border Frame -->
    <rect width="1020" height="480" class="outer-border"/>
    
    <!-- Inner Background -->
    <rect x="10" y="10" width="1000" height="460" class="inner-bg"/>

    <!-- Left Side: Lowered ASCII Art -->
    <text class="ascii">
{ascii_tspans}    </text>

    <!-- Embedded Solana PNG Image (Moved to match your red circle target on the hoodie) -->
    <image x="245" y="325" width="36" height="32" href="{solana_b64}" />

    <!-- Right Side: Info Panel -->
    <text x="430" y="40" class="title">akshay@akshayysm <tspan class="dim">----------------------------------------</tspan></text>
    <text x="430" y="65" class="text">. <tspan class="label">OS:</tspan> ............................... macOS</text>
    <text x="430" y="87" class="text">. <tspan class="label">Uptime:</tspan> ........................... 4 years, 1 months, 7 days</text>
    <text x="430" y="109" class="text">. <tspan class="label">Role:</tspan> ............................. Builder</text>
    <text x="430" y="131" class="text">. <tspan class="label">IDE:</tspan> .............................. VS Code</text>

    <text x="430" y="163" class="text">. <tspan class="label">Languages.Tech:</tspan> ................... Rust, TypeScript, Anchor, Solana</text>
    <text x="430" y="185" class="text">. <tspan class="label">Languages.Real:</tspan> ................... English, Hindi, Kannada</text>

    <!-- Work Section -->
    <text x="430" y="222" class="section-header"><tspan class="dim">- </tspan>Work <tspan class="dim">------------------------------------------</tspan></text>
    <text x="430" y="244" class="text">. <tspan class="label">Turbin3:</tspan> .......................... 2x Graduate</text>

    <!-- Contact Section -->
    <text x="430" y="281" class="section-header"><tspan class="dim">- </tspan>Contact <tspan class="dim">---------------------------------------</tspan></text>
    <text x="430" y="303" class="text">. <tspan class="label">Email.Work:</tspan> ...................... akshaysm.dev@gmail.com</text>
    <text x="430" y="325" class="text">. <tspan class="label">LinkedIn:</tspan> ........................ https://www.linkedin.com/in/akshay-meti</text>
    <text x="430" y="347" class="text">. <tspan class="label">X:</tspan> ............................... https://x.com/akshaaytwt</text>
    <text x="430" y="369" class="text">. <tspan class="label">Discord:</tspan> ......................... akshaaytwt</text>

    <!-- GitHub Stats Section -->
    <text x="430" y="406" class="section-header"><tspan class="dim">- </tspan>GitHub Stats <tspan class="dim">----------------------------------</tspan></text>
    <text x="430" y="428" class="text">. <tspan class="label">Repos:</tspan> .. <tspan class="val">{stats.get('repos', 0)}</tspan> {{<tspan class="label">Contributed:</tspan> <tspan class="val">{stats.get('contributed', 0)}</tspan>}} | <tspan class="label">Stars:</tspan> ....... <tspan class="val">{stats.get('stars', 0)}</tspan></text>
    <text x="430" y="450" class="text">. <tspan class="label">Commits:</tspan> ................. <tspan class="val">{stats.get('commits', 0)}</tspan> | <tspan class="label">Followers:</tspan> ... <tspan class="val">{stats.get('followers', 0)}</tspan></text>
</svg>"""
    return svg_template

def main():
    stats = fetch_stats()
    svg_content = generate_svg(stats)
    with open("dark_mode.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)

if __name__ == "__main__":
    main()