const express = require("express");
const fetch = require("node-fetch");
const app = express();

app.use(express.json());

const GITHUB_USERNAME = "YOUR_USERNAME";
const GITHUB_REPO = "YOUR_REPO";
const GITHUB_PAT = "YOUR_GITHUB_PAT";  // KEEP THIS SECRET, don't commit it publicly!

app.post("/api/register-user", async (req, res) => {
  const { discord_id, ra_username } = req.body;

  if (!discord_id || !ra_username) {
    return res.status(400).json({ error: "Missing discord_id or ra_username" });
  }

  try {
    const githubResponse = await fetch(
      `https://api.github.com/repos/${GITHUB_USERNAME}/${GITHUB_REPO}/dispatches`,
      {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${GITHUB_PAT}`,
          "Accept": "application/vnd.github.everest-preview+json",
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          event_type: "register-user",
          client_payload: {
            discord_id,
            ra_username
          }
        })
      }
    );

    if (!githubResponse.ok) {
      const errorText = await githubResponse.text();
      return res.status(githubResponse.status).json({ error: errorText });
    }

    res.json({ success: true });

  } catch (err) {
    console.error("GitHub API error:", err);
    res.status(500).json({ error: "Internal server error" });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
