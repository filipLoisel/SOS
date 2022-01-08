library(ggplot2)
library(ggfortify)

run1 <- read.csv("exp2.csv", skip = 6)

increasing_particle_inertia <- read.csv("increasing_particle_inertia.csv", skip = 6)
increasing_personal_confidence <- read.csv("increasing_personal_confidence.csv", skip = 6)
increasing_population_size <- read.csv("increasing_population_size.csv", skip = 6)
increasing_speed <- read.csv("increasing_speed.csv", skip = 6)
increasing_swarm_confidence <- read.csv("increasing_swarm_confidence.csv", skip = 6)

increasing_particle_inertia_penalty_c4 <- read.csv("increasing_particle_inertia_penalty_c4.csv", skip = 6)
increasing_particle_inertia_penalty_c8 <- read.csv("increasing_particle_inertia_penalty_c8.csv", skip = 6)
increasing_personal_confidence_penalty_c4 <- read.csv("increasing_personal_confidence_penalty_c4.csv", skip = 6)
increasing_personal_confidence_penalty_c8 <- read.csv("increasing_personal_confidence_penalty_c8.csv", skip = 6)
increasing_population_size_penalty_c4 <- read.csv("increasing_population_size_penalty_c4.csv", skip = 6)
increasing_population_size_penalty_c8 <- read.csv("increasing_population_size_penalty_c8.csv", skip = 6)
increasing_speed_penalty_c4 <- read.csv("increasing_speed_penalty_c4.csv", skip = 6)
increasing_speed_penalty_c8 <- read.csv("increasing_speed_penalty_c8.csv", skip = 6)
increasing_swarm_confidence_penalty_c4 <- read.csv("increasing_swarm_confidence_penalty_c4.csv", skip = 6)
increasing_swarm_confidence_penalty_c8 <- read.csv("increasing_swarm_confidence_penalty_c8.csv", skip = 6)

increasing_particle_inertia_rejection_c4 <- read.csv("increasing_particle_inertia_rejection_c4.csv", skip = 6)
increasing_particle_inertia_rejection_c8 <- read.csv("increasing_particle_inertia_rejection_c8.csv", skip = 6)
increasing_personal_confidence_rejection_c4 <- read.csv("increasing_personal_confidence_rejection_c4.csv", skip = 6)
increasing_personal_confidence_rejection_c8 <- read.csv("increasing_personal_confidence_rejection_c8.csv", skip = 6)
increasing_population_size_rejection_c4 <- read.csv("increasing_population_size_rejection_c4.csv", skip = 6)
increasing_population_size_rejection_c8 <- read.csv("increasing_population_size_rejection_c8.csv", skip = 6)
increasing_speed_rejection_c4 <- read.csv("increasing_speed_rejection_c4.csv", skip = 6)
increasing_speed_rejection_c8 <- read.csv("increasing_speed_rejection_c8.csv", skip = 6)
increasing_swarm_confidence_rejection_c4 <- read.csv("increasing_swarm_confidence_rejection_c4.csv", skip = 6)
increasing_swarm_confidence_rejection_c8 <- read.csv("increasing_swarm_confidence_rejection_c8.csv", skip = 6)

allTogether <- rbind(increasing_particle_inertia,increasing_personal_confidence,increasing_population_size,
                     increasing_speed,increasing_swarm_confidence,increasing_particle_inertia_penalty_c4,
                     increasing_particle_inertia_penalty_c8,increasing_personal_confidence_penalty_c4,
                     increasing_personal_confidence_penalty_c8, increasing_population_size_penalty_c4,
                     increasing_population_size_penalty_c8, increasing_speed_penalty_c4,
                     increasing_speed_penalty_c8, increasing_swarm_confidence_penalty_c4,
                     increasing_swarm_confidence_penalty_c8, increasing_particle_inertia_rejection_c4,
                     increasing_particle_inertia_rejection_c8, increasing_personal_confidence_rejection_c4,
                     increasing_personal_confidence_rejection_c8, increasing_population_size_rejection_c4,
                     increasing_population_size_rejection_c8, increasing_speed_rejection_c4, 
                     increasing_speed_rejection_c8, increasing_swarm_confidence_rejection_c4,
                     increasing_swarm_confidence_rejection_c8)



pcadat <- allTogether

pcadat[c('trails.mode', 'path.to.load', 'highlight.mode', 
'path.to.save', 'X.step.', 'iterations',
'penalty', 'Constraints', 'constraint_handling_method',
'fitness_function',  'X.run.number.')] <- NULL

pcadat <- sapply(pcadat, as.numeric)

pca_res <- prcomp(pcadat, scale. = T, retx = T)

PCApoints <- as.data.frame(pca_res$x)
PCAloadings <- data.frame(Variables = rownames(pca_res$rotation), pca_res$rotation)

theme<-theme(panel.background = element_blank(),panel.border=element_rect(fill=NA),panel.grid.major = element_blank(),panel.grid.minor = element_blank(),strip.background=element_blank(),axis.text.x=element_text(colour="black"),axis.text.y=element_text(colour="black"),axis.ticks=element_line(colour="black"),plot.margin=unit(c(1,1,1,1),"line"))

ggplot(PCApoints,aes(x=PC1,y=PC2, alpha = allTogether$iterations)) +
  geom_jitter(width = 0.7, height = 0.7) + 
  geom_segment(data = PCAloadings, aes(x = 0, y = 0, xend = (PC1 * 2),
              yend = (PC2 * 2)), arrow = arrow(length = unit(1/2, "picas")),
               alpha = 1, colour = 'red', size = 1) +
  annotate("text", x = (PCAloadings$PC1 * 2.5), y = (PCAloadings$PC2 * 2.5),
           label = PCAloadings$Variables, colour = 'red')
