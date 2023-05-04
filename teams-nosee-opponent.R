Two <- read.csv("two900v2.csv")
Three <- read.csv("three3600v2.csv")

ntwo <- nrow(Two) # 900
nthree <- nrow(Three) # 3600


SIZETEAMS <- 3 # 2 or 3

numTeams2Players <- 30
numTeams3Players <- 60

if (SIZETEAMS == 2) {
  num <- numTeams2Players # 30
  size <- ntwo # 900
  Data <- Two
} else {
  num <- numTeams3Players # 60
  size <- nthree # 3600
  Data <- Three
}
a<-mean(Data$R)
b<-mean(Data$Md)
c<-mean(Data$Rd)
#print(mean(Data$R))
#print(mean(Data$Md))
#print(mean(Data$Rd))

# STRATEGIES
# "best" : simply chooses the lineup with highest (resp. lowest) R for the Pursuer (resp. the Evader)
# "uniform" : chooses the lineup randomly following a uniform distribution
# "weighted" : chooses the lineup randomly with a weight that is directly (resp. inversely) proportional to R for the Pursuer (resp. the Evader)
#              the "relevance" is an exponent to R before calculating the weights, giving more relevance to the weighting

strategyPursuer = "best" # "best", "weighted" , "uniform"
strategyEvader  = "best" # "best", "weighted" , "uniform"
relevanceP <- 1.0
relevanceE <- 2.0

cumRglobal <- 0
maxRglobal <- -Inf
minRglobal <- +Inf

nrep <- 1000
set.seed(0)
#pursChoice <- 1
dd<-min(Data$R)
Rshifted <- -min(Data$R) + Data$R  # We shifted them so all positives
RexpP <- Rshifted^relevanceP
RexpE <- Rshifted^relevanceE
print(sum(RexpP))
probShifted = RexpP / sum(RexpP)#pursuer

Rinverted <- max(RexpE) - RexpE
probInverted = Rinverted / sum(Rinverted)#evader

for (i in 1:nrep) {
  if (strategyEvader == "uniform") {
    evader <- sample(size, 1, replace= T)
  } else if (strategyEvader == "weighted") {
    evader <- sample(size, 1, replace= T, prob= probInverted)  # We give more probability the lower R is
  } else if (strategyEvader == "best") {
    evader <- which.min(Data$R)
  }
  print(evader)
  Mr <- Data[evader,]$Mr
  Dr <- Data[evader,]$Dr
  Lr <- Data[evader,]$Lr
  Rr <- Data[evader,]$Rr
  Ar <- Data[evader,]$Ar
  # R <- Data[evader,]$R
  
  if (strategyPursuer == "uniform") {
    pursuer <- sample(size, 1, replace= T)
  } else if (strategyPursuer == "weighted") {
    pursuer <- sample(size, 1, replace= T, prob= probShifted)  # We give more probability the higher R is
  } else if (strategyPursuer == "best") {
    pursuer <- which.max(Data$R)
  }
  print(pursuer)
  Md <- Data[pursuer,]$Md
  Dd <- Data[pursuer,]$Dd
  Ld <- Data[pursuer,]$Ld
  Rd <- Data[pursuer,]$Rd
  Ad <- Data[pursuer,]$Ad
  # R <- Data[pursuer,]$R
  
  for (j in 1:size) {
    if ((Data[j,]$Mr == Mr) &&
        (Data[j,]$Dr == Dr) &&
        (Data[j,]$Lr == Lr) &&
        (Data[j,]$Rr == Rr) && 
        (Data[j,]$Ar == Ar)
        &&
        (Data[j,]$Md == Md) &&
        (Data[j,]$Dd == Dd) &&
        (Data[j,]$Ld == Ld) &&
        (Data[j,]$Rd == Rd) && 
        (Data[j,]$Ad == Ad)
       ) 
    {
      #cat("Found")
      break
    }  
  }
  
  R <- Data[j,]$R
  
  cumRglobal <- cumRglobal + R
  if (maxRglobal < R)
    maxRglobal <- R
  if (minRglobal > R)
    minRglobal <- R
}


cat(paste0("\nEnd of"), nrep, "repetitions. Mean R: ", cumRglobal/nrep, ", Max R: ", maxRglobal, ", Min R: ", minRglobal, "\n")
cat(paste0("\nCompare with the mean: ", mean(Data$R), " min: ", min(Data$R), " and max: ", max(Data$R)))



