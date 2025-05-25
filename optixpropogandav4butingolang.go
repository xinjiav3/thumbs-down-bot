package main

import (
	"fmt"
	"log"
	"os"
	"strings"

	"github.com/bwmarrin/discordgo"
	"github.com/cdipaolo/sentiment"
	"github.com/joho/godotenv"
)

func main() {
	// Load .env file
	err := godotenv.Load()
	if err != nil {
		log.Println("Error loading .env file:", err)
	}

	// Get token from environment variable
	token := os.Getenv("DISCORD_BOT_TOKEN2")
	if token == "" {
		log.Fatal("No token provided. Set DISCORD_BOT_TOKEN2 in .env file")
	}

	// Create a new Discord session
	dg, err := discordgo.New("Bot " + token)
	if err != nil {
		log.Fatal("Error creating Discord session:", err)
	}

	// Initialize sentiment analyzer
	analyzer := sentiment.NewAnalyzer()

	// Register handlers
	dg.AddHandler(func(s *discordgo.Session, r *discordgo.Ready) {
		log.Printf("Logged in as %s!", r.User.Username)
	})

	dg.AddHandler(func(s *discordgo.Session, m *discordgo.MessageCreate) {
		// Ignore messages from bots including itself
		if m.Author.Bot {
			return
		}

		// Convert message to lowercase
		content := strings.ToLower(m.Content)

		// Analyze sentiment
		analysis := analyzer.SentimentAnalysis(content, sentiment.English)
		
		// Convert sentiment to score between -1 and 1 (simplified approach)
		// sentiment.Analysis returns 0 for negative and 1 for positive
		var score float64
		if analysis.Score == 1 {
			// Simulate a positive score (0 to 1)
			score = 0.7 // arbitrary positive value
		} else {
			// Simulate a negative score (-1 to 0)
			score = -0.7 // arbitrary negative value
		}

		log.Printf("[DEBUG] Sentiment score: %.2f | Message: %s", score, content)

		// quizbowl vs optix logic
		if strings.Contains(content, "quizbowl") && strings.Contains(content, "optix") {
			if strings.Contains(content, "better") || strings.Contains(content, "superior") || strings.Contains(content, "beats") {
				s.MessageReactionAdd(m.ChannelID, m.ID, "👏")
			} else if score > 0 {
				s.MessageReactionAdd(m.ChannelID, m.ID, "👏")
			}
		}

		// optix or robotics with sentiment
		if strings.Contains(content, "optix") || strings.Contains(content, "robotics") {
			if score < 0 {
				s.MessageReactionAdd(m.ChannelID, m.ID, "👍")
			} else {
				s.MessageReactionAdd(m.ChannelID, m.ID, "👎")
			}
		}

		// santhosh, optix, and good in the same message
		if strings.Contains(content, "santhosh") && strings.Contains(content, "optix") && strings.Contains(content, "good") {
			s.MessageReactionAdd(m.ChannelID, m.ID, "👍")
		}
	})

	// Register the help command
	dg.AddHandler(func(s *discordgo.Session, i *discordgo.InteractionCreate) {
		if i.Type == discordgo.InteractionApplicationCommand {
			if i.ApplicationCommandData().Name == "help" {
				s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
					Type: discordgo.InteractionResponseChannelMessageWithSource,
					Data: &discordgo.InteractionResponseData{
						Content: "**Bot Help** 🤖\n- now uses sentiment analysis to react thumbs up or thumbs down to the according message\n- still muy anti optix\n",
					},
				})
			}
		}
	})

	// Set necessary intents
	dg.Identify.Intents = discordgo.IntentsGuildMessages | discordgo.IntentsGuildMessageReactions

	// Open a websocket connection to Discord
	err = dg.Open()
	if err != nil {
		log.Fatal("Error opening connection:", err)
	}
	defer dg.Close()

	// Register slash commands
	_, err = dg.ApplicationCommandCreate(dg.State.User.ID, "", &discordgo.ApplicationCommand{
		Name:        "help",
		Description: "Get info about what the bot does",
	})
	if err != nil {
		log.Println("Error creating slash command:", err)
	}

	fmt.Println("Bot is now running. Press CTRL-C to exit.")
	// Wait here until CTRL-C or other term signal is received
	select {}
}