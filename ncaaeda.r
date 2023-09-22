library(ggplot2) # for data visualization
library(dplyr) # for data wrangling
library(moderndive) # package of datasets and regression functions 
library(skimr)
library(tidyr)

boxscores <- read.csv("partialboxscores2.csv")

ggplot(boxscores, aes(x=w_pts, y=l_pts)) +
  geom_jitter() +
  labs(title = "Winning vs Losing Points", 
       x= "Winning Points",
       y= "Losing Points")



ggplot(boxscores, aes(x = w_fg_pct)) +
  geom_histogram(aes(fill = "Winner"), position = "identity", alpha = 0.5) +
  geom_histogram(data = boxscores, aes(x = l_fg_pct, fill = "Loser"), position = "identity", alpha = 0.5) +
  labs(title = "Winner vs Loser Total Rebounds",
       x = "Total Rebounds",
       y = "Frequency") +
  theme_minimal() +
  scale_fill_manual(values = c("Winner" = "blue", "Loser" = "red")) +
  guides(fill=guide_legend(title="Outcome"))


ggplot(boxscores, aes(x = factor(1), y = w_drb)) +
  geom_boxplot(aes(fill = "Winner"), position = position_dodge(width = 0.75), width = 0.6) +
  geom_boxplot(data = boxscores, aes(x = factor(2), y = l_drb, fill = "Loser"), position = position_dodge(width = 0.75), width = 0.6) +
  scale_x_discrete(labels = c("Winner", "Loser")) +
  labs(title = "Winner vs Loser Field Goal Percentage",
       x = "",
       y = "Field Goal Percentage") +
  theme_minimal() +
  scale_fill_manual(values = c("Winner" = "grey70", "Loser" = "grey30"))

instances <- boxscores %>%
  filter(l_pts > w_pts)
