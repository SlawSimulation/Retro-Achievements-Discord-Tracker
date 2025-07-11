require("dotenv").config();
const { Client, GatewayIntentBits, REST, Routes, SlashCommandBuilder } = require("discord.js");
const fetch = require("node-fetch");

const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.MessageContent, GatewayIntentBits.GuildMessages] });

const TOKEN = process.env.DISCORD_BOT_TOKEN;
const CLIENT_ID = process.env.CLIENT_ID;
const GUILD_ID = process.env.GUILD_ID;

// Register the /register command
const commands = [
  new SlashCommandBuilder().setName("register").setDescription("Register your RetroAchievements username")
];

const rest = new REST({ version: "10" }).setToken(TOKEN);
(async () => {
  try {
    await rest.put(Routes.applicationGuildCommands(CLIENT_ID, GUILD_ID), { body: commands });
    console.log("✅ Slash command registered.");
  } catch (err) {
    console.error("❌ Command registration failed:", err);
  }
})();

// Handle the /register command
client.on("interactionCreate", async (interaction) => {
  if (!interaction.isChatInputCommand()) return;
  if (interaction.commandName !== "register") return;

  const discordId = interaction.user.id;
  await interaction.reply({ content: "What is your RetroAchievements username?", ephemeral: true });

  const filter = m => m.author.id === discordId;
  const collector = interaction.channel.createMessageCollector({ filter, time: 15000, max: 1 });

  collector.on("collect", async (m) => {
    const raUsername = m.content;

    const res = await fetch("https://your-domain.com/api/register-user", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ discord_id: discordId, ra_username: raUsername })
    });

    if (res.ok) {
      await m.reply("✅ Registered successfully!");
    } else {
      await m.reply("❌ Registration failed. Try again.");
    }
  });

  collector.on("end", (collected) => {
    if (collected.size === 0) {
      interaction.followUp({ content: "⏰ You didn’t provide a username in time.", ephemeral: true });
    }
  });
});

client.once("ready", () => {
  console.log(`🤖 Logged in as ${client.user.tag}`);
});

client.login(TOKEN);
