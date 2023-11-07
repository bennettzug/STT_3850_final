library(ggplot2) # for data visualization
library(dplyr) # for data wrangling
library(moderndive) # package of datasets and regression functions 
library(skimr)
library(tidyr)

boxscores <- read.csv("data/boxscores.csv")
games <- read.csv("data/games_ha.csv")



games$home_won = as.factor(games$home_won)

skim(games)

ggplot(boxscores, aes(x=w_fg_pct, y=l_fg_pct)) +
  geom_jitter() +
  labs(title = "Winning vs Losing True Shooting Percentage", 
       x= "Winning TS%",
       y= "Losing TS%") + 
  geom_smooth(method = lm)



ggplot(boxscores, aes(x = w_ts_pct)) +
  geom_histogram(aes(fill = "Winner"), position = "identity", alpha = 0.5, binwidth=0.02) +
  geom_histogram(data = boxscores, aes(x = l_ts_pct, fill = "Loser"), position = "identity", alpha = 0.5, binwidth=0.02) +
  labs(title = "Winner vs Loser Field Goal Percentage",
       x = "FG%",
       y = "Frequency") +
  theme_minimal() +
  scale_fill_manual(values = c("Winner" = "blue", "Loser" = "red")) +
  guides(fill=guide_legend(title="Outcome"))


ggplot(boxscores, aes(x = w_fg3_pct)) +
  geom_density(aes(fill = "Winner"), position = "identity", alpha = 0.5) +
  geom_density(data = boxscores, aes(x = l_fg3_pct, fill = "Loser"), position = "identity", alpha = 0.5) +
  labs(title = "Winner vs Loser TS%",
       x = "TS%",
       y = "Frequency") +
  theme_minimal() +
  scale_fill_manual(values = c("Winner" = "blue", "Loser" = "red")) +
  guides(fill=guide_legend(title="Outcome"), alpha = 0.5)


ggplot(boxscores, aes(x = factor(1), y = w_orb)) +
  geom_boxplot(aes(fill = "Winner"), position = position_dodge(width = 0.75), width = 0.6) +
  geom_boxplot(data = boxscores, aes(x = factor(2), y = l_orb, fill = "Loser"), position = position_dodge(width = 0.75), width = 0.6) +
  scale_x_discrete(labels = c("Winner", "Loser")) +
  labs(title = "Winner vs Loser Offensive Rebounds",
       x = "",
       y = "Offensive Rebounds") +
  theme_minimal() +
  scale_fill_manual(values = c("Winner" = "grey70", "Loser" = "grey30"))

instances <- boxscores %>%
  filter(l_pts > w_pts)

statistics <- c("mp", "fg", "fga", "fg_pct", "fg2", "fg2a", "fg2_pct", "fg3", "fg3a", "fg3_pct", "ft", "fta", "ft_pct", "orb", "drb", "trb", "ast", "stl", "blk", "tov", "pf", "pts", "ts_pct", "efg_pct", "fg3a_per_fga_pct", "fta_per_fga_pct", "orb_pct", "drb_pct", "trb_pct", "ast_pct", "stl_pct", "blk_pct", "tov_pct", "usg_pct", "off_rtg", "def_rtg")

percentage_row <- numeric(length(statistics))

for (i in seq_along(statistics)) {
  winner_col <- paste0("w_", statistics[i])
  loser_col <- paste0("l_", statistics[i])
  
  winner_values <- boxscores[[winner_col]]
  loser_values <- boxscores[[loser_col]]
  
  # Calculate the percentage
  percentage <- mean(loser_values > winner_values, na.rm = TRUE)
  
  percentage_row[i] <- percentage
}

# Create a data frame with one row containing the percentages
percentages <- data.frame(t(percentage_row))
names(percentages) <- paste0("pct_", statistics)

percentages
